import json
import os


# Custom exception used when a student ID does not exist
class StudentNotFoundError(Exception):
    pass


# Class for a regular student
class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        # Each student's grades are stored as {course: grade}
        self.grades = {}

    # Regular students need at least 10 to pass
    def passing_grade(self):
        return 10

    # Calculate the average grade, or return 0 if there are no grades
    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    # Return the best course and grade as a tuple
    def best_course(self):
        if len(self.grades) == 0:
            return ("No grades yet", 0)

        best_course_name = max(self.grades, key=self.grades.get)
        return (best_course_name, self.grades[best_course_name])

    # Special method used when printing a student
    def __str__(self):
        return (
            f"ID: {self.student_id} | Name: {self.name} | "
            f"Average: {self.average():.2f}"
        )


# GraduateStudent inherits from Student
class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    # Graduate students need at least 14 to pass
    def passing_grade(self):
        return 14

    # Show the thesis title as well as the regular student information
    def __str__(self):
        return (
            f"{super().__str__()} | Graduate student | "
            f"Thesis: {self.thesis_title}"
        )


# Class that manages all students
class Gradebook:
    def __init__(self):
        # Store all students as {student_id: Student}
        self.students = {}
        # Set of unique course names offered across all students
        self.courses = set()

    # Number of students in the gradebook
    def __len__(self):
        return len(self.students)

    # Add a student, making sure the ID is unique
    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("That student ID is already in use.")
        self.students[student.student_id] = student

    # Find a student or raise our custom exception
    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError("Student ID was not found.")
        return self.students[student_id]

    # Add or update a grade
    def set_grade(self, student_id, course, grade):
        student = self.get_student(student_id)

        if grade < 0 or grade > 20:
            raise ValueError("Grades must be between 0 and 20.")

        student.grades[course] = grade
        self.courses.add(course)

    # Build a ranking using sorted() and a lambda function
    def ranking(self):
        return sorted(
            self.students.values(),
            key=lambda student: student.average(),
            reverse=True
        )

    # Use a list comprehension to find students who have a failing grade
    def failing_students(self):
        return [
            student
            for student in self.students.values()
            if any(grade < student.passing_grade()
                   for grade in student.grades.values())
        ]

    # Find courses that two students have in common using set intersection
    def common_courses(self, first_id, second_id):
        first_student = self.get_student(first_id)
        second_student = self.get_student(second_id)
        first_courses = set(first_student.grades.keys())
        second_courses = set(second_student.grades.keys())
        return first_courses.intersection(second_courses)

    # Save all student information to a JSON file
    def save(self, filename):
        data = []

        for student in self.students.values():
            student_data = {
                "student_id": student.student_id,
                "name": student.name,
                "grades": student.grades,
                "student_type": "graduate"
                if isinstance(student, GraduateStudent) else "regular"
            }

            if isinstance(student, GraduateStudent):
                student_data["thesis_title"] = student.thesis_title

            data.append(student_data)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # Load student information from a JSON file
    def load(self, filename):
        if not os.path.exists(filename):
            return

        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                if item.get("student_type") == "graduate":
                    student = GraduateStudent(
                        item["student_id"],
                        item["name"],
                        item.get("thesis_title", "")
                    )
                else:
                    student = Student(item["student_id"], item["name"])

                student.grades = {
                    course: float(grade)
                    for course, grade in item.get("grades", {}).items()
                }
                self.students[student.student_id] = student
                self.courses.update(student.grades.keys())

        except (json.JSONDecodeError, OSError, KeyError, TypeError, ValueError) as error:
            print("Could not load saved data:", error)


# Ask the user for a grade and handle non-numeric input
def get_grade_input():
    grade_text = input("Enter grade (0-20): ")
    try:
        grade = float(grade_text)
    except ValueError:
        raise ValueError("Please enter a numeric grade.")

    if grade < 0 or grade > 20:
        raise ValueError("Grades must be between 0 and 20.")

    return grade


