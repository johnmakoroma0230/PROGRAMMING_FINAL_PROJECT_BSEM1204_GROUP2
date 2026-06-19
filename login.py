from tkinter import *
from tkinter import messagebox
import os

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == "lucian" and password == "lucian123":

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        root.destroy()

        os.system("py dashboard.py")

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )


root = Tk()

root.title("Hilltop Community Login")
root.geometry("400x250")

Label(
    root,
    text="Username"
).pack(pady=10)

username_entry = Entry(root,width=30)
username_entry.pack()

Label(
    root,
    text="Password"
).pack(pady=10)

password_entry = Entry(root,width=30,show="*")
password_entry.pack()

Button(
    root,
    text="Login",
    width=15,
    command=login
).pack(pady=20)

root.mainloop()