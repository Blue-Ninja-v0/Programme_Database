# Programme_Database 📊🔍

Programme_Database is a flask web application, used to parse, store, and analyze XER files (exported from Primavera P6). This tool is a crucial component of the larger PMO Tool (and upcoming tools') ecosystem, serving as the data ingestion and storage system. It streamlines the process of managing project data, allowing users to upload XER files, store them in a database, and generate detailed reports for further analysis - leveraging industry reliance on Primavera P6.

## Features 🚀

- 📤 Upload XER files through a user-friendly web interface
- 💾 Automatically parse and store XER data in a SQLite database
- 📥 Export entire database or specific uploads to Excel files
- 🔄 Dynamic table creation based on XER file structure
- 🆔 Unique ID generation for improved data tracking and analysis
- 🔗 Seamless integration with the main PMO Toolfor advanced visualization and analysis

## How It Works 🧠

### Database Structure 📊

Programme_Database uses a SQLite database to store the parsed XER file data. The database structure is dynamic and adapts to the content of the uploaded XER files:

1. A main table called `xer_files` keeps track of all uploaded files, including their filenames and upload dates.
2. For each table in the XER file, a corresponding table is created in the database. These tables are generated dynamically based on the structure of the XER file.
3. Each record in these dynamically created tables is linked to its source XER file through a foreign key relationship with the `xer_files` table.

### Reporting Capabilities 📈

Programme_Database offers advanced reporting features - NEEDS TO BE UPDATED, DOESNT WORK:

1. **Project Overview Report**: Provides a summary of project details, including key dates, costs, and custom fields.
2. **Task Timeline Report**: Offers a detailed view of all tasks, their dates, floats, constraints, and relationships.
3. **Resource Allocation Report**: Presents resource assignments, quantities, and costs across tasks.

These reports can be generated individually or as a combined comprehensive report.

### Data Analysis 🔬

The application facilitates data analysis through:

- Detailed breakdowns of project components
- Timeline visualizations
- Resource utilization insights
- Custom field tracking

### Integration with PMO_Tool 🔗

Programme_Database works in tandem with the main PMO_Tool:

- Provides a robust data foundation for advanced visualization and analysis features
- Enables seamless data flow between XER files and the PMO tool analysis environment
- Supports complex queries and data manipulations required by the main app

## Installation 🛠️

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/Programme_Database.git
   cd Programme_Database
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

3. Use the web interface to:
   - Upload XER files
   - View uploads
   - Generate reports
   - Export data

4. Integrate with the main P6 Unified App for advanced analysis and visualization

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Support 💬

If you encounter any problems or have any questions, please open an issue in the GitHub repository.

Happy forecasting! 📈🎉