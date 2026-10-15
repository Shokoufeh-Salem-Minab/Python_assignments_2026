import json
import os

class GradebookError(Exception):
    pass

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  

    def to_dict(self):
        return {
            "type": "regular",
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    def add_grade(self, course, grade):
        if not(0 <= grade <= 20):
            raise GradebookError("Grade must be between 0 and 20.")
        self.grades[course] = grade

    def calculate_average(self):
        if not self.grades:
            return 0.0
        return sum(self.grades.values()) / len(self.grades)

    def is_passing(self):
        avg = self.calculate_average()
        if avg >= 10.0:
            return True
        else:
            return False

    def best_course(self):
        if len(self.grades) == 0:
            return ("None", 0.0)
        best = max(self.grades.items(), key=lambda x: x[1])
        return best

    def __str__(self):
        # Mixed string formatting: using .format() instead of f-string
        return "Student ID: {}, Name: {}, Average: {:.2f}".format(self.student_id, self.name, self.calculate_average())

class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "graduate"
        d["thesis_title"] = self.thesis_title
        return d

    def is_passing(self):
        avg = self.calculate_average()
        if avg >= 14.0:
            return True
        else:
            return False

    def __str__(self):
        # Mixed string formatting: using concatenation + style
        return "Graduate Student ID: " + self.student_id + ", Name: " + self.name + ", Thesis: '" + self.thesis_title + "', Average: " + "{:.2f}".format(self.calculate_average())

class Gradebook:
    def __init__(self):
        self.students = {}  

    def all_courses(self):
        courses = set()
        for s in self.students.values():
            courses.update(s.grades.keys())
        return courses

    def add_student(self, student):
        if student.student_id in self.students:
            raise GradebookError("Student ID " + student.student_id + " already exists.")
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise GradebookError("Student ID '" + student_id + "' not found.")
        return self.students[student_id]

    def __len__(self):
        return len(self.students)

    def save_to_file(self, filename="gradebook_data.json"):
        data = {sid: s.to_dict() for sid, s in self.students.items()}
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename="gradebook_data.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data = json.load(f)
            for sid, info in data.items():
                if info["type"] == "graduate":
                    s = GraduateStudent(sid, info["name"], info["thesis_title"])
                else:
                    s = Student(sid, info["name"])
                s.grades = info["grades"]
                self.students[sid] = s


def show_menu():
    print("\n--- Student Gradebook Menu ---")
    print("1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking (highest to lowest average)")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")

def show_all_students(gb):
    if not gb.students:
        print("No students recorded in the gradebook.")
    else:
        for s in gb.students.values():
            print(s)
            c, g = s.best_course()
            print("  -> Best Course: {} ({})".format(c, g))
        courses = gb.all_courses()
        if courses:
            print("Courses offered: " + ", ".join(sorted(courses)))

def add_new_student(gb):
    stype = input("Enter type (regular/grad): ").strip().lower()
    sid = input("Enter student ID: ").strip()
    name = input("Enter student name: ").strip()
    if stype == "grad":
        thesis = input("Enter thesis title: ").strip()
        student = GraduateStudent(sid, name, thesis)
    elif stype == "regular":
        student = Student(sid, name)
    else:
        raise GradebookError("Invalid student type specified.")
    gb.add_student(student)
    print("Student " + name + " added successfully.")

def update_grade(gb):
    sid = input("Enter student ID: ").strip()
    student = gb.get_student(sid)
    course = input("Enter course name: ").strip()
    grade_input = input("Enter grade (0-20): ").strip()
    try:
        grade = float(grade_input)
    except ValueError:
        raise GradebookError("Grade must be a numeric value.")
    student.add_grade(course, grade)
    print("Grade updated for " + student.name + " in " + course + ".")

def show_failing_students(gb):
    failing = [s for s in gb.students.values() if not s.is_passing()]
    if not failing:
        print("No failing students found.")
    else:
        print("Failing Students:")
        for s in failing:
            print("- " + s.name + " (ID: " + s.student_id + ") - Avg: " + "{:.2f}".format(s.calculate_average()))

def show_ranking(gb):
    if not gb.students:
        print("No students recorded.")
    else:
        ranked = sorted(gb.students.values(), key=lambda s: s.calculate_average(), reverse=True)
        print("Student Ranking (Highest to Lowest Average):")
        for rank, s in enumerate(ranked, 1):
            print(str(rank) + ". " + s.name + " (ID: " + s.student_id + ") - Avg: " + "{:.2f}".format(s.calculate_average()))

def show_common_courses(gb):
    sid1 = input("Enter first student ID: ").strip()
    sid2 = input("Enter second student ID: ").strip()
    s1 = gb.get_student(sid1)
    s2 = gb.get_student(sid2)
    common = set(s1.grades.keys()).intersection(set(s2.grades.keys()))
    if not common:
        print("Students " + s1.name + " and " + s2.name + " have no courses in common.")
    else:
        print("Common courses between " + s1.name + " and " + s2.name + ": " + ", ".join(common))


def main():
    gb = Gradebook()
    db_file = "gradebook_data.json"

    try:
        gb.load_from_file(db_file)
    except Exception:
        pass

    while True:
        show_menu()

        choice = input("Enter choice (1-7): ").strip()

        try:
            # Scrambled order of checks
            if choice == "3":
                show_all_students(gb)

            elif choice == "1":
                add_new_student(gb)

            elif choice == "2":
                update_grade(gb)

            elif choice == "5":
                show_failing_students(gb)

            elif choice == "4":
                show_ranking(gb)

            elif choice == "6":
                show_common_courses(gb)

            elif choice == "7":
                gb.save_to_file(db_file)
                print("Gradebook data saved to JSON file. Exiting program. Goodbye!")
                break

            else:
                print("Invalid menu option. Please choose between 1 and 7.")

        except GradebookError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("An unexpected error occurred: " + str(e))

if __name__ == "__main__":
    main()