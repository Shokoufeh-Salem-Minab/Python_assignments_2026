# Akhil Kammalan Kandy, ak23204, Assignment 4 - Student Gradebook

import json
import os

DATA_FILE = "gradebook.json"
MIN_GRADE = 0
MAX_GRADE = 20
EXIT_CHOICE = "7"

MENU = """
 Student Gradebook
1. Add student (regular or graduate)
2. Add or update a grade
3. Show all students
4. Show ranking (highest to lowest average)
5. Show failing students
6. Show common courses of two students
7. Save and exit"""

# Custom errors
class GradebookError(Exception):
    # Base gradebook error
    pass
class InvalidGradeError(GradebookError):
    # Invalid grade
    pass
class UnknownStudentError(GradebookError):
    # No ID found
    pass
class DuplicateStudentError(GradebookError):
    # ID already exists
    pass


# Student classes

class Student:
    # Regular student

    type_name = "regular"
    label = "Regular"
    passing_grade = 10

    def __init__(self, student_id, name, grades=None):
        self.student_id = student_id
        self.name = name
        self.grades = {}
        for course, grade in (grades or {}).items():
            self.set_grade(course, grade)  # Validate grade

    def set_grade(self, course, grade):
        if not MIN_GRADE <= grade <= MAX_GRADE:
            raise InvalidGradeError(
                f"Grade must be between {MIN_GRADE} and {MAX_GRADE}, got {grade:g}."
            )
        self.grades[course] = grade

    def courses(self):
        return set(self.grades)

    def average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        # Find highest course grade
        if not self.grades:
            return None
        return max(self.grades.items(), key=lambda item: item[1])

    def is_failing(self):
        return bool(self.grades) and self.average() < self.passing_grade

    def to_dict(self):
        return {
            "type": self.type_name,
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["grades"])

    def _best_text(self):
        best = self.best_course()
        if best is None:
            return "-"
        course, grade = best  # Get course and grade
        return f"{course} ({grade:g})"

    def _grades_text(self):
        pairs = sorted(self.grades.items())
        return ", ".join(f"{course}: {grade:g}" for course, grade in pairs) or "no grades yet"

    def __str__(self):
        return (
            f"[{self.student_id}] {self.name} ({self.label}, pass mark {self.passing_grade})"
            f" - average {self.average():.2f}, best: {self._best_text()}\n"
            f"    Grades: {self._grades_text()}"
        )


class GraduateStudent(Student):
    # Graduate student with thesis

    type_name = "graduate"
    label = "Graduate"
    passing_grade = 14

    def __init__(self, student_id, name, grades=None, thesis_title=""):
        super().__init__(student_id, name, grades)
        self.thesis_title = thesis_title

    def to_dict(self):
        data = super().to_dict()
        data["thesis_title"] = self.thesis_title
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["grades"], data["thesis_title"])

    def __str__(self):
        return super().__str__() + f"\n    Thesis: {self.thesis_title}"


STUDENT_TYPES = {cls.type_name: cls for cls in (Student, GraduateStudent)}
LOAD_ERRORS = (OSError, ValueError, KeyError, TypeError, GradebookError)


# Gradebook

class Gradebook:
    # Store students by ID

    def __init__(self):
        self.students = {}

    def __len__(self):
        return len(self.students)

    def ensure_id_available(self, student_id):
        if student_id in self.students:
            raise DuplicateStudentError(f"Student ID '{student_id}' is already in use.")

    def add_student(self, student):
        self.ensure_id_available(student.student_id)
        self.students[student.student_id] = student

    def get_student(self, student_id):
        try:
            return self.students[student_id]
        except KeyError:
            raise UnknownStudentError(f"No student with ID '{student_id}'.") from None

    def all_courses(self):
        # Get unique courses
        return {course for student in self.students.values() for course in student.grades}

    def common_courses(self, id_a, id_b):
        # Find shared courses
        return self.get_student(id_a).courses() & self.get_student(id_b).courses()

    def ranking(self):
        graded = [student for student in self.students.values() if student.grades]
        return sorted(graded, key=lambda student: student.average(), reverse=True)

    def failing_students(self):
        failing = [student for student in self.students.values() if student.is_failing()]
        return sorted(failing, key=lambda student: student.average())

    def save(self, path=DATA_FILE):
        records = [student.to_dict() for student in self.students.values()]
        with open(path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)

    def load(self, path=DATA_FILE):
        if not os.path.exists(path):
            return
        try:
            self.students = self._read_students(path)
        except LOAD_ERRORS as error:
            print(f"Warning: could not read '{path}' ({error}).")
            print("Starting with an empty gradebook (the file is overwritten on exit).")

    @staticmethod
    def _read_students(path):
        with open(path, encoding="utf-8") as file:
            records = json.load(file)
        students = {}
        for record in records:
            student = STUDENT_TYPES[record["type"]].from_dict(record)
            if student.student_id in students:
                raise DuplicateStudentError(f"Duplicate ID '{student.student_id}' in file.")
            students[student.student_id] = student
        return students


