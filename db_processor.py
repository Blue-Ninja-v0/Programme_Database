import sqlite3
import pandas as pd
import os
import tempfile

def export_database_to_excel(db_path):
    conn = sqlite3.connect(db_path)
    
    # Get all table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        output_path = temp_file.name
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for table_name in tables:
            table_name = table_name[0]
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            df.to_excel(writer, sheet_name=table_name, index=False)
    
    conn.close()
    return output_path

def export_specific_upload(db_path, upload_id):
    conn = sqlite3.connect(db_path)
    
    # Get all table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
        output_path = temp_file.name
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for table_name in tables:
            table_name = table_name[0]
            if table_name == 'xer_files':
                df = pd.read_sql_query(f"SELECT * FROM {table_name} WHERE id = ?", conn, params=(upload_id,))
            elif table_name == 'sqlite_sequence':
                # Skip this system table
                continue
            else:
                df = pd.read_sql_query(f"SELECT * FROM {table_name} WHERE xer_file_id = ?", conn, params=(upload_id,))
            if not df.empty:
                df.to_excel(writer, sheet_name=table_name, index=False)
    
    conn.close()
    return output_path

# Placeholder for future export functions
def export_custom_report(db_path, output_path):
    # This is a placeholder for future custom report exports
    pass

if __name__ == "__main__":
    db_path = 'p6forecaster.db'
    output_path = export_database_to_excel(db_path)
    print(f"Full database exported to: {output_path}")
    
    # Test export_specific_upload
    upload_id = 1  # Replace with an actual upload ID for testing
    specific_output_path = export_specific_upload(db_path, upload_id)
    print(f"Specific upload (ID: {upload_id}) exported to: {specific_output_path}")