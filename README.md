# Hilltop Community Record Management System

This is a Python desktop application for managing community records for Hilltop. It was built for the Structured Programming final project.

## Features

- Login page for system access
- Add, update, delete, search, and filter records
- Dashboard cards for total, active, inactive, and pending records
- Bar chart for record status
- Pie chart for gender distribution
- Line graph for registration trend
- PDF reports for all records, weekly records, monthly records, and yearly records
- CSV export for spreadsheet access and data sharing
- SQLite database storage

## Assignment Alignment

This project is a Community Data System for Hilltop. It addresses community record management in Sierra Leone and supports SDG 11: Sustainable Cities and Communities, and SDG 16: Peace, Justice and Strong Institutions.

The project demonstrates structured programming through:

- Modular Python files
- User-defined functions
- Decision structures
- Loops
- Input validation
- Separation of GUI and backend logic
- File-based reports and CSV export

## Login Details

Username:

```text
lucian
```

Password:

```text
luciamn123
```

## How to Run

Install the required libraries:

```bash
pip install matplotlib reportlab
```

Run the application:

```bash
python main.py
```


To check the database records from the terminal:

```bash
python test_db.py
```

## Project Files

- `login.py` contains the login window.
- `dashboard.py` contains the main record management interface.
- `database.py` contains all database functions.

## Documentation

- `docs/PROJECT_REPORT_DRAFT.md` contains a written report draft for submission.
- `docs/CODE_EXPLANATION.md` explains each source code file for presentation.
