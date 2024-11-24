import sys
import json
import csv
import re
import sqlite3
import shutil 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QInputDialog



class SchoolManagementSystem(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("School Management System")
        self.setGeometry(100, 100, 600, 600)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

 
        layout = QVBoxLayout()


        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()


        self.create_tables()


        self.student_label = QLabel("Add Student")
        layout.addWidget(self.student_label)

        self.student_name_input = QLineEdit(self)
        self.student_name_input.setPlaceholderText("Student Name")
        layout.addWidget(self.student_name_input)

        self.student_id_input = QLineEdit(self)
        self.student_id_input.setPlaceholderText("Student ID")
        layout.addWidget(self.student_id_input)

        self.student_email_input = QLineEdit(self)
        self.student_email_input.setPlaceholderText("Student Email")
        layout.addWidget(self.student_email_input)

        self.course_selection = QComboBox(self)
        self.course_selection.addItem("Select Course")
        layout.addWidget(self.course_selection)

        self.add_student_button = QPushButton("Add Student", self)
        self.add_student_button.clicked.connect(self.add_student)
        layout.addWidget(self.add_student_button)

        # ------------------- Instructor Form -------------------
        self.instructor_label = QLabel("Add Instructor")
        layout.addWidget(self.instructor_label)

        self.instructor_name_input = QLineEdit(self)
        self.instructor_name_input.setPlaceholderText("Instructor Name")
        layout.addWidget(self.instructor_name_input)

        self.instructor_id_input = QLineEdit(self)
        self.instructor_id_input.setPlaceholderText("Instructor ID")
        layout.addWidget(self.instructor_id_input)

        self.instructor_email_input = QLineEdit(self)
        self.instructor_email_input.setPlaceholderText("Instructor Email")
        layout.addWidget(self.instructor_email_input)

        self.instructor_selection = QComboBox(self)
        self.instructor_selection.addItem("Select Instructor")
        layout.addWidget(self.instructor_selection)

        self.add_instructor_button = QPushButton("Add Instructor", self)
        self.add_instructor_button.clicked.connect(self.add_instructor)
        layout.addWidget(self.add_instructor_button)


        self.course_label = QLabel("Add Course")
        layout.addWidget(self.course_label)

        self.course_name_input = QLineEdit(self)
        self.course_name_input.setPlaceholderText("Course Name")
        layout.addWidget(self.course_name_input)

        self.course_id_input = QLineEdit(self)
        self.course_id_input.setPlaceholderText("Course ID")
        layout.addWidget(self.course_id_input)

        self.add_course_button = QPushButton("Add Course", self)
        self.add_course_button.clicked.connect(self.add_course)
        layout.addWidget(self.add_course_button)

        self.show_records_button = QPushButton("Show All Records", self)
        self.show_records_button.clicked.connect(self.show_records)
        layout.addWidget(self.show_records_button)

        self.records_table = QTableWidget(self)
        self.records_table.setRowCount(10) 
        self.records_table.setColumnCount(3)
        self.records_table.setHorizontalHeaderLabels(["ID", "Name", "Role"])
        layout.addWidget(self.records_table)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Search by Name or ID")
        layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_records)
        layout.addWidget(self.search_button)

 
        self.edit_button = QPushButton("Edit Selected Record", self)
        self.edit_button.clicked.connect(self.edit_record)
        layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Selected Record", self)
        self.delete_button.clicked.connect(self.delete_record)
        layout.addWidget(self.delete_button)


        self.save_button = QPushButton("Save Data", self)
        self.save_button.clicked.connect(self.save_data)
        layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Data", self)
        self.load_button.clicked.connect(self.load_data)
        layout.addWidget(self.load_button)


        self.export_button = QPushButton("Export to CSV", self)
        self.export_button.clicked.connect(self.export_to_csv)
        layout.addWidget(self.export_button)


        self.backup_button = QPushButton("Backup Database", self)
        self.backup_button.clicked.connect(self.backup_database)
        layout.addWidget(self.backup_button)


        self.central_widget.setLayout(layout)


    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS instructors (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                instructor_id TEXT,
                FOREIGN KEY (instructor_id) REFERENCES instructors(id)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                student_id TEXT,
                course_id TEXT,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (course_id) REFERENCES courses(id)
            )
        ''')

        self.conn.commit()


    def add_student(self):
        student_name = self.student_name_input.text()
        student_id = self.student_id_input.text()
        student_email = self.student_email_input.text()

        if not student_name or not student_id or not student_email:
            QMessageBox.warning(self, "Invalid Input", "All fields must be filled.")
            return

        if not self.is_valid_email(student_email):
            QMessageBox.warning(self, "Invalid Email", "Please enter a valid email address.")
            return


        try:
            self.cursor.execute('''
                INSERT INTO students (id, name, email)
                VALUES (?, ?, ?)
            ''', (student_id, student_name, student_email))
            self.conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Student ID already exists.")
            return

        selected_course = self.course_selection.currentText()
        if selected_course != "Select Course":

            self.cursor.execute('''
                INSERT INTO registrations (student_id, course_id)
                VALUES (?, ?)
            ''', (student_id, selected_course))
            self.conn.commit()

        QMessageBox.information(self, "Success", "Student added successfully!")
        self.student_name_input.clear()
        self.student_id_input.clear()
        self.student_email_input.clear()


    def add_instructor(self):
        instructor_name = self.instructor_name_input.text()
        instructor_id = self.instructor_id_input.text()
        instructor_email = self.instructor_email_input.text()

        try:
            self.cursor.execute('''
                INSERT INTO instructors (id, name, email)
                VALUES (?, ?, ?)
            ''', (instructor_id, instructor_name, instructor_email))
            self.conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Instructor ID already exists.")
            return


        self.instructor_selection.addItem(instructor_name)
        self.instructor_name_input.clear()
        self.instructor_id_input.clear()
        self.instructor_email_input.clear()

    def add_course(self):
        course_name = self.course_name_input.text()
        course_id = self.course_id_input.text()
        selected_instructor = self.instructor_selection.currentText()

        try:
            self.cursor.execute('''
                INSERT INTO courses (id, name, instructor_id)
                VALUES (?, ?, ?)
            ''', (course_id, course_name, selected_instructor))
            self.conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Course ID already exists.")
            return


        self.course_selection.addItem(course_name)
        self.course_name_input.clear()
        self.course_id_input.clear()


    def show_records(self):
        self.records_table.setRowCount(0) 
        self.cursor.execute('''
            SELECT students.id, students.name, "Student"
            FROM students
            UNION
            SELECT instructors.id, instructors.name, "Instructor"
            FROM instructors
        ''')

        for idx, row in enumerate(self.cursor.fetchall()):
            self.records_table.insertRow(idx)
            self.records_table.setItem(idx, 0, QTableWidgetItem(row[0]))
            self.records_table.setItem(idx, 1, QTableWidgetItem(row[1]))
            self.records_table.setItem(idx, 2, QTableWidgetItem(row[2]))


    def search_records(self):
        search_term = self.search_input.text()
        self.records_table.setRowCount(0)

        self.cursor.execute('''
            SELECT id, name, 'Student' AS role FROM students WHERE name LIKE ? OR id LIKE ?
            UNION
            SELECT id, name, 'Instructor' AS role FROM instructors WHERE name LIKE ? OR id LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

        for idx, row in enumerate(self.cursor.fetchall()):
            self.records_table.insertRow(idx)
            self.records_table.setItem(idx, 0, QTableWidgetItem(row[0]))
            self.records_table.setItem(idx, 1, QTableWidgetItem(row[1]))
            self.records_table.setItem(idx, 2, QTableWidgetItem(row[2]))


    def is_valid_email(self, email):
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        return re.match(email_regex, email)


    def edit_record(self):
        selected_row = self.records_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a record to edit.")
            return


        id_item = self.records_table.item(selected_row, 0)
        name_item = self.records_table.item(selected_row, 1)
        role_item = self.records_table.item(selected_row, 2)

        new_name, ok1 = QInputDialog.getText(self, "Edit Name", "Enter new name:", QLineEdit.Normal, name_item.text())
        new_role, ok2 = QInputDialog.getText(self, "Edit Role", "Enter new role:", QLineEdit.Normal, role_item.text())

        if ok1 and ok2:
            if new_role == "Student":
                self.cursor.execute('''
                    UPDATE students SET name = ? WHERE id = ?
                ''', (new_name, id_item.text()))
            elif new_role == "Instructor":
                self.cursor.execute('''
                    UPDATE instructors SET name = ? WHERE id = ?
                ''', (new_name, id_item.text()))
            self.conn.commit()


            self.records_table.setItem(selected_row, 1, QTableWidgetItem(new_name))
            self.records_table.setItem(selected_row, 2, QTableWidgetItem(new_role))

    def delete_record(self):
        selected_row = self.records_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No selection", "Please select a record to delete.")
            return

        id_item = self.records_table.item(selected_row, 0)
        role_item = self.records_table.item(selected_row, 2)

        confirmation = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this record?",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation == QMessageBox.Yes:
            if role_item.text() == "Student":
                self.cursor.execute('''
                    DELETE FROM students WHERE id = ?
                ''', (id_item.text(),))
            elif role_item.text() == "Instructor":
                self.cursor.execute('''
                    DELETE FROM instructors WHERE id = ?
                ''', (id_item.text(),))

            self.conn.commit()
            self.records_table.removeRow(selected_row)

 
    def save_data(self):
        data = []
        row_count = self.records_table.rowCount()

        for row in range(row_count):
            record = {
                "ID": self.records_table.item(row, 0).text(),
                "Name": self.records_table.item(row, 1).text(),
                "Role": self.records_table.item(row, 2).text()
            }
            data.append(record)

        with open("records.json", "w") as file:
            json.dump(data, file, indent=4)

        QMessageBox.information(self, "Save Data", "Data saved to records.json")


    def load_data(self):
        try:
            with open("records.json", "r") as file:
                data = json.load(file)
                self.records_table.setRowCount(0)
                for record in data:
                    row_position = self.records_table.rowCount()
                    self.records_table.insertRow(row_position)
                    self.records_table.setItem(row_position, 0, QTableWidgetItem(record["ID"]))
                    self.records_table.setItem(row_position, 1, QTableWidgetItem(record["Name"]))
                    self.records_table.setItem(row_position, 2, QTableWidgetItem(record["Role"]))
        except FileNotFoundError:
            QMessageBox.warning(self, "Load Data", "No saved data found.")

 
    def export_to_csv(self):
        data = []
        row_count = self.records_table.rowCount()

        for row in range(row_count):
            record = [
                self.records_table.item(row, 0).text(),
                self.records_table.item(row, 1).text(),  
                self.records_table.item(row, 2).text()  
            ]
            data.append(record)

        with open("records.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Role"]) 
            writer.writerows(data)

        QMessageBox.information(self, "Export to CSV", "Data exported to records.csv")


    def backup_database(self):
        try:
            shutil.copyfile('school_management.db', 'school_management_backup.db')
            QMessageBox.information(self, "Backup", "Database backup completed successfully!")
        except Exception as e:
            QMessageBox.warning(self, "Backup Failed", f"Error during backup: {e}")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SchoolManagementSystem()
    window.show()
    sys.exit(app.exec_())
