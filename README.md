# P6Forecaster_DB 📊🔍

P6Forecaster_DB is a powerful web application designed to parse, store, and analyze XER files (typically exported from Primavera P6) with ease. This tool streamlines the process of managing project data, allowing users to upload XER files, store them in a database, and export the data for further analysis.

## Features 🚀

- 📤 Upload XER files through a user-friendly web interface
- 💾 Automatically parse and store XER data in a SQLite database
- 📥 Export entire database or specific uploads to Excel files
- 🔄 Dynamic table creation based on XER file structure
- 🛠️ Built with Flask for a lightweight and efficient web application
- 🆔 Planned feature: Unique ID generation for improved data tracking

## How It Works 🧠

### Database Structure 📊

P6Forecaster_DB uses a SQLite database to store the parsed XER file data. The database structure is dynamic and adapts to the content of the uploaded XER files:

1. A main table called `xer_files` keeps track of all uploaded files, including their filenames and upload dates.
2. For each table in the XER file, a corresponding table is created in the database. These tables are generated dynamically based on the structure of the XER file.
3. Each record in these dynamically created tables is linked to its source XER file through a foreign key relationship with the `xer_files` table.

### Additional Counting Table 🔢

The application includes an additional table for counting purposes. This table helps in tracking and analyzing the number of records across different uploads and tables.

### Unique ID Feature (Planned) 🆔

A future update will introduce a unique ID feature to enhance data tracking and management. This feature will:

- Generate a unique identifier for each record across all tables
- Improve data integrity and traceability
- Facilitate more advanced querying and data analysis capabilities

## Installation 🛠️

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/P6Forecaster_DB.git
   cd P6Forecaster_DB
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage 🖥️

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

3. Use the web interface to upload XER files, view uploads, and export data

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.


## Support 💬

If you encounter any problems or have any questions, please open an issue in the GitHub repository.

Happy forecasting! 📈🎉