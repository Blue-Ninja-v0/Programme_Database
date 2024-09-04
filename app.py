import os
from flask import Flask, request, render_template, flash, redirect, url_for, send_file, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import logging
import pandas as pd
from db_processor import export_database_to_excel, export_specific_upload
from reports import generate_project_overview_report, generate_task_timeline_report, generate_resource_allocation_report, REPORT_VERSION

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with a real secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DATABASE'] = '/Users/blueninja/p6forecaster.db'

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS xer_files
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         filename TEXT NOT NULL,
                         upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def parse_xer_and_update_db(file_path):
    logging.info(f"Starting to parse XER file: {file_path}")
    
    try:
        # Read XER file
        with open(file_path, 'r', encoding='latin-1') as file:
            xer_content = file.read()
        
        # Parse XER content
        tables = {}
        current_table = None
        for line in xer_content.split('\n'):
            if line.startswith('%T'):
                current_table = line.split('\t')[1]
                tables[current_table] = {'fields': [], 'records': []}
            elif line.startswith('%F') and current_table:
                tables[current_table]['fields'] = line.split('\t')[1:]
            elif line.startswith('%R') and current_table:
                tables[current_table]['records'].append(line.split('\t')[1:])
        
        # Connect to SQLite database
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            
            # Insert XER file information
            cursor.execute("INSERT INTO xer_files (filename) VALUES (?)", (os.path.basename(file_path),))
            xer_file_id = cursor.lastrowid
            
            # Create tables and insert data
            for table_name, data in tables.items():
                if data['fields'] and data['records']:
                    # Check if table exists
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                    table_exists = cursor.fetchone()
                    
                    if not table_exists:
                        # Create table
                        fields = [f'"{field}" TEXT' for field in data['fields']]
                        fields.append(f'"xer_file_id" INTEGER')
                        create_table_sql = f'''CREATE TABLE "{table_name}" 
                                               ({', '.join(fields)}, 
                                               FOREIGN KEY(xer_file_id) REFERENCES xer_files(id))'''
                        cursor.execute(create_table_sql)
                        existing_columns = data['fields']
                    else:
                        # Get existing columns
                        cursor.execute(f"PRAGMA table_info({table_name})")
                        existing_columns = [row[1] for row in cursor.fetchall()]
                        
                        # Add missing columns
                        for field in data['fields']:
                            if field not in existing_columns:
                                cursor.execute(f"ALTER TABLE '{table_name}' ADD COLUMN '{field}' TEXT")
                                existing_columns.append(field)
                    
                    # Insert data
                    existing_fields = [f for f in data['fields'] if f in existing_columns]
                    if existing_fields:
                        placeholders = ', '.join(['?' for _ in range(len(existing_fields) + 1)])
                        insert_sql = f'''INSERT INTO "{table_name}" 
                                         ({', '.join(existing_fields)}, xer_file_id) 
                                         VALUES ({placeholders})'''
                        for record in data['records']:
                            existing_values = [record[data['fields'].index(f)] for f in existing_fields]
                            try:
                                cursor.execute(insert_sql, existing_values + [xer_file_id])
                            except sqlite3.OperationalError as e:
                                logging.error(f"Error inserting into {table_name}: {str(e)}")
                                logging.error(f"SQL: {insert_sql}")
                                logging.error(f"Values: {existing_values + [xer_file_id]}")
                    else:
                        logging.warning(f"No matching fields found for table {table_name}")
            
            conn.commit()
        
        logging.info(f"Successfully parsed and updated database with file: {file_path}")
    except Exception as e:
        logging.error(f"Error parsing XER file: {str(e)}")
        raise

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.xer'):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            parse_xer_and_update_db(file_path)
            flash('File successfully uploaded and processed')
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type. Please upload an .xer file.')
            return redirect(request.url)
    
    # Fetch upload IDs
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, filename, upload_date FROM xer_files ORDER BY upload_date DESC")
        uploads = cursor.fetchall()
    
    show_download = True
    return render_template('upload.html', show_download=show_download, uploads=uploads)

@app.route('/download_database')
def download_database():
    try:
        output_path = export_database_to_excel(app.config['DATABASE'])
        return send_file(output_path, as_attachment=True, download_name='database_export.xlsx')
    except Exception as e:
        flash(f'Error exporting database: {str(e)}')
        return redirect(url_for('upload_file'))

@app.route('/download_upload/<int:upload_id>')
def download_upload(upload_id):
    try:
        output_path = export_specific_upload(app.config['DATABASE'], upload_id)
        return send_file(output_path, as_attachment=True, download_name=f'upload_{upload_id}_export.xlsx')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/report/project_overview/<int:upload_id>')
def project_overview_report(upload_id):
    try:
        output_path = generate_project_overview_report(app.config['DATABASE'], upload_id)
        return send_file(output_path, as_attachment=True, download_name=f'project_overview_{upload_id}_v{REPORT_VERSION}.xlsx')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/report/task_timeline/<int:upload_id>')
def task_timeline_report(upload_id):
    try:
        output_path = generate_task_timeline_report(app.config['DATABASE'], upload_id)
        return send_file(output_path, as_attachment=True, download_name=f'task_timeline_{upload_id}_v{REPORT_VERSION}.xlsx')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/report/resource_allocation/<int:upload_id>')
def resource_allocation_report(upload_id):
    try:
        output_path = generate_resource_allocation_report(app.config['DATABASE'], upload_id)
        return send_file(output_path, as_attachment=True, download_name=f'resource_allocation_{upload_id}_v{REPORT_VERSION}.xlsx')
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True)