# Input helpers

def read_text(prompt):
    text = input(prompt).strip()
    if not text:
        raise GradebookError("Input cannot be empty.")
    return text


def normalize_course(name):
    return name.title()  # Standardize course name


def read_grade(prompt):
    text = input(prompt).strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        raise InvalidGradeError(f"'{text}' is not a number.") from None


# Menu actions

def add_student_action(gradebook):
    kind = read_text("Student type - (r)egular or (g)raduate: ").lower()
    if kind not in ("r", "g"):
        raise GradebookError("Type must be 'r' or 'g'.")
    student_id = read_text("Student ID: ")
    gradebook.ensure_id_available(student_id)
    name = read_text("Name: ")
    if kind == "g":
        student = GraduateStudent(student_id, name, thesis_title=read_text("Thesis title: "))
    else:
        student = Student(student_id, name)
    gradebook.add_student(student)
    print(f"Added {student.label.lower()} student {name} ({student_id}).")


def set_grade_action(gradebook):
    student = gradebook.get_student(read_text("Student ID: "))
    course = normalize_course(read_text("Course: "))
    grade = read_grade(f"Grade ({MIN_GRADE}-{MAX_GRADE}): ")
    student.set_grade(course, grade)
    print(f"Saved: {student.name} - {course}: {grade:g}")


def show_all_action(gradebook):
    if len(gradebook) == 0:
        print("No students yet.")
        return
    print(f"\nStudents ({len(gradebook)}):")
    for student in gradebook.students.values():
        print(student)
    courses = ", ".join(sorted(gradebook.all_courses())) or "none"
    print(f"\nCourses offered: {courses}")


def show_ranking_action(gradebook):
    ranking = gradebook.ranking()
    if not ranking:
        print("No graded students to rank yet.")
        return
    for position, student in enumerate(ranking, start=1):
        print(f"{position}. {student.name} ({student.student_id}) - {student.average():.2f}")


def show_failing_action(gradebook):
    failing = gradebook.failing_students()
    if not failing:
        print("No failing students.")
        return
    for student in failing:
        print(f"{student.name} ({student.student_id}) - average {student.average():.2f}, "
              f"needs {student.passing_grade}")


def common_courses_action(gradebook):
    id_a = read_text("First student ID: ")
    id_b = read_text("Second student ID: ")
    common = gradebook.common_courses(id_a, id_b)
    print("Common courses: " + (", ".join(sorted(common)) if common else "none"))


ACTIONS = {
    "1": add_student_action,
    "2": set_grade_action,
    "3": show_all_action,
    "4": show_ranking_action,
    "5": show_failing_action,
    "6": common_courses_action,
}


# Main loop

def save_and_exit(gradebook):
    # Save data before exit
    try:
        gradebook.save()
    except OSError as error:
        print(f"Error: could not save data ({error}). Returning to the menu.")
        return False
    print(f"Saved {len(gradebook)} student(s) to {DATA_FILE}. Goodbye!")
    return True


def handle_choice(gradebook, choice):
    # Handle selected menu option
    if choice == EXIT_CHOICE:
        return not save_and_exit(gradebook)
    action = ACTIONS.get(choice)
    if action is None:
        print(f"Error: '{choice}' is not a menu option. Choose 1-7.")
        return True
    try:
        action(gradebook)
    except GradebookError as error:
        print(f"Error: {error}")
    return True


def main():
    gradebook = Gradebook()
    gradebook.load()
    print(f"Loaded {len(gradebook)} student(s).")
    running = True
    try:
        while running:
            print(MENU)
            choice = input("Choose an option (1-7): ").strip()
            running = handle_choice(gradebook, choice)
    except (EOFError, KeyboardInterrupt):
        print("\nInput closed - saving and exiting.")
        save_and_exit(gradebook)


if __name__ == "__main__":
    main()