import json
import os

# file where all data is saved
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gradebook.json")
MIN_GRADE = 0
MAX_GRADE = 20


# custom exceptions
class GradebookError(Exception):
    # parent class for all my errors
    pass


class InvalidGradeError(GradebookError):
    # grade is not a number or not between 0 and 20
    pass


class StudentNotFoundError(GradebookError):
    # unknown student id
    pass


class DuplicateStudentError(GradebookError):
    # student id already used
    pass


class InvalidInputError(GradebookError):
    # other wrong input (empty text, wrong menu choice)
    pass


def validate_grade(value):
    # check that grade is a number
    try:
        grade = float(value)
    except (TypeError, ValueError):
        raise InvalidGradeError(f"'{value}' is not a number.") from None
    # check that grade is in range 0-20
    if not MIN_GRADE <= grade <= MAX_GRADE:
        raise InvalidGradeError(
            f"Grade must be between {MIN_GRADE} and {MAX_GRADE}, got {value}."
        )
    return grade


class Student:
    kind = "Student"
    passing_grade = 10

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  # {course: grade}

    def set_grade(self, course, grade):
        # add a new grade or update the old one
        self.grades[course] = validate_grade(grade)

    def average(self):
        # no grades -> average is 0
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        # returns a tuple (course, grade) with the highest grade
        if not self.grades:
            return None
        return max(self.grades.items(), key=lambda item: item[1])

    def is_failing(self):
        # failing = has grades and average is below passing grade
        return bool(self.grades) and self.average() < self.passing_grade

    def grades_text(self):
        # grades as text, for printing
        if not self.grades:
            return "none"
        return ", ".join(f"{course}={grade:g}" for course, grade in self.grades.items())

    def to_dict(self):
        # student -> dictionary, so it can be saved in json
        return {
            "type": "student",
            "id": self.student_id,
            "name": self.name,
            "grades": self.grades,
        }

    def load_grades(self, grades):
        # put grades from the file into the student
        for course, grade in grades.items():
            self.set_grade(course, grade)

    @classmethod
    def from_dict(cls, data):
        # dictionary from json -> Student object
        student = cls(str(data["id"]), str(data["name"]))
        student.load_grades(data["grades"])
        return student

    def __str__(self):
        text = (
            f"[{self.student_id}] {self.name} ({self.kind}) "
            f"| Average: {self.average():.2f} | Passing grade: {self.passing_grade}"
        )
        best = self.best_course()
        if best is not None:
            course, grade = best  # tuple unpacking
            text += f" | Best: {course} ({grade:g})"
        return f"{text}\n    Grades: {self.grades_text()}"


class GraduateStudent(Student):
    # inherits from Student, but has a thesis and higher passing grade
    kind = "Graduate"
    passing_grade = 14

    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def to_dict(self):
        # same as Student, plus type and thesis
        data = super().to_dict()
        data["type"] = "graduate"
        data["thesis_title"] = self.thesis_title
        return data

    @classmethod
    def from_dict(cls, data):
        student = cls(str(data["id"]), str(data["name"]), str(data["thesis_title"]))
        student.load_grades(data["grades"])
        return student

    def __str__(self):
        return super().__str__() + f"\n    Thesis: {self.thesis_title}"


# used when loading, picks the class by the saved type
STUDENT_TYPES = {"student": Student, "graduate": GraduateStudent}


class Gradebook:
    def __init__(self):
        self.students = {}  # {student_id: Student}

    def __len__(self):
        # number of students
        return len(self.students)

    def check_id_free(self, student_id):
        # ids must be unique
        if student_id in self.students:
            raise DuplicateStudentError(f"Student ID '{student_id}' already exists.")

    def add_student(self, student):
        self.check_id_free(student.student_id)
        self.students[student.student_id] = student

    def get_student(self, student_id):
        # find student by id, error if it does not exist
        try:
            return self.students[student_id]
        except KeyError:
            raise StudentNotFoundError(f"No student with ID '{student_id}'.") from None

    def all_courses(self):
        # set of unique course names from all students
        return {course for student in self.students.values() for course in student.grades}

    def common_courses(self, id_one, id_two):
        # courses that both students have (set intersection)
        first = self.get_student(id_one)
        second = self.get_student(id_two)
        return set(first.grades) & set(second.grades)

    def ranking(self):
        # sort students by average, highest first
        return sorted(self.students.values(), key=lambda s: s.average(), reverse=True)

    def failing_students(self):
        # list comprehension to get failing students, then sort lowest average first
        failing = [s for s in self.students.values() if s.is_failing()]
        return sorted(failing, key=lambda s: s.average())

    def save(self, path):
        # write all students to the json file
        data = {"students": [s.to_dict() for s in self.students.values()]}
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load(cls, path):
        # read students from the json file
        book = cls()
        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
            for item in data["students"]:
                book.add_student(STUDENT_TYPES[item["type"]].from_dict(item))
        except FileNotFoundError:
            # first run, no file yet
            return cls()
        except (OSError, ValueError, KeyError, TypeError, AttributeError, GradebookError) as error:
            print(f"Warning: could not read '{path}' ({error}). Starting empty.")
            backup_bad_file(path)
            return cls()
        return book


