import json


class InvalidGradeError(Exception):
    pass


class Student:
    def init(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    def passing_grade(self):
        return 10

    def add_grade(self, course, grade):
        if grade < 0 or grade > 20:
            raise InvalidGradeError("Grade must be between 0 and 20.")
        self.grades[course] = grade

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        if not self.grades:
            return None
        course = max(self.grades, key=self.grades.get)
        return course, self.grades[course]

    def is_failing(self):
        return any(grade < self.passing_grade()
                   for grade in self.grades.values())

    def str(self):
        return f"{self.name} (ID: {self.student_id})"


class GraduateStudent(Student):
    def init(self, student_id, name, thesis_title):
        super().init(student_id, name)
        self.thesis_title = thesis_title

    def passing_grade(self):
        return 14

    def str(self):
        return super().str() + f" - Thesis: {self.thesis_title}"


class Gradebook:
    def init(self):
        self.students = {}

    def len(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("This student ID already exists.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise KeyError("Student not found.")
        return self.students[student_id]

    def all_courses(self):
        courses = set()
        for student in self.students.values():
            courses.update(student.grades.keys())
        return courses

    def ranking(self):
        return sorted(
            self.students.values(),
            key=lambda student: student.average(),
            reverse=True
        )

    def failing_students(self):
        return [
            student for student in self.students.values()
            if student.is_failing()
        ]

    def common_courses(self, id1, id2):
        student1 = self.get_student(id1)
        student2 = self.get_student(id2)
        return set(student1.grades) & set(student2.grades)

    def save(self):
        data = []

        for student in self.students.values():
            item = {
                "student_id": student.student_id,
                "name": student.name,
                "grades": student.grades,
                "type": "graduate" if isinstance(student, GraduateStudent)
                        else "regular"
            }

            if isinstance(student, GraduateStudent):
                item["thesis_title"] = student.thesis_title

            data.append(item)

        with open("gradebook.json", "w") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open("gradebook.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("No saved data found. Starting a new gradebook.")
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
            self.students[student.student_id] = student


def add_student(gradebook):
    student_id = input("Student ID: ").strip()
    name = input("Student name: ").strip()

    if not student_id or not name:
        print("ID and name cannot be empty.")
        return

    kind = input("Regular or graduate? (r/g): ").lower()
    if kind == "g":
        thesis = input("Thesis title: ")
        student = GraduateStudent(student_id, name, thesis)
    elif kind == "r":
        student = Student(student_id, name)
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

    try:
        student = gradebook.get_student(student_id)
        course = input("Course name: ").strip()
        grade = float(input("Grade (0-20): "))

        student.add_grade(course, grade)
        print("Grade saved.")

    except KeyError as error:
        print(error.args[0])
    except InvalidGradeError as error:
        print(error)
    except ValueError:
        print("Please enter a valid number for the grade.")


def show_students(gradebook):
    if len(gradebook) == 0:
        print("No students yet.")
        return

    for student in gradebook.students.values():
        print("\n", student)
        print("Grades:", student.grades)
        print(f"Average: {student.average():.2f}")

        best = student.best_course()
        if best is not None:
            course, grade = best
            print(f"Best course: {course}, grade: {grade}")


def show_ranking(gradebook):
    for number, student in enumerate(gradebook.ranking(), start=1):
        print(f"{number}. {student.name} - "
              f"Average: {student.average():.2f}")


def show_failing(gradebook):
    students = gradebook.failing_students()

    if not students:
        print("No failing students.")
        return

    for student in students:
        print(student.name, "- ID:", student.student_id)


def show_common_courses(gradebook):
    id1 = input("First student ID: ").strip()
    id2 = input("Second student ID: ").strip()

    try:
        courses = gradebook.common_courses(id1, id2)

        if courses:
            print("Common courses:", ", ".join(sorted(courses)))
        else:
            print("No courses in common.")

    except KeyError as error:
        print(error.args[0])


def main():
    gradebook = Gradebook()
    gradebook.load()

    while True:
        print("\n--- Student Gradebook ---")
        print("1. Add student")
        print("2. Add or update a grade")
        print("3. Show all students")
        print("4. Show ranking")
        print("5. Show failing students")
        print("6. Show common courses")
        print("7. Save and exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student(gradebook)
        elif choice == "2":
            add_grade(gradebook)
        elif choice == "3":
            show_students(gradebook)
            print("Number of students:", len(gradebook))
            print("All courses:", gradebook.all_courses())
        elif choice == "4":
            show_ranking(gradebook)
        elif choice == "5":
            show_failing(gradebook)
        elif choice == "6":
            show_common_courses(gradebook)
        elif choice == "7":
            try:
                gradebook.save()
                print("Data saved. Goodbye!")
            except OSError as error:
                print("Could not save data:", error)
            break
        else:
            print("Choose a number from 1 to 7.")


if __name__ == "main":
    main()