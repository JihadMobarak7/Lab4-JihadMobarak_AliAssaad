import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def setup_treeview(root, columns, column_names, column_widths=None):
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col, name in zip(columns, column_names):
        width = column_widths.get(col, 100) if column_widths else 100
        tree.heading(col, text=name)
        tree.column(col, width=width)
    tree.pack(expand=True, fill=tk.BOTH, side='left')

    # Adding scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    scrollbar.pack(side='right', fill='y')
    tree.configure(yscrollcommand=scrollbar.set)

    return tree

def delete_record(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("No Selection", "Please select a record to delete.")
        return
    for selected_item in selected_items:
        tree.delete(selected_item)
    messagebox.showinfo("Operation Complete", "Selected records have been deleted.")

def edit_record(tree, name_var, age_var, email_var, id_var):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showinfo("Edit Action", "No item selected for editing.")
        return

    selected_item = selected_items[0]
    item_data = tree.item(selected_item, "values")
    
    # Add debugging to check the contents of item_data
    print("Attempting to edit with data:", item_data)
    
    if len(item_data) >= 4:
        name_var.set(item_data[0])
        age_var.set(item_data[1])
        email_var.set(item_data[2])
        id_var.set(item_data[3])
        messagebox.showinfo("Operation Complete", "Fields updated for editing.")
    else:
        messagebox.showerror("Data Error", "Selected item does not contain sufficient data.")

def populate_treeview(tree, data):
    """Populate the treeview widget with data."""
    for item in data:
        tree.insert('', 'end', values=item)