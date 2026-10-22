
import json

class InvalidGrade(Exception):
    pass

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    def average(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0

    def best_course(self):
        return max(self.grades.items(), key=lambda x: x[1]) if self.grades else ("None", 0)

    def __str__(self):
        return f"{self.student_id}: {self.name}, Grades: {self.grades}, Average: {self.average():.2f}"

class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title
        self.passing_grade = 14

    def __str__(self):
        return super().__str__() + f", Thesis: {self.thesis_title}"

class Gradebook:
    def __init__(self):
        self.students = {}

    def __len__(self):
        return len(self.students)

    def save(self):
        data = {}
        for sid, s in self.students.items():
            data[sid] = {
                "name": s.name,
                "grades": s.grades,
                "graduate": isinstance(s, GraduateStudent),
                "thesis": getattr(s, "thesis_title", "")
            }
        with open("gradebook.json", "w") as f:
            json.dump(data, f)

    def load(self):
        try:
            with open("gradebook.json", "r") as f:
                data = json.load(f)
            for sid, s in data.items():
                if s["graduate"]:
                    student = GraduateStudent(sid, s["name"], s["thesis"])
                else:
                    student = Student(sid, s["name"])
                student.grades = s["grades"]
                self.students[sid] = student
        except FileNotFoundError:
            pass

    def get_student(self, sid):
        if sid not in self.students:
            raise KeyError("Student ID not found")
        return self.students[sid]

    def courses(self):
        return {c for s in self.students.values() for c in s.grades}

def main():
    book = Gradebook()
    book.load()

    while True:
        print("\n1. Add student\n2. Add or update grade\n3. Show all students")
        print("4. Show ranking\n5. Show failing students\n6. Common courses\n7. Save and exit")
        choice = input("Choose: ")

        try:
            if choice == "1":
                sid = input("Student ID: ")
                if sid in book.students:
                    print("ID already exists")
                    continue
                name = input("Name: ")
                kind = input("Graduate student? (y/n): ").lower()
                if kind == "y":
                    thesis = input("Thesis title: ")
                    book.students[sid] = GraduateStudent(sid, name, thesis)
                else:
                    book.students[sid] = Student(sid, name)

            elif choice == "2":
                sid = input("Student ID: ")
                s = book.get_student(sid)
                course = input("Course: ")
                grade = float(input("Grade (0-20): "))
                if not 0 <= grade <= 20:
                    raise InvalidGrade("Grade must be between 0 and 20")
                s.grades[course] = grade

            elif choice == "3":
                for s in book.students.values():
                    print(s)
                    course, grade = s.best_course()
                    print("Best course:", course, grade)
                print("Total students:", len(book))

            elif choice == "4":
                ranking = sorted(book.students.values(), key=lambda s: s.average(), reverse=True)
                for s in ranking:
                    print(s.name, s.average())

            elif choice == "5":
                failing = [s for s in book.students.values()
                           if s.average() < getattr(s, "passing_grade", 10)]
                for s in failing:
                    print(s)

            elif choice == "6":
                s1 = book.get_student(input("First student ID: "))
                s2 = book.get_student(input("Second student ID: "))
                print(set(s1.grades) & set(s2.grades))

            elif choice == "7":
                book.save()
                print("Saved. Goodbye!")
                break

            else:
                print("Invalid menu choice")

        except (ValueError, InvalidGrade, KeyError) as e:
            print("Error:", e)

    book.save()

if __name__ == "__main__":
    main()
