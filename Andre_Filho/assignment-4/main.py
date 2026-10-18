# Assignment 4 - Student Gradebook
# Andre Filho

import json

DATA_FILE = "gradebook.json"


class GradebookError(Exception):
    pass


class Student:
    passing_grade = 10

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    def set_grade(self, course, grade):
        if not 0 <= grade <= 20:
            raise GradebookError("Grades must be between 0 and 20.")
        self.grades[course] = grade

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        course = max(self.grades, key=self.grades.get)
        return course, self.grades[course]

    def has_passed(self):
        return self.average() >= self.passing_grade

    def to_dict(self):
        return {"id": self.student_id, "name": self.name, "grades": self.grades}

    def __str__(self):
        text = f"{self.student_id} - {self.name} (average {self.average():.2f})"
        if self.grades:
            course, grade = self.best_course()
            text += f", best course: {course} ({grade:g})"
        return text


class GraduateStudent(Student):
    passing_grade = 14

    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def to_dict(self):
        data = super().to_dict()
        data["thesis_title"] = self.thesis_title
        return data

    def __str__(self):
        return super().__str__() + f" [graduate, thesis: {self.thesis_title}]"


class Gradebook:
    def __init__(self):
        self.students = {}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise GradebookError("That student ID is already used.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        try:
            return self.students[student_id]
        except KeyError:
            raise GradebookError(f"There is no student with ID {student_id}.")

    def all_courses(self):
        courses = set()
        for student in self.students.values():
            courses.update(student.grades)
        return courses

    def common_courses(self, id1, id2):
        first = self.get_student(id1)
        second = self.get_student(id2)
        return set(first.grades) & set(second.grades)

    def ranking(self):
        ordered = sorted(self.students.values(), key=lambda s: s.average(), reverse=True)
        return [f"{place}. {s.name}: {s.average():.2f}" for place, s in enumerate(ordered, 1)]

    def failing(self):
        failed = [s for s in self.students.values() if s.grades and not s.has_passed()]
        return sorted(failed, key=lambda s: s.name)

    def save(self):
        data = [s.to_dict() for s in self.students.values()]
        with open(DATA_FILE, "w") as file:
            json.dump(data, file, indent=2)

    def load(self):
        try:
            with open(DATA_FILE) as file:
                data = json.load(file)
        except FileNotFoundError:
            return
        except json.JSONDecodeError:
            print("The data file is damaged, starting with an empty gradebook.")
            return
        try:
            for item in data:
                if "thesis_title" in item:
                    student = GraduateStudent(item["id"], item["name"], item["thesis_title"])
                else:
                    student = Student(item["id"], item["name"])
                student.grades = item["grades"]
                self.students[student.student_id] = student
        except (KeyError, TypeError):
            print("The data file is damaged, starting with an empty gradebook.")
            self.students = {}


def ask_text(message):
    text = input(message).strip()
    if text == "":
        raise GradebookError("This field cannot be empty.")
    return text


def ask_grade(message):
    try:
        return float(input(message))
    except ValueError:
        raise GradebookError("The grade must be a number.")


def add_student(book):
    kind = input("Regular (1) or graduate (2) student? ")
    if kind not in ("1", "2"):
        raise GradebookError("Please choose 1 or 2.")
    student_id = ask_text("Student ID: ")
    name = ask_text("Name: ")
    if kind == "2":
        student = GraduateStudent(student_id, name, ask_text("Thesis title: "))
    else:
        student = Student(student_id, name)
    book.add_student(student)
    print("Student added.")


def add_grade(book):
    student = book.get_student(ask_text("Student ID: "))
    course = ask_text("Course: ")
    student.set_grade(course, ask_grade("Grade (0-20): "))
    print("Grade saved.")


def show_students(book):
    if len(book) == 0:
        print("There are no students yet.")
        return
    print(f"Students: {len(book)}")
    for student in book.students.values():
        print(student)
    print("Courses offered:", ", ".join(sorted(book.all_courses())) or "none")


def show_ranking(book):
    if len(book) == 0:
        print("There are no students yet.")
    for line in book.ranking():
        print(line)


def show_failing(book):
    failed = book.failing()
    if not failed:
        print("Nobody is failing.")
    for student in failed:
        print(f"{student.name}: {student.average():.2f} (needs {student.passing_grade})")


def show_common(book):
    id1 = ask_text("First student ID: ")
    id2 = ask_text("Second student ID: ")
    common = book.common_courses(id1, id2)
    if common:
        print("Common courses:", ", ".join(sorted(common)))
    else:
        print("These students have no courses in common.")


def print_menu():
    print()
    print("========== GRADEBOOK ==========")
    print("1. Add student")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")


def main():
    book = Gradebook()
    book.load()

    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
        except EOFError:
            choice = "7"

        try:
            if choice == "1":
                add_student(book)
            elif choice == "2":
                add_grade(book)
            elif choice == "3":
                show_students(book)
            elif choice == "4":
                show_ranking(book)
            elif choice == "5":
                show_failing(book)
            elif choice == "6":
                show_common(book)
            elif choice == "7":
                book.save()
                print("Data saved. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")
        except GradebookError as error:
            print("Error:", error)


main()
