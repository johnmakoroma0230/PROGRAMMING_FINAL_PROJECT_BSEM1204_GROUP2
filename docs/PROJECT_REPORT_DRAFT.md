# Hilltop Community Record Management System

## Cover Page

Course: PROG103 - Principle of Structured Programming  
Project Title: Structured Digital Solution for Public Service  
System Name: Hilltop Community Record Management System  
Project Area: Community Data System  
Group: Group 2  
Semester: 02  

## Project Rationale

### Problem Description

Many communities in Sierra Leone still manage resident and service records using paper books or scattered files. This makes it difficult to search records quickly, count active and inactive community members, prepare reports, or understand trends in community registration. Paper-based systems can also lead to lost records, duplicated entries, and slow decision-making.

The Hilltop Community Record Management System provides a simple digital solution for storing, updating, searching, filtering, and reporting community records. The system supports basic community administration by helping leaders keep organized information about residents and their current status.

### System Explanation

The system is a GUI-based Python application built with Tkinter. Users first log in using the login window. After successful login, the dashboard opens and displays community records in a table.

The dashboard allows users to:

- Add new community records
- Update existing records
- Delete selected records
- Search records by name, gender, phone, address, status, or ID
- Filter records by gender or status
- View dashboard statistics
- Generate charts
- Generate PDF reports
- Export records to CSV

SQLite is used to store the records locally. This makes the system easy to run without needing an internet connection or a separate database server.

### Structured Programming Application

The project follows structured programming principles by separating the program into modules and functions.

- `main.py` starts the program.
- `login.py` handles user login.
- `dashboard.py` handles the main graphical interface.
- `database.py` handles database creation, record storage, searching, filtering, updating, and deleting.
- `charts.py` handles visual charts.
- `reports.py` handles PDF report generation and CSV export.
- `test_db.py` checks that the database functions work.

The program uses variables, constants, data types, decision structures, loops, and user-defined functions. Examples include:

- Decision structures are used for login checking, form validation, filtering, and delete confirmation.
- Loops are used to display records in the table, generate PDF rows, export CSV rows, and build GUI controls.
- Functions are used throughout the project to keep the code organized and reusable.

### SDG Relevance

The system supports SDG 11: Sustainable Cities and Communities. Organized community data helps local leaders understand resident needs, prepare reports, and support better planning for community services.

The system also supports SDG 16: Peace, Justice and Strong Institutions because it improves record keeping, transparency, and access to community information.

### Data, Privacy, and Compliance

The system stores community data locally in an SQLite database. Access is protected by a basic login screen. The project uses only the data needed for community record management, such as name, gender, phone, address, status, and registration date.

For ethical use of data, the system should only be used by authorized community administrators. User data should not be shared publicly without permission.

### Data Accessibility and Interoperability

The system displays records in a clear table and can generate PDF reports for printing. It can also export records to CSV, which allows the data to be opened in spreadsheet software such as Microsoft Excel or Google Sheets.

### Screenshots

Add two system screenshots here:

1. Login window screenshot
2. Dashboard window screenshot

Add two source code screenshots here:

1. `database.py` showing database functions
2. `dashboard.py` showing GUI logic

### GitHub Evidence

Add screenshots of:

1. `git status`
2. `git commit`
3. `git push`

## Conclusion

The Hilltop Community Record Management System is a practical community data system that addresses a real record management problem. It uses Python, Tkinter, SQLite, charts, reports, and modular structured programming to provide a simple and useful public service application.