# Menu option 1: add a regular or graduate student
def add_student_menu(gradebook):
    student_id = input("Enter a unique student ID: ").strip()
    name = input("Enter student name: ").strip()

    if not student_id or not name:
        print("Student ID and name cannot be empty.")
        return

    student_type = input("Regular or graduate student? (r/g): ").strip().lower()

    if student_type == "g":
        thesis_title = input("Enter thesis title: ").strip()
        student = GraduateStudent(student_id, name, thesis_title)
    elif student_type == "r":
        student = Student(student_id, name)
    else:
        print("Please enter r for regular or g for graduate.")
        return

    try:
        gradebook.add_student(student)
        print("Student added successfully.")
    except ValueError as error:
        print("Error:", error)


# Menu option 2: add or update a grade
def add_grade_menu(gradebook):
    student_id = input("Enter student ID: ").strip()
    course = input("Enter course name: ").strip()

    if not course:
        print("Course name cannot be empty.")
        return

    try:
        grade = get_grade_input()
        gradebook.set_grade(student_id, course, grade)
        print("Grade saved successfully.")
    except (ValueError, StudentNotFoundError) as error:
        print("Error:", error)


# Menu option 3: show all students
def show_students(gradebook):
    print("\n========== ALL STUDENTS ==========")

    if len(gradebook) == 0:
        print("There are no students yet.")
        return

    for student in gradebook.students.values():
        print(student)

        if student.grades:
            for course, grade in student.grades.items():
                print(f"  {course}: {grade:g}")

            # Tuple unpacking: read the best course and its grade
            best_course, best_grade = student.best_course()
            print(f"  Best course: {best_course} ({best_grade:g})")
        else:
            print("  No grades yet.")


# Menu option 4: show ranking from highest to lowest average
def show_ranking(gradebook):
    print("\n========== STUDENT RANKING ==========")

    if len(gradebook) == 0:
        print("There are no students yet.")
        return

    for position, student in enumerate(gradebook.ranking(), start=1):
        print(f"{position}. {student.name} - Average: {student.average():.2f}")


# Menu option 5: show failing students
def show_failing_students(gradebook):
    print("\n========== FAILING STUDENTS ==========")
    failing = gradebook.failing_students()

    if not failing:
        print("No failing students.")
        return

    for student in failing:
        print(f"{student.name} (passing grade: {student.passing_grade()})")


# Menu option 6: find common courses for two students
def show_common_courses(gradebook):
    first_id = input("Enter the first student ID: ").strip()
    second_id = input("Enter the second student ID: ").strip()

    try:
        common = gradebook.common_courses(first_id, second_id)

        if common:
            print("Common courses:", ", ".join(sorted(common)))
        else:
            print("These students have no courses in common.")
    except StudentNotFoundError as error:
        print("Error:", error)


# Main program
def main():
    filename = "gradebook.json"
    gradebook = Gradebook()

    # Load saved students when the program starts
    gradebook.load(filename)
    print("Welcome to Student Gradebook!")
    print("Students loaded:", len(gradebook))

    # Keep showing the menu until the user chooses option 7
    while True:
        print("\n========== STUDENT GRADEBOOK ==========")
        print("1. Add student (regular or graduate)")
        print("2. Add or update a grade")
        print("3. Show all students")
        print("4. Show ranking")
        print("5. Show failing students")
        print("6. Show common courses of two students")
        print("7. Save and exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student_menu(gradebook)
        elif choice == "2":
            add_grade_menu(gradebook)
        elif choice == "3":
            show_students(gradebook)
        elif choice == "4":
            show_ranking(gradebook)
        elif choice == "5":
            show_failing_students(gradebook)
        elif choice == "6":
            show_common_courses(gradebook)
        elif choice == "7":
            try:
                gradebook.save(filename)
                print("Data saved. Goodbye!")
            except OSError as error:
                print("Could not save data:", error)
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 7.")


# Start the program
if __name__ == "__main__":
    main()
