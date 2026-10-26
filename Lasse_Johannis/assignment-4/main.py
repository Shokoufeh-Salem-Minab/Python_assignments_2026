# Homework 4 - Student Gradebook
# Lasse Johannis

import json

data_file = "gradebook.json"


# ----- custom exceptions -----
class InvalidGradeError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


# ----- classes -----
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  # {course: grade}
        self.passing_grade = 10

    def add_grade(self, course, grade):
        if grade < 0 or grade > 20:
            raise InvalidGradeError()
        self.grades[course] = grade

    def average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        return 0

    # returns the best course as a tuple (course, grade)
    def best_course(self):
        best = ""
        best_grade = -1
        for course, grade in self.grades.items():
            if grade > best_grade:
                best = course
                best_grade = grade
        return (best, best_grade)

    def is_failing(self):
        return self.average() < self.passing_grade

    def to_dict(self):
        return {"type": "regular", "name": self.name, "grades": self.grades}

    def __str__(self):
        return f"{self.student_id} - {self.name}, average: {round(self.average(), 2)}, grades: {self.grades}"


class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title
        self.passing_grade = 14

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "graduate"
        data["thesis_title"] = self.thesis_title
        return data

    def __str__(self):
        return super().__str__() + f", thesis: {self.thesis_title} (graduate)"


class Gradebook:
    def __init__(self):
        self.students = {}  # {student_id: Student}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError()
        return self.students[student_id]

    # set of all unique courses across all students
    def all_courses(self):
        courses = set()
        for student in self.students.values():
            for course in student.grades:
                courses.add(course)
        return courses

    def common_courses(self, id1, id2):
        student1 = self.get_student(id1)
        student2 = self.get_student(id2)
        return set(student1.grades.keys()) & set(student2.grades.keys())

    # students with grades, highest average first
    def ranking(self):
        graded = [student for student in self.students.values() if student.grades]
        return sorted(graded, key=lambda student: student.average(), reverse=True)

    def failing_students(self):
        return [student for student in self.students.values() if student.grades and student.is_failing()]

    def save(self, filename):
        data = {student_id: student.to_dict() for student_id, student in self.students.items()}
        with open(filename, "w") as f:
            f.write(json.dumps(data))

    def load(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            print("No saved data found. Starting with an empty gradebook.")
            return
        except ValueError:
            print("Saved data is damaged. Starting with an empty gradebook.")
            return
        for student_id, info in data.items():
            if info["type"] == "graduate":
                student = GraduateStudent(student_id, info["name"], info["thesis_title"])
            else:
                student = Student(student_id, info["name"])
            student.grades = info["grades"]
            self.add_student(student)


# ----- menu functions -----
def add_student(gradebook):
    student_id = input("Enter student ID: ")
    if student_id == "":
        print("Error: student ID cannot be empty.")
        return
    if student_id in gradebook.students:
        print("Error: student ID", student_id, "already exists.")
        return
    name = input("Enter student name: ")
    kind = input("Regular or graduate student? (r/g): ")
    if kind == "r":
        gradebook.add_student(Student(student_id, name))
    elif kind == "g":
        thesis_title = input("Enter thesis title: ")
        gradebook.add_student(GraduateStudent(student_id, name, thesis_title))
    else:
        print("Error: please enter r or g.")
        return
    print("Student", name, "added.")


def add_grade(gradebook):
    try:
        student = gradebook.get_student(input("Enter student ID: "))
        course = input("Enter course name: ")
        if course == "":
            print("Error: course name cannot be empty.")
            return
        grade = float(input("Enter grade (0-20): "))
        student.add_grade(course, grade)
        print("Grade saved:", student.name, "-", course, "-", grade)
    except StudentNotFoundError:
        print("Error: unknown student ID.")
    except ValueError:
        print("Error: grade must be a number.")
    except InvalidGradeError:
        print("Error: grade must be between 0 and 20.")


def show_all_students(gradebook):
    print("\n========== ALL STUDENTS ==========")
    if len(gradebook) == 0:
        print("No students yet.")
        return
    for student in gradebook.students.values():
        print(student)
        if student.grades:
            course, grade = student.best_course()
            print("   Best course:", course, "-", grade)
    print()
    print("Number of students:", len(gradebook))
    print("Courses offered:", gradebook.all_courses())


def show_ranking(gradebook):
    print("\n========== RANKING ==========")
    ranking = gradebook.ranking()
    if len(ranking) == 0:
        print("No grades yet.")
        return
    place = 1
    for student in ranking:
        print(str(place) + ".", student.name, "-", round(student.average(), 2))
        place += 1


def show_failing(gradebook):
    print("\n========== FAILING STUDENTS ==========")
    failing = gradebook.failing_students()
    if len(failing) == 0:
        print("No failing students.")
        return
    for student in failing:
        print(student.name, "- average", round(student.average(), 2), "- needs", student.passing_grade)


def show_common_courses(gradebook):
    try:
        id1 = input("Enter first student ID: ")
        id2 = input("Enter second student ID: ")
        common = gradebook.common_courses(id1, id2)
    except StudentNotFoundError:
        print("Error: unknown student ID.")
        return
    if len(common) == 0:
        print("These students have no common courses.")
    else:
        print("Common courses:", common)


def show_menu():
    print("\n========== STUDENT GRADEBOOK ==========")
    print("1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")


gradebook = Gradebook()
gradebook.load(data_file)
print("Students loaded:", len(gradebook))

running = True
while running:
    show_menu()
    choice = input("Enter your choice: ")

    if choice == "1":
        add_student(gradebook)
    elif choice == "2":
        add_grade(gradebook)
    elif choice == "3":
        show_all_students(gradebook)
    elif choice == "4":
        show_ranking(gradebook)
    elif choice == "5":
        show_failing(gradebook)
    elif choice == "6":
        show_common_courses(gradebook)
    elif choice == "7":
        gradebook.save(data_file)
        print("Data saved to", data_file + ". Goodbye!")
        running = False
    else:
        print("Invalid choice. Please enter a number from 1 to 7.")
