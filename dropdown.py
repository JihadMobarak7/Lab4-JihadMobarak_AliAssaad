import tkinter as tk

def setup_dropdown(frame, label_text, choices, callback):
    # Create a label for the dropdown
    label = tk.Label(frame, text=label_text, font=('Helvetica', 10, 'bold'))
    label.pack(side=tk.LEFT, padx=(0, 10))  # Add some padding for visual separation

    # Define a variable to hold the current selection
    var = tk.StringVar(frame)
    var.set(choices[0] if choices else 'No options available')

    # Create the dropdown menu
    dropdown = tk.OptionMenu(frame, var, *choices if choices else ['No options available'])
    dropdown.config(width=15, font=('Helvetica', 10), state='normal' if choices else 'disabled')
    dropdown.pack(side=tk.LEFT)

    # Function to update the dropdown choices dynamically
    def update_choices(new_choices):
        dropdown['menu'].delete(0, 'end')
        if new_choices:
            for choice in new_choices:
                dropdown['menu'].add_command(label=choice, command=lambda choice=choice: var.set(choice))
            var.set(new_choices[0])
            dropdown.config(state='normal')
        else:
            dropdown['menu'].add_command(label='No options available')
            var.set('No options available')
            dropdown.config(state='disabled')

    # Attach the update function to the dropdown object
    dropdown.update_choices = update_choices

    # Setup a trace callback to react to changes in selection
    var.trace('w', lambda *args: callback(var.get()))

    # Accessibility improvements:
    # Keyboard focus configuration
    dropdown.bind("<Enter>", lambda e: dropdown.focus_set())

    # Tooltip for additional context
    tooltip = tk.Label(frame, text=f"Select a {label_text.lower()[:-1]}", bg='yellow', font=('Helvetica', 8), wraplength=150)
    dropdown.bind("<Enter>", lambda e: tooltip.place(x=dropdown.winfo_x(), y=dropdown.winfo_y() + 30))
    dropdown.bind("<Leave>", lambda e: tooltip.place_forget())

    return var, dropdown