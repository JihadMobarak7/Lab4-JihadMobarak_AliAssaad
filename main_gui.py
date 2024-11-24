import tkinter as tk
from tkinter import ttk, messagebox
import re

if __name__ == "__main__" and __package__ is None:
    import os, sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "source"

from .data_management import save_data, export_to_csv
from .forms import add_student_form
from .dropdown import setup_dropdown
from .treeview_display import edit_record, setup_treeview, delete_record

def submit_student_data(tree, name, age, email, student_id):
    """
    Attempts to submit student data into the system and save it to a JSON file.
    
    :param tree: The treeview object where the student data is displayed.
    :param str name: The name of the student.
    :param int age: The age of the student.
    :param str email: The email address of the student.
    :param str student_id: The unique identifier for the student.
    
    :returns: None
    """
    if not validate_unique_id(tree, student_id):
        messagebox.showerror("Duplicate Entry", "This student ID already exists.")
        return
    if not validate_email(email):
        messagebox.showerror("Invalid Email", "Invalid email address")
        return
    if not validate_age(age):
        return  # Error message handled within the function

    tree.insert('', 'end', values=(name, "Student", "Not Assigned"))
    save_data("data.json", tree)

def validate_unique_id(tree, student_id):
    """
    Validates that the student ID does not already exist within the system.
    
    :param tree: The treeview object where student data is stored.
    :param str student_id: The student ID to check for uniqueness.
    
    :returns: bool - True if unique, False otherwise.
    """
    existing_ids = []
    for item in tree.get_children():
        item_data = tree.item(item, "values")
        if len(item_data) > 3:
            existing_ids.append(item_data[3])
    return student_id not in existing_ids

def validate_email(email):
    """
    Validates the format of the email address using a regular expression.
    
    :param str email: The email address to validate.
    
    :returns: bool - True if the email is valid, False otherwise.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_age(age):
    """
    Validates that the age is a positive integer.
    
    :param int age: The age to validate.
    
    :returns: bool - True if the age is valid, False otherwise.
    """
    try:
        age = int(age)
        if age < 0:
            raise ValueError("Age cannot be negative")
    except ValueError as e:
        messagebox.showerror("Invalid Age", str(e))
        return False
    return True

def main():
    """
    Main function to initialize the GUI application.
    """
    root = tk.Tk()
    root.title("School Management System")
    root.geometry("800x600+100+100")
    setup_ui(root)
    root.mainloop()

def setup_ui(root):
    """
    Sets up the user interface for the application.
    
    :param root: The root window of the application.
    """
    tree = setup_treeview(root, ('Name', 'Role', 'Course Assigned'), ["Name", "Role", "Course Assigned"])
    setup_forms_and_controls(root, tree)

def setup_forms_and_controls(root, tree):
    """
    Sets up the forms and control elements within the user interface.
    
    :param root: The root window of the application.
    :param tree: The treeview object for displaying student data.
    """
    form_frame, name_var, age_var, email_var, id_var = add_student_form(root, lambda n, a, e, i: submit_student_data(tree, n, a, e, i))
    setup_dropdown_controls(root, tree)
    setup_action_buttons(root, tree, name_var, age_var, email_var, id_var)

def setup_dropdown_controls(root, tree):
    """
    Sets up dropdown controls for the application.
    
    :param root: The root window of the application.
    :param tree: The treeview object used in other controls.
    """
    courses = ["Math 101", "Science 102", "History 103", "Biology 201", "Math 201"]
    course_dropdown_frame = tk.Frame(root)
    course_dropdown_frame.pack(pady=20)
    setup_dropdown(course_dropdown_frame, "Register Student:", courses, lambda x: print(f"Student registered for {x}"))
    setup_dropdown(course_dropdown_frame, "Assign Instructor:", courses, lambda x: print(f"Instructor assigned to {x}"))

def setup_action_buttons(root, tree, name_var, age_var, email_var, id_var):
    """
    Sets up action buttons for editing, deleting, saving, and exporting data.

    :param root: The root window of the application.
    :param tree: The treeview where the data is displayed.
    :param name_var: Variable associated with student's name input.
    :param age_var: Variable associated with student's age input.
    :param email_var: Variable associated with student's email input.
    :param id_var: Variable associated with student's ID input.
    """
    # Command functions
    def handle_edit():
        if tree.selection():  # Check if there's a selection
            edit_record(tree, name_var.get(), age_var.get(), email_var.get(), id_var.get())
        else:
            messagebox.showinfo("No Selection", "Please select an item to edit.")

    def handle_delete():
        if tree.selection():  # Check if there's a selection
            delete_record(tree)
        else:
            messagebox.showinfo("No Selection", "Please select an item to delete.")

    def handle_save():
        try:
            save_data("data.json", tree)
            messagebox.showinfo("Save Successful", "Data saved successfully.")
        except Exception as e:
            messagebox.showerror("Save Failed", f"Failed to save data: {str(e)}")

    def handle_export():
        try:
            export_to_csv("output.csv", tree)
            messagebox.showinfo("Export Successful", "Data exported to CSV successfully.")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export data: {str(e)}")

    # Buttons
    edit_btn = tk.Button(root, text="Edit Selected", command=handle_edit)
    delete_btn = tk.Button(root, text="Delete Selected", command=handle_delete)
    save_btn = tk.Button(root, text="Save Data", command=handle_save)
    export_btn = tk.Button(root, text="Export to CSV", command=handle_export)
    
    # Button layout
    edit_btn.pack(pady=5)
    delete_btn.pack(pady=5)
    save_btn.pack(pady=5)
    export_btn.pack(pady=5)