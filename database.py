import sqlite3

conn = sqlite3.connect("hilltop_records.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    gender TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    status TEXT NOT NULL,
    created_date TEXT NOT NULL
)
""")

records = [
("John Koroma","Male","076111111","Hilltop Zone A","Active","2026-01-01"),
("Mariama Kamara","Female","076111112","Hilltop Zone B","Pending","2026-01-02"),
("Ibrahim Conteh","Male","076111113","Hilltop Zone C","Active","2026-01-03"),
("Fatmata Bangura","Female","076111114","Hilltop Zone A","Inactive","2026-01-04"),
("Mohamed Sesay","Male","076111115","Hilltop Zone B","Active","2026-01-05")
]

cursor.executemany("""
INSERT INTO records
(full_name, gender, phone, address, status, created_date)
VALUES (?, ?, ?, ?, ?, ?)
""", records)

conn.commit()
conn.close()

print("Database Created Successfully")