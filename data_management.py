import csv
import json
from tkinter import messagebox
from treeview_display import populate_treeview

def object_serializer(obj):
    if hasattr(obj, "__dict__"):
        obj_dict = obj.__dict__.copy()  # Create a shallow copy of the dictionary
        # Avoid serializing properties that can cause circular references
        circular_refs = ['instructor', 'enrolled_students', 'registered_courses']

        for key in circular_refs:
            if key in obj_dict:
                # Replace circular reference properties with a placeholder (like a name or ID)
                if isinstance(obj_dict[key], list):
                    obj_dict[key] = [str(element) for element in obj_dict[key]]  # Serialize list elements as strings
                else:
                    obj_dict[key] = str(obj_dict[key])  # Serialize as a string identifier

        # Recursively serialize objects in the dictionary
        for key, value in obj_dict.items():
            if hasattr(value, "__dict__"):
                obj_dict[key] = object_serializer(value)
            elif isinstance(value, list):
                # If it's a list, apply serialization to each element if necessary
                obj_dict[key] = [object_serializer(item) if hasattr(item, "__dict__") else item for item in value]

        return obj_dict
    raise TypeError(f"Type {type(obj)} is not serializable")

def save_data(filename, tree):
    try:
        # Collect simple data from the treeview (assume all data is in 'values' form)
        data = [tree.item(row_id)['values'] for row_id in tree.get_children()]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        
        print("Data saved successfully.")
    except Exception as e:
        print(f"Failed to save data: {str(e)}")
        messagebox.showerror("Save Failed", f"Failed to save data: {str(e)}")

def load_data(filename, tree):
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        populate_treeview(tree, data)
    except FileNotFoundError:
        print(f"Warning: No data file found at {filename}. Creating a new file.")
        open(filename, 'a').close()  # Create the file if it doesn't exist
    except json.JSONDecodeError:
        print(f"Error: Data file {filename} is corrupt. Starting with an empty dataset.")

def export_to_csv(filename, tree):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Extract the headings directly from the Treeview
            headers = [tree.heading(col)['text'] for col in tree['columns']]
            writer.writerow(headers)
            # Extract row data from Treeview
            for child in tree.get_children():
                row_data = [tree.item(child, 'values')[i] for i in range(len(tree['columns']))]
                writer.writerow(row_data)
        messagebox.showinfo("Export Success", "Data exported to CSV successfully.")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Failed to export data: {str(e)}")