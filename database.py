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

("John M.A Koroma","Male","079-282227","Hilltop Zone A","Active","2026-09-01"),
("Zainab Jalloh","Female","079345623","Hilltop Zone B","Pending","2026-01-02"),
("Princess Turay","Female","076119999","Hilltop Zone C","Active","2026-01-03"),
("Fatmata Bangura","Female","076114514","Hilltop Zone A","Inactive","2026-01-04"),
("Mohamed Sesay","Male","076111115","Hilltop Zone B","Active","2026-01-05"),
("Hawa Turay","Female","076111116","Hilltop Zone C","Pending","2026-01-06"),
("Alhaji Kamara","Male","076111117","Hilltop Zone A","Active","2026-01-07"),
("Aminata Koroma","Female","076111118","Hilltop Zone B","Active","2026-01-08"),
("Abdul Bangura","Male","076111119","Hilltop Zone C","Inactive","2026-01-09"),
("Kadiatu Conteh","Female","076111120","Hilltop Zone A","Active","2026-01-10"),

("David Johnson","Male","076111121","Hilltop Zone B","Pending","2026-01-11"),
("Sarah Williams","Female","076111122","Hilltop Zone C","Active","2026-01-12"),
("Joseph Tucker","Male","076111123","Hilltop Zone A","Active","2026-01-13"),
("Martha Jones","Female","076111124","Hilltop Zone B","Inactive","2026-01-14"),
("Samuel Kanu","Male","076111125","Hilltop Zone C","Active","2026-01-15"),
("Rugiatu Sesay","Female","076111126","Hilltop Zone A","Pending","2026-01-16"),
("Abubakarr Kamara","Male","076111127","Hilltop Zone B","Active","2026-01-17"),
("Adama Bangura","Female","076111128","Hilltop Zone C","Active","2026-01-18"),
("Mustapha Koroma","Male","076111129","Hilltop Zone A","Inactive","2026-01-19"),
("Isatu Conteh","Female","076111130","Hilltop Zone B","Active","2026-01-20")

]

cursor.executemany("""
INSERT INTO records
(full_name, gender, phone, address, status, created_date)
VALUES (?, ?, ?, ?, ?, ?)
""", records)

conn.commit()
conn.close()

print("20 Records Added Successfully")