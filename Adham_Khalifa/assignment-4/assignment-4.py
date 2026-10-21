# Homework 4 - Student Gradebook
import json


class StudentNotFoundError(Exception):
    pass


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    def passing_grade(self):
        return 10

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        if not self.grades:
            return ("No grades", 0)
        course = max(self.grades, key=self.grades.get)
        return (course, self.grades[course])

    def __str__(self):
        return f"{self.student_id} - {self.name} - Average: {self.average():.2f}"


class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def passing_grade(self):
        return 14

    def __str__(self):
        return f"{super().__str__()} - Thesis: {self.thesis_title}"


class Gradebook:
    def __init__(self):
        self.students = {}
        self.courses = set()

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("This student ID already exists.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError("Student ID not found.")
        return self.students[student_id]

    def add_grade(self, student_id, course, grade):
        student = self.get_student(student_id)

        if grade < 0 or grade > 20:
            raise ValueError("Grade must be between 0 and 20.")

        student.grades[course] = grade
        self.courses.add(course)

    def ranking(self):
        return sorted(
            self.students.values(),
            key=lambda student: student.average(),
            reverse=True
        )

    def failing_students(self):
        return [
            student for student in self.students.values()
            if any(grade < student.passing_grade()
                   for grade in student.grades.values())
        ]

    def common_courses(self, id1, id2):
        student1 = self.get_student(id1)
        student2 = self.get_student(id2)
        return set(student1.grades) & set(student2.grades)

    def save(self):
        data = []
        for student in self.students.values():
            item = {
                "id": student.student_id,
                "name": student.name,
                "grades": student.grades,
                "type": "graduate" if isinstance(student, GraduateStudent) else "regular"
            }
            if isinstance(student, GraduateStudent):
                item["thesis"] = student.thesis_title
            data.append(item)

        with open("gradebook.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open("gradebook.json", "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                if item["type"] == "graduate":
                    student = GraduateStudent(item["id"], item["name"], item["thesis"])
                else:
                    student = Student(item["id"], item["name"])

                student.grades = item["grades"]
                self.students[student.student_id] = student
                self.courses.update(student.grades.keys())

        except FileNotFoundError:
            print("No saved file yet. Starting a new gradebook.")
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print("Could not load the file:", error)


def add_student(gradebook):
    student_id = input("Student ID: ").strip()
    name = input("Student name: ").strip()

    if not student_id or not name:
        print("ID and name cannot be empty.")
        return

    kind = input("Regular or graduate? (r/g): ").lower().strip()

    if kind == "r":
        student = Student(student_id, name)
    elif kind == "g":
        thesis = input("Thesis title: ").strip()
        student = GraduateStudent(student_id, name, thesis)
    else:
        print("Please enter r or g.")
        return

    try:
        gradebook.add_student(student)
        print("Student added.")
    except ValueError as error:
        print(error)


def add_grade(gradebook):
    student_id = input("Student ID: ").strip()
    course = input("Course name: ").strip()

    try:
        grade = float(input("Grade (0-20): "))
        gradebook.add_grade(student_id, course, grade)
        print("Grade saved.")
    except ValueError as error:
        print("Please enter a number from 0 to 20.", error)
    except StudentNotFoundError as error:
        print(error)


def show_students(gradebook):
    if len(gradebook) == 0:
        print("No students yet.")
        return

    for student in gradebook.students.values():
        print(student)
        for course, grade in student.grades.items():
            print(f"  {course}: {float(grade):.2f}")

        # Unpack the tuple returned by best_course().
        course, grade = student.best_course()
        print(f"  Best course: {course}, grade: {grade}")


def show_ranking(gradebook):
    for number, student in enumerate(gradebook.ranking(), start=1):
        print(f"{number}. {student.name}: {student.average():.2f}")


def show_failing(gradebook):
    students = gradebook.failing_students()
    if not students:
        print("No failing students.")
    for student in students:
        print(f"{student.name} needs {student.passing_grade()} to pass.")


def show_common_courses(gradebook):
    try:
        id1 = input("First student ID: ").strip()
        id2 = input("Second student ID: ").strip()
        common = gradebook.common_courses(id1, id2)
        print("Common courses:", ", ".join(sorted(common)) if common else "None")
    except StudentNotFoundError as error:
        print(error)


def main():
    gradebook = Gradebook()
    gradebook.load()

    while True:
        print("\nSTUDENT GRADEBOOK")
        print("1. Add student")
        print("2. Add or update a grade")
        print("3. Show all students")
        print("4. Show ranking")
        print("5. Show failing students")
        print("6. Show common courses")
        print("7. Save and exit")

        choice = input("Choose 1-7: ").strip()

        try:
            if choice == "1":
                add_student(gradebook)
            elif choice == "2":
                add_grade(gradebook)
            elif choice == "3":
                show_students(gradebook)
            elif choice == "4":
                show_ranking(gradebook)
            elif choice == "5":
                show_failing(gradebook)
            elif choice == "6":
                show_common_courses(gradebook)
            elif choice == "7":
                gradebook.save()
                print("Data saved. Goodbye!")
                break
            else:
                print("Choose a number from 1 to 7.")
        except (ValueError, StudentNotFoundError) as error:
            print("Error:", error)
        except (OSError, TypeError) as error:
            print("Something went wrong:", error)


if __name__ == "__main__":
    main()
