from Person import Student

class Course:
    def __init__(self, course_id, course_name, instructor):
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = []

    def add_student(self, student):
        if not isinstance(student, Student):
            print("Invalid student. Addition failed.")
            return False
        
        if student in self.enrolled_students:
            print(f"{student.name} is already enrolled in {self.course_name}.")
            return False
        
        self.enrolled_students.append(student)
        print(f"{student.name} has been added to the course {self.course_name}.")
        return True
    
    
    