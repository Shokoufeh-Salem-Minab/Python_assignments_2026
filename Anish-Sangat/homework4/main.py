# Student Gradebook
# Homework 4


import json
import os

# the JSON file
FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gradebook.json")


#Custom exceptions 

class GradeError(Exception):
    """Raised when a grade is not between 0 and 20."""
    pass


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""
    pass


#Student classes

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}          
        self.passing_grade = 10

    def add_grade(self, course, grade):
        # check that the grade is between 0 and 20
        if not (0 <= grade <= 20):
            raise GradeError("Grade must be between 0 and 20.")
        self.grades[course] = grade

    def average(self):
        if len(self.grades) == 0:
            return 0
        total = sum(self.grades.values())
        return total / len(self.grades)

    def best_course(self):
        # returns a tuple (course, grade)
        if len(self.grades) == 0:
            return ("None", 0)
        best = max(self.grades, key=self.grades.get)
        return (best, self.grades[best])

    def is_failing(self):
        # a student with no grades is not counted as failing
        if len(self.grades) == 0:
            return False
        return self.average() < self.passing_grade

    def to_dict(self):
        return {
            "type": "regular",
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    def __str__(self):
        course, grade = self.best_course()   # tuple unpacking
        text = "ID: " + self.student_id + " | Name: " + self.name
        text += " | Average: " + str(round(self.average(), 2))
        text += " | Best course: " + course + " (" + str(grade) + ")"
        return text


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
        text = super().__str__()
        text += " | Thesis: " + self.thesis_title
        return text


# Gradebook class
class Gradebook:
    def __init__(self):
        self.students = {}        # {student_id: Student}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("This student ID already exists.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError("Student ID " + student_id + " was not found.")
        return self.students[student_id]

    def all_courses(self):
        # set of unique course names from all students
        courses = set()
        for student in self.students.values():
            for course in student.grades:
                courses.add(course)
        return courses

    def common_courses(self, id1, id2):
        student1 = self.get_student(id1)
        student2 = self.get_student(id2)
        set1 = set(student1.grades.keys())
        set2 = set(student2.grades.keys())
        return set1 & set2        # intersection

    def ranking(self):
        # list comprehension + sorted with lambda
        pairs = [(s.name, s.average()) for s in self.students.values()]
        return sorted(pairs, key=lambda p: p[1], reverse=True)

    def failing_students(self):
        return [s for s in self.students.values() if s.is_failing()]

    def save(self):
        data = [s.to_dict() for s in self.students.values()]
        with open(FILE_NAME, "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            return    # first run, no file yet
        except json.JSONDecodeError:
            print("The data file is damaged. Starting with an empty gradebook.")
            return

        for item in data:
            if item["type"] == "graduate":
                student = GraduateStudent(item["student_id"], item["name"], item["thesis_title"])
            else:
                student = Student(item["student_id"], item["name"])
            student.grades = item["grades"]
            self.students[student.student_id] = student


# Functions for the menu 

def read_grade():
    text = input("Grade (0-20): ")
    try:
        grade = float(text)
    except ValueError:
        raise ValueError("The grade must be a number.")
    return grade


def add_student_option(gradebook):
    # keep asking until the ID is not empty and not already used
    student_id = input("Student ID: ").strip()
    while student_id == "" or student_id in gradebook.students:
        if student_id == "":
            print("ID cannot be empty.")
        else:
            print("This student ID already exists. Try another one.")
        student_id = input("Student ID: ").strip()

    # keep asking until the name is not empty
    name = input("Student name: ").strip()
    while name == "":
        print("Name cannot be empty.")
        name = input("Student name: ").strip()

    # keep asking until the answer is y or n
    kind = input("Graduate student? (y/n): ").strip().lower()
    while kind != "y" and kind != "n":
        print("Please type y or n.")
        kind = input("Graduate student? (y/n): ").strip().lower()

    if kind == "y":
        thesis = input("Thesis title: ").strip()
        student = GraduateStudent(student_id, name, thesis)
    else:
        student = Student(student_id, name)

    gradebook.add_student(student)
    print("Student added.")


def add_grade_option(gradebook):
    student_id = input("Student ID: ").strip()
    student = gradebook.get_student(student_id)
    course = input("Course name: ").strip().title()
    if course == "":
        print("Course name cannot be empty.")
        return
    grade = read_grade()
    student.add_grade(course, grade)
    print("Grade saved.")


def show_all_option(gradebook):
    if len(gradebook) == 0:
        print("There are no students yet.")
        return
    print("Number of students:", len(gradebook))
    for student in gradebook.students.values():
        print(student)
    print("Courses offered:", sorted(gradebook.all_courses()))


def show_ranking_option(gradebook):
    if len(gradebook) == 0:
        print("There are no students yet.")
        return
    place = 1
    for name, average in gradebook.ranking():
        print(str(place) + ". " + name + " - " + str(round(average, 2)))
        place += 1


def show_failing_option(gradebook):
    failing = gradebook.failing_students()
    if len(failing) == 0:
        print("No failing students.")
        return
    for student in failing:
        print(student)


def show_common_option(gradebook):
    id1 = input("First student ID: ").strip()
    id2 = input("Second student ID: ").strip()
    common = gradebook.common_courses(id1, id2)
    if len(common) == 0:
        print("These students have no courses in common.")
    else:
        print("Common courses:", sorted(common))


def show_menu():
    print()
    print("!!! Student Gradebook !!!")
    print("1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")


#Main program 

def main():
    gradebook = Gradebook()
    gradebook.load()

    running = True
    while running:
        show_menu()
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_student_option(gradebook)
            elif choice == "2":
                add_grade_option(gradebook)
            elif choice == "3":
                show_all_option(gradebook)
            elif choice == "4":
                show_ranking_option(gradebook)
            elif choice == "5":
                show_failing_option(gradebook)
            elif choice == "6":
                show_common_option(gradebook)
            elif choice == "7":
                gradebook.save()
                print("Data saved to", FILE_NAME)
                running = False
            else:
                print("Please choose a number from 1 to 7.")
        except GradeError as error:
            print("Grade error:", error)
        except StudentNotFoundError as error:
            print("Student error:", error)
        except ValueError as error:
            print("Input error:", error)


main()
