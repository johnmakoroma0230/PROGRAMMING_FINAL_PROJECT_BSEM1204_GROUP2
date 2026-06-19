import sqlite3
from datetime import datetime

from tkinter import (
    Tk,
    Toplevel,
    Frame,
    Label,
    Entry,
    Button,
    StringVar,
    END,
    messagebox
)

from tkinter import ttk

import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas

from database import setup_database

DB_NAME = "hilltop_records.db"
REPORT_TOP = 800
REPORT_BOTTOM = 50

def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                status TEXT NOT NULL,
                created_date TEXT NOT NULL
            )
            """
        )


def fetch_records(query="SELECT * FROM records", params=()):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def run_query(query, params=()):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()


def clear_table():
    for item in tree.get_children():
        tree.delete(item)


def show_records(rows):
    clear_table()
    for row in rows:
        tree.insert("", END, values=row)


def load_records():
    show_records(fetch_records("SELECT * FROM records ORDER BY id DESC"))
    update_dashboard()


def update_dashboard():
    rows = fetch_records(
        """
        SELECT
            COUNT(*),
            SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Inactive' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END)
        FROM records
        """
    )
    total, active, inactive, pending = rows[0]

    total_var.set(f"Total Records: {total or 0}")
    stat_total.config(text=f"Total\n{total or 0}")
    stat_active.config(text=f"Active\n{active or 0}")
    stat_inactive.config(text=f"Inactive\n{inactive or 0}")
    stat_pending.config(text=f"Pending\n{pending or 0}")


def search_records():
    keyword = search_entry.get().strip()

    if not keyword:
        load_records()
        return

    show_records(
        fetch_records(
            """
            SELECT * FROM records
            WHERE full_name LIKE ?
               OR status LIKE ?
               OR gender LIKE ?
               OR phone LIKE ?
               OR CAST(id AS TEXT) LIKE ?
            ORDER BY id ASC
            """,
            tuple([f"%{keyword}%"] * 5),
        )
    )


def filter_gender():
    gender = gender_var.get()

    if gender == "All":
        load_records()
    else:
        show_records(
            fetch_records(
                "SELECT * FROM records WHERE gender = ? ORDER BY id ASC",
                (gender,),
            )
        )


def filter_status():
    status = status_var.get()

    if status == "All":
        load_records()
    else:
        show_records(
            fetch_records(
                "SELECT * FROM records WHERE status = ? ORDER BY id ASC",
                (status,),
            )
        )


def selected_record():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning("No Selection", "Please select a record first.")
        return None

    return tree.item(selected)["values"]


def get_summary(field):
    return fetch_records(
        f"""
        SELECT {field}, COUNT(*)
        FROM records
        GROUP BY {field}
        ORDER BY COUNT(*) ASC
        """
    )


def bar_chart():
    data = get_summary("status")

    if not data:
        messagebox.showinfo("No Data", "There are no records to chart.")
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, values, color=["#2e7d32", "#c62828", "#ef6c00"])
    plt.title("Records by Status")
    plt.xlabel("Status")
    plt.ylabel("Number of Records")
    plt.tight_layout()
    plt.show()


def pie_chart():
    data = get_summary("gender")

    if not data:
        messagebox.showinfo("No Data", "There are no records to chart.")
        return

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Gender Distribution")
    plt.tight_layout()
    plt.show()


def line_graph():
    data = fetch_records(
        """
        SELECT created_date, COUNT(*)
        FROM records
        GROUP BY created_date
        ORDER BY created_date
        """
    )

    if not data:
        messagebox.showinfo("No Data", "There are no records to chart.")
        return

    dates = [row[0] for row in data]
    totals = []
    running_total = 0

    for row in data:
        running_total += row[1]
        totals.append(running_total)

    plt.figure(figsize=(8, 5))
    plt.plot(dates, totals, marker="o", color="#1565c0")
    plt.title("Record Registration Trend")
    plt.xlabel("Date")
    plt.ylabel("Total Records")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.show()


def write_report(filename, title, rows):
    pdf = canvas.Canvas(filename)
    pdf.setTitle(title)

    y = REPORT_TOP
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, title)

    y -= 20
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    y -= 35
    if not rows:
        pdf.drawString(50, y, "No records found for this report.")
    else:
        for row in rows:
            pdf.drawString(50, y, format_record(row))
            y -= 18

            if y < REPORT_BOTTOM:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = REPORT_TOP

    pdf.save()


def format_record(row):
    return (
        f"ID: {row[0]} | Name: {row[1]} | Gender: {row[2]} | "
        f"Phone: {row[3]} | Status: {row[5]} | Date: {row[6]}"
    )


def generate_pdf():
    rows = fetch_records("SELECT * FROM records ORDER BY id ASC")
    write_report("Hilltop_Report.pdf", "Hilltop Community Record Report", rows)
    messagebox.showinfo("Success", "PDF report generated successfully.")


def date_report(days, filename, title):
    rows = fetch_records(
        """
        SELECT * FROM records
        WHERE created_date >= date('now', ?)
        ORDER BY created_date ASC
        """,
        (f"-{days} days",),
    )
    write_report(filename, title, rows)
    messagebox.showinfo("Success", f"{title} generated successfully.")


def weekly_report():
    date_report(7, "Weekly_Report.pdf", "Hilltop Weekly Report")


def monthly_report():
    date_report(30, "Monthly_Report.pdf", "Hilltop Monthly Report")


def yearly_report():
    date_report(365, "Yearly_Report.pdf", "Hilltop Yearly Report")


def record_form(title, button_text, existing_record=None):
    form = Toplevel(root)
    form.title(title)
    form.geometry("420x430")
    form.configure(bg="#f4f6f9")
    form.resizable(False, False)

    entries = {}

    fields = [
        ("full_name", "Full Name"),
        ("gender", "Gender"),
        ("phone", "Phone"),
        ("address", "Address"),
        ("status", "Status"),
        ("created_date", "Date (YYYY-MM-DD)"),
    ]

    for index, (key, label_text) in enumerate(fields):
        Label(form, text=label_text, bg="#f4f6f9").grid(
            row=index, column=0, padx=20, pady=8, sticky="w"
        )

        if key == "gender":
            entry = ttk.Combobox(form, values=["Male", "Female", "Other"], width=27, state="readonly")
        elif key == "status":
            entry = ttk.Combobox(
                form,
                values=["Active", "Inactive", "Pending"],
                width=27,
                state="readonly",
            )
        else:
            entry = Entry(form, width=30)

        entry.grid(row=index, column=1, padx=20, pady=8)
        entries[key] = entry

    if existing_record:
        values = existing_record[1:]
        for index, key in enumerate(entries):
            entries[key].insert(0, values[index])
    else:
        entries["gender"].set("Male")
        entries["status"].set("Active")
        entries["created_date"].insert(0, datetime.now().strftime("%Y-%m-%d"))

    def save_record():
        name = entries["full_name"].get().strip()
        gender = entries["gender"].get().strip()
        phone = entries["phone"].get().strip()
        address = entries["address"].get().strip()
        status = entries["status"].get().strip()
        created_date = entries["created_date"].get().strip()

        if not name or not gender or not status or not created_date:
            messagebox.showwarning(
                "Missing Details",
                "Full name, gender, status, and date are required.",
            )
            return

        try:
            datetime.strptime(created_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Invalid Date", "Please use the date format YYYY-MM-DD.")
            return

        if existing_record:
            run_query(
                """
                UPDATE records
                SET full_name = ?,
                    gender = ?,
                    phone = ?,
                    address = ?,
                    status = ?,
                    created_date = ?
                WHERE id = ?
                """,
                (name, gender, phone, address, status, created_date, existing_record[0]),
            )
            messagebox.showinfo("Success", "Record updated successfully.")
        else:
            run_query(
                """
                INSERT INTO records
                (full_name, gender, phone, address, status, created_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, gender, phone, address, status, created_date),
            )
            messagebox.showinfo("Success", "Record added successfully.")

        form.destroy()
        load_records()

    Button(form, text=button_text, width=18, command=save_record).grid(
        row=len(fields), column=0, columnspan=2, pady=25
    )


