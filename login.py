from tkinter import *
from tkinter import messagebox

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "admin123":
        messagebox.showinfo("Success", "Login Successful")

    else:
        messagebox.showerror("Error", "Invalid Username or Password")


root = Tk()
root.title("Hilltop Community Record Management System")
root.geometry("800x500")
root.configure(bg="#f0f4f7")

title = Label(
    root,
    text="HILLTOP COMMUNITY RECORD MANAGEMENT SYSTEM",
    font=("Arial", 18, "bold"),
    bg="#f0f4f7"
)
title.pack(pady=20)

subtitle = Label(
    root,
    text="Login to Continue",
    font=("Arial", 12),
    bg="#f0f4f7"
)
subtitle.pack()

frame = Frame(root, bg="white", bd=2, relief="solid")
frame.pack(pady=40)

Label(frame, text="Username", font=("Arial", 12), bg="white").grid(row=0, column=0, padx=20, pady=15)

username_entry = Entry(frame, width=30, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=20)

Label(frame, text="Password", font=("Arial", 12), bg="white").grid(row=1, column=0, padx=20, pady=15)

password_entry = Entry(frame, show="*", width=30, font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=20)

Button(
    root,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    width=20,
    bg="green",
    fg="white",
    command=login
).pack()

root.mainloop()
