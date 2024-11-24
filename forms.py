import tkinter as tk
import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def add_student_form(root, callback):
    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1)

    tk.Label(frame, text="Age:").grid(row=1, column=0)
    age_entry = tk.Entry(frame)
    age_entry.grid(row=1, column=1)

    tk.Label(frame, text="Email:").grid(row=2, column=0)
    email_entry = tk.Entry(frame)
    email_entry.grid(row=2, column=1)

    tk.Label(frame, text="Student ID:").grid(row=3, column=0)
    id_entry = tk.Entry(frame)
    id_entry.grid(row=3, column=1)

    error_label = tk.Label(frame, text="", fg="red")
    error_label.grid(row=5, columnspan=2)

    def on_submit():
        name = name_entry.get()
        email = email_entry.get()
        student_id = id_entry.get()

        try:
            age = int(age_entry.get())
        except ValueError:
            error_label.config(text="Age must be a number")
            return

        if not validate_email(email):
            error_label.config(text="Invalid email format")
            return

        callback(name, age, email, student_id)
        error_label.config(text="")  # Clear error message
        # Clear form fields
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)

    submit_btn = tk.Button(frame, text="Submit", command=on_submit)
    submit_btn.grid(row=4, columnspan=2)

    # Return the frame and the entry widgets
    return frame, name_entry, age_entry, email_entry, id_entry