def add_record():
    record_form("Add Record", "Save Record")


def update_record():
    record = selected_record()

    if record:
        record_form("Update Record", "Save Changes", record)


def delete_record():
    record = selected_record()

    if not record:
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete the record for {record[1]}?",
    )

    if not confirm:
        return

    run_query("DELETE FROM records WHERE id = ?", (record[0],))
    load_records()
    messagebox.showinfo("Success", "Record deleted successfully.")


setup_database()

root = Tk()
root.title("Hilltop Community Record Management System")
root.geometry("1300x720")
root.configure(bg="#f4f6f9")

Label(
    root,
    text="HILLTOP COMMUNITY RECORD MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#f4f6f9",
).pack(pady=10)

total_var = StringVar(value="Total Records: 0")
Label(
    root,
    textvariable=total_var,
    font=("Arial", 12, "bold"),
    bg="#2e7d32",
    fg="white",
    padx=20,
    pady=10,
).pack()

stats_frame = Frame(root, bg="#f4f6f9")
stats_frame.pack(pady=10)

stat_total = Label(
    stats_frame,
    text="Total\n0",
    bg="#1565c0",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
    height=3,
)
stat_total.grid(row=0, column=0, padx=10)

stat_active = Label(
    stats_frame,
    text="Active\n0",
    bg="#2e7d32",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
    height=3,
)
stat_active.grid(row=0, column=1, padx=10)

