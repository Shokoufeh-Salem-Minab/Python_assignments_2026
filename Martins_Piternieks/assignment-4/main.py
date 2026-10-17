import json
import os

# ----- Global Settings -----
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gradebook.json")
MIN_GRADE = 0
MAX_GRADE = 20


# ----- Custom Exceptions -----
class InvalidGradeError(Exception):
    """Raised when a grade is outside 0 to 20."""

class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when a student ID is already used."""


# ----- Student Class -----
class Student:
    passing_grade = 10

    def __init__(self, student_id, name, grades=None):
        self.student_id = student_id
        self.name = name
        # grades are stored as {course: grade}
        self.grades = grades if grades is not None else {}

    def add_grade(self, course, grade):
        if grade < MIN_GRADE or grade > MAX_GRADE:
            raise InvalidGradeError(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}.")
        self.grades[course] = grade

    def average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        # returns a tuple: (course, grade)
        if not self.grades:
            return "-", 0
        course = max(self.grades, key=lambda c: self.grades[c])
        return course, self.grades[course]

    def is_failing(self):
        return len(self.grades) > 0 and self.average() < self.passing_grade

    def to_dict(self):
        return {"type": "regular", "id": self.student_id, "name": self.name, "grades": self.grades}

    def __str__(self):
        return f"[{self.student_id}] {self.name} | average: {self.average():.2f} | grades: {self.grades}"


# ----- GraduateStudent Class (inherits from Student) -----
class GraduateStudent(Student):
    passing_grade = 14

    def __init__(self, student_id, name, thesis_title, grades=None):
        super().__init__(student_id, name, grades)
        self.thesis_title = thesis_title

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "graduate"
        data["thesis_title"] = self.thesis_title
        return data

    def __str__(self):
        return super().__str__() + f" | thesis: {self.thesis_title} (graduate)"


# ----- Gradebook Class -----
class Gradebook:
    def __init__(self):
        # all students are stored as {student_id: Student}
        self.students = {}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise DuplicateStudentError(f"Student ID '{student.student_id}' already exists.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f"No student with ID '{student_id}'.")
        return self.students[student_id]

    def all_courses(self):
        # set of unique course names across all students
        courses = set()
        for student in self.students.values():
            courses.update(student.grades.keys())
        return courses

    def common_courses(self, id_1, id_2):
        courses_1 = set(self.get_student(id_1).grades)
        courses_2 = set(self.get_student(id_2).grades)
        return courses_1 & courses_2  # set intersection

    def ranking(self):
        # sorted() with a lambda: highest average first
        return sorted(self.students.values(), key=lambda s: s.average(), reverse=True)

    def failing_students(self):
        # list comprehension
        return [s for s in self.students.values() if s.is_failing()]

    # ----- file handling -----
    def save(self, filename):
        data = [student.to_dict() for student in self.students.values()]
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self, filename):
        if not os.path.exists(filename):
            return
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        for item in data:
            self.students[item["id"]] = student_from_dict(item)


def student_from_dict(item):
    if item["type"] == "graduate":
        return GraduateStudent(item["id"], item["name"], item["thesis_title"], item["grades"])
    return Student(item["id"], item["name"], item["grades"])


# ----- input helpers -----
def ask_text(message):
    text = input(message).strip()
    if text == "":
        raise ValueError("Input cannot be empty.")
    return text


def ask_grade():
    text = input("Enter grade (0-20): ").strip()
    try:
        grade = float(text)
    except ValueError:
        raise ValueError(f"'{text}' is not a number.")
    if grade < MIN_GRADE or grade > MAX_GRADE:
        raise InvalidGradeError(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}.")
    return grade


# ----- menu actions -----
def add_student(gradebook):
    kind = ask_text("Regular or graduate student? (r/g): ").lower()
    if kind not in ("r", "g"):
        raise ValueError("Please type 'r' or 'g'.")

    student_id = ask_text("Enter student ID: ")
    if student_id in gradebook.students:
        raise DuplicateStudentError(f"Student ID '{student_id}' already exists.")
    name = ask_text("Enter student name: ")

    if kind == "g":
        thesis = ask_text("Enter thesis title: ")
        student = GraduateStudent(student_id, name, thesis)
    else:
        student = Student(student_id, name)

    gradebook.add_student(student)
    print(f"\nStudent '{name}' added successfully!")


def add_grade(gradebook):
    student = gradebook.get_student(ask_text("Enter student ID: "))
    course = ask_text("Enter course name: ")
    grade = ask_grade()
    student.add_grade(course, grade)
    print(f"\n{course}: {grade} saved for {student.name}.")


def show_all_students(gradebook):
    if len(gradebook) == 0:
        print("\nNo students yet.")
        return

    print(f"\n----- ALL STUDENTS ({len(gradebook)}) -----")
    for student in gradebook.students.values():
        print(student)
        course, grade = student.best_course()  # tuple unpacking
        print(f"    best course: {course} ({grade})")

    print("\nAll courses offered:", sorted(gradebook.all_courses()))


def show_ranking(gradebook):
    ranking = gradebook.ranking()
    if not ranking:
        print("\nNo students yet.")
        return

    print("\n----- RANKING -----")
    for place, student in enumerate(ranking, start=1):
        print(f"{place}. {student.name} - {student.average():.2f}")


def show_failing(gradebook):
    failing = gradebook.failing_students()
    if not failing:
        print("\nNo failing students.")
        return

    print("\n----- FAILING STUDENTS -----")
    for student in failing:
        print(f"{student.name} - average {student.average():.2f} (needs {student.passing_grade})")


def show_common_courses(gradebook):
    id_1 = ask_text("Enter first student ID: ")
    id_2 = ask_text("Enter second student ID: ")
    common = gradebook.common_courses(id_1, id_2)

    if common:
        print("\nCommon courses:", sorted(common))
    else:
        print("\nThese students have no courses in common.")


# ----- menu -----
def show_menu():
    print("\n===== STUDENT GRADEBOOK =====")
    print("1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")


def load_gradebook():
    gradebook = Gradebook()
    try:
        gradebook.load(DATA_FILE)
        print(f"Loaded {len(gradebook)} student(s) from file.")
    except (json.JSONDecodeError, KeyError):
        print("Could not read the data file. Starting with an empty gradebook.")
    return gradebook


def main():
    gradebook = load_gradebook()
    actions = {
        "1": add_student,
        "2": add_grade,
        "3": show_all_students,
        "4": show_ranking,
        "5": show_failing,
        "6": show_common_courses,
    }

    running = True
    while running:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        if choice == "7":
            gradebook.save(DATA_FILE)
            print("\nData saved. Goodbye!")
            running = False
        elif choice in actions:
            try:
                actions[choice](gradebook)
            except (ValueError, InvalidGradeError, StudentNotFoundError, DuplicateStudentError) as error:
                print(f"\nError: {error}")
        else:
            print("\nInvalid option. Please choose 1-7.")


main()
