import sqlite3
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from reportlab.pdfgen import canvas
from datetime import datetime


# ---------------- DATABASE FUNCTIONS ---------------- #

def load_records():

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


def search_records():

    keyword = search_entry.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM records
        WHERE full_name LIKE ?
        OR status LIKE ?
        OR CAST(id AS TEXT) LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


def filter_gender():

    gender = gender_var.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    if gender == "All":
        cursor.execute("SELECT * FROM records")
    else:
        cursor.execute(
            "SELECT * FROM records WHERE gender=?",
            (gender,)
        )

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


def filter_status():

    status = status_var.get()

    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    if status == "All":
        cursor.execute("SELECT * FROM records")
    else:
        cursor.execute(
            "SELECT * FROM records WHERE status=?",
            (status,)
        )

    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

    conn.close()


# ---------------- CHARTS ---------------- #

def bar_chart():

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM records
        GROUP BY status
    """)

    data = cursor.fetchall()
    conn.close()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.bar(labels, values)

    plt.title("Records by Status")
    plt.xlabel("Status")
    plt.ylabel("Number of Records")

    plt.show()


def pie_chart():

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT gender, COUNT(*)
        FROM records
        GROUP BY gender
    """)

    data = cursor.fetchall()
    conn.close()

    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    plt.pie(values, labels=labels, autopct="%1.1f%%")

    plt.title("Gender Distribution")

    plt.show()


def line_graph():

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT created_date
        FROM records
    """)

    rows = cursor.fetchall()

    conn.close()

    dates = [row[0] for row in rows]

    values = list(range(1, len(dates) + 1))

    plt.plot(values, marker="o")

    plt.title("Record Registration Trend")
    plt.xlabel("Record Number")
    plt.ylabel("Growth")

    plt.show()


# ---------------- PDF REPORT ---------------- #

def generate_pdf():

    pdf = canvas.Canvas("Hilltop_Report.pdf")

    pdf.setTitle("Hilltop Community Report")

    pdf.drawString(
        50,
        800,
        "Hilltop Community Record Report"
    )

    pdf.drawString(
        50,
        780,
        f"Generated: {datetime.now()}"
    )

    conn = sqlite3.connect("hilltop_records.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM records")

    rows = cursor.fetchall()

    y = 740

    for row in rows:

        pdf.drawString(
            50,
            y,
            str(row)
        )

        y -= 20

        if y < 50:
            pdf.showPage()
            y = 800

    conn.close()

    pdf.save()

    messagebox.showinfo(
        "Success",
        "PDF Report Generated Successfully"
    )


# ---------------- MAIN WINDOW ---------------- #

root = Tk()

root.title("Hilltop Community Record Management System")

root.geometry("1300x700")

root.configure(bg="#f4f6f9")


# ---------------- TITLE ---------------- #

title = Label(
    root,
    text="HILLTOP COMMUNITY RECORD MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#f4f6f9"
)

title.pack(pady=10)


# ---------------- TOTAL RECORDS ---------------- #

conn = sqlite3.connect("hilltop_records.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM records")

total_records = cursor.fetchone()[0]

conn.close()

Label(
    root,
    text=f"Total Records: {total_records}",
    font=("Arial", 12, "bold"),
    bg="green",
    fg="white",
    padx=20,
    pady=10
).pack()


# ---------------- SEARCH FRAME ---------------- #

search_frame = Frame(root)

search_frame.pack(pady=10)

Label(search_frame, text="Search").grid(row=0, column=0)

search_entry = Entry(search_frame, width=30)

search_entry.grid(row=0, column=1, padx=10)

Button(
    search_frame,
    text="Search",
    command=search_records
).grid(row=0, column=2)


# ---------------- GENDER FILTER ---------------- #

gender_var = StringVar()

gender_var.set("All")

gender_combo = ttk.Combobox(
    search_frame,
    textvariable=gender_var,
    values=["All", "Male", "Female"]
)

gender_combo.grid(row=0, column=3, padx=10)

Button(
    search_frame,
    text="Gender Filter",
    command=filter_gender
).grid(row=0, column=4)


# ---------------- STATUS FILTER ---------------- #

status_var = StringVar()

status_var.set("All")

status_combo = ttk.Combobox(
    search_frame,
    textvariable=status_var,
    values=["All", "Active", "Inactive", "Pending"]
)

status_combo.grid(row=0, column=5, padx=10)

Button(
    search_frame,
    text="Status Filter",
    command=filter_status
).grid(row=0, column=6)


# ---------------- TABLE ---------------- #

table_frame = Frame(root)

table_frame.pack(pady=20)

columns = (
    "ID",
    "Name",
    "Gender",
    "Phone",
    "Address",
    "Status",
    "Date"
)

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=18
)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=160)

tree.pack()


# ---------------- BUTTONS ---------------- #

button_frame = Frame(root)

button_frame.pack(pady=10)

Button(
    button_frame,
    text="Bar Chart",
    width=15,
    command=bar_chart
).grid(row=0, column=0, padx=10)

Button(
    button_frame,
    text="Pie Chart",
    width=15,
    command=pie_chart
).grid(row=0, column=1, padx=10)

Button(
    button_frame,
    text="Line Graph",
    width=15,
    command=line_graph
).grid(row=0, column=2, padx=10)

Button(
    button_frame,
    text="Generate PDF",
    width=15,
    command=generate_pdf
).grid(row=0, column=3, padx=10)


# ---------------- LOAD DATA ---------------- #

load_records()

root.mainloop()