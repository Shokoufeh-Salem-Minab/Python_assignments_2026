# Homework 4
# Srivishva Melvin - sm25017
# Program created on: 18/10/2026

import json

DATA_FILE = "gradebook.json"

class GradebookError(Exception):
    pass

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}
        self.passing_grade = 10

    def set_grade(self, course, grade):
        if grade >= 0 and grade <= 20:
            self.grades[course] = grade
        else:
            raise GradebookError("Grade must be between 0 and 20.")

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def is_passing(self):
        for course in self.grades:
            if self.grades[course] < self.passing_grade:
                return False
        return True

    def best_course(self):
        if len(self.grades) == 0:
            return None
        bestCourse = None
        best_grade = -1
        for course in self.grades:
            if self.grades[course] > best_grade:
                bestCourse = course
                best_grade = self.grades[course]
        return (bestCourse, best_grade)

    def grades_text(self):
        if len(self.grades) == 0:
            return "no grades yet"
        parts = []
        for course in self.grades:
            parts.append(course + ": " + str(self.grades[course]))
        return ", ".join(parts)

    def to_dict(self): # into a dictionary for saving to JSON
        return {
            "type": "student",
            "id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    def __str__(self):
        return f"[{self.student_id}] {self.name} (Student) - average: {round(self.average(), 2)} - {self.grades_text()}"

class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.passing_grade = 14
        self.thesis_title = thesis_title

    def to_dict(self):
        return {
            "type": "graduate",
            "id": self.student_id,
            "name": self.name,
            "grades": self.grades,
            "thesis_title": self.thesis_title
        }

    def __str__(self):
        return f"[{self.student_id}] {self.name} (Graduate) - average: {round(self.average(), 2)} - {self.grades_text()} - thesis: {self.thesis_title}"

def student_from_dict(data): # builds a student or a graduate student from saved data
    if data["type"] == "graduate":
        student = GraduateStudent(data["id"], data["name"], data["thesis_title"])
    else:
        student = Student(data["id"], data["name"])

    for course in data["grades"]:
        student.set_grade(course, data["grades"][course])
    return student

class Gradebook:
    def __init__(self):
        self.students = {}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise GradebookError("A student with ID " + student.student_id + " already exists")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise GradebookError("No student with ID " + student_id)
        return self.students[student_id]

    def all_courses(self):
        courses = set()
        for student in self.students.values():
            courses.update(student.grades.keys())
        return courses

    def common_courses(self, id1, id2):
        first = self.get_student(id1)
        second = self.get_student(id2)
        return set(first.grades) & set(second.grades)

    def ranking(self):
        graded = [s for s in self.students.values() if len(s.grades) > 0]
        return sorted(graded, key=lambda s: s.average(), reverse=True)

    def failing_students(self):
        failing = [s for s in self.students.values() if len(s.grades) > 0 and not s.is_passing()]
        return sorted(failing, key=lambda s: s.average())

    def save(self, filename):
        data = []
        for student in self.students.values():
            data.append(student.to_dict())
        with open(filename, "w") as f:
            f.write(json.dumps(data, indent=2))

    def load(self, filename):
        try:
            with open(filename) as f:
                data = json.loads(f.read())
            for item in data:
                self.add_student(student_from_dict(item))
        except FileNotFoundError: # for first run, as there is no file yet so start empty
            pass 
        except (ValueError, KeyError, TypeError, AttributeError, GradebookError):
            print("Warning: the data file is damaged, starting with an empty gradebook")
            self.students = {}

def input_check(text):
    userInput = input(text).strip()
    if userInput == "":
        raise GradebookError("This field cannot be empty")
    return userInput

def show_menu():
    print("\nStudent Gradebook: ")
    print("1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking (highest to lowest average)")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")

def add_student_option(gradebook):
    kind = input("Regular or graduate student? (r/g): ").strip().lower()
    if kind != "r" and kind != "g":
        raise GradebookError("Please type r (for regular student) or g (for graduate student)")
    studentID = input_check("Student ID: ").upper() 
    name = input_check("Name: ")
    if kind == "g":
        thesis = input_check("Thesis title: ")
        student = GraduateStudent(studentID, name, thesis)
    else:
        student = Student(studentID, name)
    gradebook.add_student(student)
    print("Added:", student)

def grade_option(gradebook):
    student = gradebook.get_student(input_check("Student ID: ").upper())
    course = input_check("Course name: ").title()
    grade = float(input("Enter grade (0-20): ").strip())
    present_grade = course in student.grades
    student.set_grade(course, grade)
    if present_grade:
        print("Grade updated.")
    else:
        print("Grade added.")

def print_student(student):
    print(student)
    best = student.best_course()
    if best is not None:
        course, grade = best 
        print("Best course:", course, "(Grade:", str(grade) + ")")

def show_students_option(gradebook):
    if len(gradebook) == 0:
        print("There are no students")
        return
    print("Number of students:", len(gradebook))
    for student in gradebook.students.values():
        print_student(student)
    courses = sorted(gradebook.all_courses())
    if len(courses) > 0:
        print("Courses offered:", ", ".join(courses))

def ranking_option(gradebook):
    ranked = gradebook.ranking()
    if len(ranked) == 0:
        print("No grades have been entered")
        return
    rank = 1
    for student in ranked:
        print(f"{rank}. {student.name} ({student.student_id}) - average: {round(student.average(), 2)}")
        rank += 1

def failing_option(gradebook):
    failing = gradebook.failing_students()
    if len(failing) == 0:
        print("No failing students")
        return
    for student in failing:
        low = []
        for course in student.grades:
            if student.grades[course] < student.passing_grade:
                low.append(course + ": " + str(student.grades[course]))
        print(f"{student.name} ({student.student_id}) - below {student.passing_grade}: " + ", ".join(low))

def common_option(gradebook):
    id1 = input_check("First student ID: ").upper()
    id2 = input_check("Second student ID: ").upper()
    common = gradebook.common_courses(id1, id2)
    if len(common) == 0:
        print("These students have no courses in common")
    else:
        print("Common courses:", ", ".join(sorted(common)))

def save_data(gradebook):
    try:
        gradebook.save(DATA_FILE)
    except OSError:
        print("Could not save the data file")
        return False
    print("Data saved to", DATA_FILE)
    return True

def run_option(choice, gradebook):
    if choice == "1":
        add_student_option(gradebook)
    elif choice == "2":
        grade_option(gradebook)
    elif choice == "3":
        show_students_option(gradebook)
    elif choice == "4":
        ranking_option(gradebook)
    elif choice == "5":
        failing_option(gradebook)
    elif choice == "6":
        common_option(gradebook)
    else:
        print("Enter a number from 1 to 7")

def main():
    gradebook = Gradebook()
    gradebook.load(DATA_FILE)
    print("Loaded", len(gradebook), "student(s) from", DATA_FILE)
    running = True
    while running:
        show_menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "7":
                if save_data(gradebook):
                    running = False
            else:
                run_option(choice, gradebook)
        except GradebookError as error:
            print("Error:", error)
        except ValueError:
            print("Error: please enter a valid number.")

if __name__ == "__main__":
    main()