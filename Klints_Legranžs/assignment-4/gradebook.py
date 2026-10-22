import json
from student import Student, GraduateStudent

class Gradebook:

    def __init__(self):
        self.students = {}
        self.courses = set()


    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError(f"Student ID {student.student_id} already exists.")

        self.students[student.student_id] = student
        self.courses.update(student.grades.keys())

    
    def get_student(self, student_id):
        try:
            return self.students[student_id]
        except KeyError:
            raise KeyError(f"Student ID {student_id} was not found.")

    
    def add_grade(self, student_id, course, grade):
        student = self.get_student(student_id)

        student.add_grade(course, grade)
        self.courses.add(course.strip())

    
    def ranking(self):
        graded_students = [
            student for student in self.students.values()
            if student.average_grade() is not None
        ]

        return sorted(
            graded_students,
            key = lambda student: student.average_grade(),
            reverse = True
        )


    def failing_student(self):
        return [
            student for student in self.students.values()
            if student.is_failing()
        ]

    
    def common_course(self, first_id, second_id):
        first = self.get_student(first_id)
        second = self.get_student(second_id)

        return set(first.grades.keys()) & set(second.grades.keys())

    
    def __len__(self):
        return len(self.students)

    def save(self, filename = "gradebook.json"):
        data = [
            student.to_dict()
            for student in self.students.values()
        ]

        with open(filename, "w", encoding = "utf-8") as file:
            json.dump(data, file, indent = 4)

    
    def load(self, filename = "gradebook.json"):
        try:
            with open(filename, "r", encoding = "utf-8") as file:
                data = json.load(file)
        
        except FileNotFoundError:
            return
        
        except json.JSONDecodeError:
            print("Error: The save file contains invalid JSON.")
            return

        for item in data:
            if item["type"] == "graduate":
                student = GraduateStudent(
                    item["student_id"],
                    item["name"],
                    item["thesis_title"]
                )
            else:
                student = Student(
                    item["student_id"],
                    item["name"]
                )

            student.grades = item["grades"]
            self.add_student(student)