stat_inactive = Label(
    stats_frame,
    text="Inactive\n0",
    bg="#c62828",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
    height=3,
)
stat_inactive.grid(row=0, column=2, padx=10)

stat_pending = Label(
    stats_frame,
    text="Pending\n0",
    bg="#ef6c00",
    fg="white",
    font=("Arial", 12, "bold"),
    width=15,
    height=3,
)
stat_pending.grid(row=0, column=3, padx=10)

search_frame = Frame(root, bg="#f4f6f9")
search_frame.pack(pady=10)

Label(search_frame, text="Search", bg="#f4f6f9").grid(row=0, column=0)

search_entry = Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=8)

Button(search_frame, text="Search", command=search_records).grid(row=0, column=2, padx=4)
Button(search_frame, text="Show All", command=load_records).grid(row=0, column=3, padx=4)

gender_var = StringVar(value="All")
gender_combo = ttk.Combobox(
    search_frame,
    textvariable=gender_var,
    values=["All", "Male", "Female", "Other"],
    width=12,
    state="readonly",
)
gender_combo.grid(row=0, column=4, padx=8)
Button(search_frame, text="Filter Gender", command=filter_gender).grid(row=0, column=5)

status_var = StringVar(value="All")
status_combo = ttk.Combobox(
    search_frame,
    textvariable=status_var,
    values=["All", "Active", "Inactive", "Pending"],
    width=12,
    state="readonly",
)
status_combo.grid(row=0, column=6, padx=8)
Button(search_frame, text="Filter Status", command=filter_status).grid(row=0, column=7)

table_frame = Frame(root)
table_frame.pack(pady=15)

columns = ("ID", "Name", "Gender", "Phone", "Address", "Status", "Date")

tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=17)

column_widths = {
    "ID": 60,
    "Name": 190,
    "Gender": 100,
    "Phone": 140,
    "Address": 260,
    "Status": 120,
    "Date": 130,
}

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=column_widths[col], anchor="center")

tree.pack(side="left")

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

button_frame = Frame(root, bg="#f4f6f9")
button_frame.pack(pady=10)

buttons = [
    ("Add Record", add_record),
    ("Update Record", update_record),
    ("Delete Record", delete_record),
    ("Bar Chart", bar_chart),
    ("Pie Chart", pie_chart),
    ("Line Graph", line_graph),
    ("Generate PDF", generate_pdf),
]

for index, (text, command) in enumerate(buttons):
    Button(button_frame, text=text, width=15, command=command).grid(
        row=0, column=index, padx=6, pady=5
    )

report_buttons = [
    ("Weekly Report", weekly_report),
    ("Monthly Report", monthly_report),
    ("Yearly Report", yearly_report),
]

for index, (text, command) in enumerate(report_buttons):
    Button(button_frame, text=text, width=15, command=command).grid(
        row=1, column=index, padx=6, pady=5
    )

load_records()
root.mainloop()
