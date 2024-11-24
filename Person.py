import re

class InvalidEmailError(ValueError):
    """Custom exception for invalid email formats."""
    pass

class InvalidAgeError(ValueError):
    """Custom exception for invalid age values."""
    pass

class Person:
    def __init__(self, name, age, email):
        if not name:
            raise ValueError("Name cannot be empty.")
        self.name = name
        self.age = age
        self.email = email

    def introduce(self):
        """Introduce the person with their name and age."""
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise InvalidEmailError(f"Invalid email format: {value}")
        self._email = value

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise InvalidAgeError("Age cannot be negative.")
        self._age = value

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.registered_courses = []

    def register_course(self, course):
        """Register the student for a course if not already registered."""
        if course and hasattr(course, 'course_name') and course not in self.registered_courses:
            self.registered_courses.append(course)
            print(f"Registered for {course.course_name}")
        else:
            print("Invalid course provided or already registered.")

    def list_courses(self):
        """List all courses the student is registered for."""
        return [course.course_name for course in self.registered_courses]

class Instructor(Person):
    def __init__(self, name, age, email, instructor_id):
        super().__init__(name, age, email)
        self.instructor_id = instructor_id
        self.assigned_courses = []

    def assign_course(self, course):
        """Assign a course to the instructor if not already assigned."""
        if course and hasattr(course, 'course_name') and course not in self.assigned_courses:
            self.assigned_courses.append(course)
            print(f"Assigned to teach {course.course_name}")
        else:
            print("Invalid course provided or already assigned.")

    def list_courses(self):
        """List all courses the instructor is assigned to."""
        return [course.course_name for course in self.assigned_courses]