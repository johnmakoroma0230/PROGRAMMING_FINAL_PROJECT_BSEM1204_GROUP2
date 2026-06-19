# Code Explanation

## `main.py`

This is the starting point of the program. It prepares the database and opens the login window.

Important function:

- `main()` runs the setup and starts the application.

## `login.py`

This file controls the login screen. It checks the username and password before opening the dashboard.

Important parts:

- `USERNAME` and `PASSWORD` store the login details.
- `LoginWindow` builds the login interface.
- `check_login()` checks if the user entered the correct details.
- `run_login()` starts the login window.

## `dashboard.py`

This file contains the main application window. It displays records and gives the user buttons for all main actions.

Important parts:

- `Dashboard` is the main dashboard class.
- `build_interface()` builds the screen layout.
- `load_records()` loads records from the database into the table.
- `open_record_form()` opens the add/update form.
- `is_valid_record()` checks that the user entered correct data.
- `delete_selected_record()` deletes a selected record.
- `create_all_report()`, `create_weekly_report()`, `create_monthly_report()`, and `create_yearly_report()` generate reports.
- `export_csv()` exports records for use in spreadsheet software.

## `database.py`

This file contains all SQLite database operations. Keeping database code here makes the project more organized.

Important functions:

- `setup_database()` creates the table and adds sample records if the database is empty.
- `fetch_all_records()` gets all saved records.
- `search_records()` searches records using a keyword.
- `filter_records()` filters records by gender or status.
- `add_record()` saves a new record.
- `update_record()` changes an existing record.
- `delete_record()` removes a record.
- `get_dashboard_counts()` calculates dashboard statistics.
- `get_grouped_counts()` prepares grouped data for charts.

## `charts.py`

This file creates the charts for the system.

Important functions:

- `show_bar_chart()` displays records grouped by status.
- `show_pie_chart()` displays gender distribution.
- `show_line_graph()` displays record registration growth.

## `reports.py`

This file creates report files.

Important functions:

- `generate_all_records_report()` creates a PDF for all records.
- `generate_weekly_report()` creates a PDF for recent weekly records.
- `generate_monthly_report()` creates a PDF for recent monthly records.
- `generate_yearly_report()` creates a PDF for yearly records.
- `export_records_to_csv()` exports records into a CSV file.

## `test_db.py`

This file is used to test that the database works without opening the GUI.

Important function:

- `main()` runs the database setup, prints dashboard counts, and prints sample records.
