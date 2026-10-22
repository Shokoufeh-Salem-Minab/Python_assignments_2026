import json

class InvalidGradeError(Exception):
    pass

class Student:
    passing_grade = 10

    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        self.grades = {}

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) /len(self.grades)

    def best_course(self):
        return max(self.grades.items(), key=lambda item: item[1])

    def __str__(self):
        return f"{self.id}: {self.name}, grades: {self.grades}"

class Gradebook:
    def __init__(self):
        self.students = {}

    def __len__(self):
        return len(self.students)

    def add_student(self, student, student_id):
        if student_id in self.students:
            print("ID already exists")
        else:
            self.students[student_id] = student
            print("Student added successfully")

    def change_grade(self, student_id):
        try:
            student = self.students[student_id]
        except KeyError:
            print("Student ID doesn't exist")
            return

        course = input("Which course?")

        try:
            grade = int(input("Enter grade (0-20):"))
            if not 0 <= grade <= 20:
                raise InvalidGradeError("Grade must be between 0 and 20")
        except (ValueError, InvalidGradeError):
            print("Invalid grade.")
            return

        student.grades[course] = grade

    def show_students(self):
        print(len(self), "students")
        for student in self.students.values():
            print(student)
        print("All courses:", self.all_courses())

    def show_ranking(self):
        ranking = sorted(
            self.students.values(),
            key=lambda student: student.average(),
            reverse = True
        )
        for student in ranking:
            print(student.name, student.average())
            if student.grades:
                course, grade = student.best_course()
                print("  best course:", course, grade)

    def failing_students(self):
        failing = [
            student for student in self.students.values()
        if student.average() < student.passing_grade
        ]

        failing = sorted(
            failing,
            key=lambda student: student.average()
        )

        for student in failing:
            print(student.name, student.average())

    def common_courses(self, first_student_id, second_student_id):
        try:
            first_student = self.students[first_student_id]
            second_student = self.students[second_student_id]
        except KeyError:
            print("Invalid student ID")
            return

        common = first_student.grades.keys() & second_student.grades.keys()
        print(common)

    def all_courses(self):
        return {course for student in self.students.values() for course in student.grades}

    def save(self):
        with open("gradebook.json", "w") as file:
            json.dump([vars(student) for student in self.students.values()], file)

    def load(self):
        try:
            with open("gradebook.json") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        for item in data:
            if "thesis_title" in item:
                student = GraduateStudent(item["id"], item["name"], item["thesis_title"])
            else:
                student = Student(item["id"], item["name"])
            student.grades = item["grades"]
            self.students[student.id] = student

class GraduateStudent(Student):
    passing_grade = 14

    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def __str__(self):
        return super().__str__() + f", thesis: {self.thesis_title}"

gradebook = Gradebook()
gradebook.load()

while True:
    print(
        "\n1. Add student (regular or graduate)\n"
        "2. Add or update a grade\n"
        "3. Show all students\n"
        "4. Show ranking (highest to lowest average)\n"
        "5. Show failing students\n"
        "6. Show common courses of two students\n"
        "7. Save and exit")
    choice = input("What would you like to do? ")

    if choice == "1":
        student_id = input("Input Student ID: ")
        name = input("Input student name: ")
        thesis_title = input("Thesis title: ")
        if thesis_title:
            student = GraduateStudent(student_id, name, thesis_title)
        else:
            student = Student(student_id, name)
        gradebook.add_student(student, student_id)

    elif choice == "2":
        student_id = input("Input the student ID of which to change grade: ")
        gradebook.change_grade(student_id)

    elif choice == "3":
        gradebook.show_students()

    elif choice == "4":
        gradebook.show_ranking()

    elif choice == "5":
        gradebook.failing_students()

    elif choice == "6":
        first_student_id  = input("Input the student ID of first student: ")
        second_student_id = input("Input the student ID of second student: ")
        gradebook.common_courses(first_student_id, second_student_id)

    elif choice == "7":
        gradebook.save()
        print("Saved")
        break

    else:
        print("Invalid option, choose 1-7")