def backup_bad_file(path):
    # keep the broken file as .bak so it is not overwritten
    try:
        os.replace(path, path + ".bak")
        print(f"The old file was kept as '{path}.bak'.")
    except OSError:
        pass


def ask(prompt):
    return input(prompt).strip()


def ask_required(prompt):
    # input that cannot be empty
    text = ask(prompt)
    if not text:
        raise InvalidInputError("This field cannot be empty.")
    return text


# menu option 1
def add_student_action(book):
    kind = ask("Student type - (r)egular or (g)raduate: ").lower()
    if kind not in ("r", "g"):
        raise InvalidInputError("Type must be 'r' or 'g'.")
    student_id = ask_required("Student ID: ")
    book.check_id_free(student_id)
    name = ask_required("Name: ")
    if kind == "g":
        student = GraduateStudent(student_id, name, ask_required("Thesis title: "))
    else:
        student = Student(student_id, name)
    book.add_student(student)
    print(f"Added {student.kind.lower()}: {name} ({student_id}).")


# menu option 2
def update_grade_action(book):
    student = book.get_student(ask_required("Student ID: "))
    course = ask_required("Course name: ")
    grade = validate_grade(ask(f"Grade ({MIN_GRADE}-{MAX_GRADE}): "))
    verb = "Updated" if course in student.grades else "Added"
    student.set_grade(course, grade)
    print(f"{verb} {course} = {grade:g} for {student.name}.")


# menu option 3
def show_all_action(book):
    if len(book) == 0:
        print("No students yet.")
        return
    print(f"\nStudents ({len(book)}):")
    for student in book.students.values():
        print(student)
    courses = ", ".join(sorted(book.all_courses())) or "none"
    print(f"\nCourses offered: {courses}")


# menu option 4
def show_ranking_action(book):
    if len(book) == 0:
        print("No students yet.")
        return
    # list comprehension builds the ranking lines
    lines = [
        f"{place}. {student.name} ({student.student_id}) - {student.average():.2f}"
        for place, student in enumerate(book.ranking(), start=1)
    ]
    print("\nRanking (highest to lowest average):")
    print("\n".join(lines))


# menu option 5
def show_failing_action(book):
    failing = book.failing_students()
    if not failing:
        print("No failing students.")
        return
    lines = [
        f"{s.name} ({s.student_id}) - average {s.average():.2f}, needs {s.passing_grade}"
        for s in failing
    ]
    print("\nFailing students:")
    print("\n".join(lines))


# menu option 6
def common_courses_action(book):
    id_one = ask_required("First student ID: ")
    id_two = ask_required("Second student ID: ")
    common = book.common_courses(id_one, id_two)
    if common:
        print("Common courses: " + ", ".join(sorted(common)))
    else:
        print("These students have no common courses.")


# menu number -> function
ACTIONS = {
    "1": add_student_action,
    "2": update_grade_action,
    "3": show_all_action,
    "4": show_ranking_action,
    "5": show_failing_action,
    "6": common_courses_action,
}

MENU = """
===== Student Gradebook =====
1. Add student (regular or graduate)
2. Add or update a grade
3. Show all students
4. Show ranking (highest to lowest average)
5. Show failing students
6. Show common courses of two students
7. Save and exit"""


def save_data(book):
    try:
        book.save(DATA_FILE)
        print(f"Saved {len(book)} student(s) to {DATA_FILE}.")
    except OSError as error:
        print(f"Error: could not save data ({error}).")


def run_choice(book, choice):
    # runs one menu choice, returns False when the user picks 7 (exit)
    if choice == "7":
        return False
    if choice not in ACTIONS:
        raise InvalidInputError("Please enter a number from 1 to 7.")
    ACTIONS[choice](book)
    return True


def main():
    # load saved data when the program starts
    book = Gradebook.load(DATA_FILE)
    print(f"Loaded {len(book)} student(s).")
    running = True
    # main menu loop, runs until the user chooses 7
    while running:
        print(MENU)
        try:
            running = run_choice(book, ask("Choose an option (1-7): "))
        except GradebookError as error:
            # any of my errors: show message and go back to the menu
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C or closed input: save and exit
            print("\nInput closed. Saving and exiting.")
            running = False
    # save everything when the program ends
    save_data(book)


if __name__ == "__main__":
    main()
