import json

# Custom exceptions
class InvalidGradeError(Exception):
    pass

class StudentNotFoundError(Exception):
    pass


class Student:
    passing_grade = 10.0

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  # Dictionary: {course: grade}

    def add_grade(self, course, grade):
        if not (0 <= grade <= 20):
            raise InvalidGradeError("Grade must be between 0 and 20.")
        self.grades[course] = grade

    def get_average(self):
        return sum(self.grades.values()) / len(self.grades) if self.grades else 0.0

    def get_best_course(self):
        # Tuple return: (course, grade)
        if not self.grades:
            return ("None", 0.0)
        best = max(self.grades, key=self.grades.get)
        return (best, self.grades[best])

    def __str__(self):
        # Tuple unpacking
        course, grade = self.get_best_course()
        return f"[{self.student_id}] {self.name} | Avg: {self.get_average():.1f} | Best: {course} ({grade})"


class GraduateStudent(Student):
    passing_grade = 14.0  # Higher passing threshold

    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title

    def __str__(self):
        course, grade = self.get_best_course()
        return f"[{self.student_id}] {self.name} (Grad - {self.thesis_title}) | Avg: {self.get_average():.1f} | Best: {course} ({grade})"


class Gradebook:
    def __init__(self, filename="gradebook.json"):
        self.filename = filename
        self.students = {}  # Dictionary: {student_id: Student}

    def __len__(self):
        return len(self.students)

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f"Student ID '{student_id}' not found.")
        return self.students[student_id]

    def get_unique_courses(self):
        # Set: all unique courses across students
        courses = set()
        for s in self.students.values():
            courses.update(s.grades.keys())
        return courses

    def get_common_courses(self, id1, id2):
        # Set operation: intersection of two students' courses
        s1 = self.get_student(id1)
        s2 = self.get_student(id2)
        return set(s1.grades.keys()) & set(s2.grades.keys())

    def get_ranking(self):
        # sorted() with lambda
        return sorted(self.students.values(), key=lambda s: s.get_average(), reverse=True)

    def get_failing_students(self):
        # List comprehension
        return [s for s in self.students.values() if s.get_average() < s.passing_grade]

    def save(self):
        data = {}
        for sid, s in self.students.items():
            data[sid] = {
                "name": s.name,
                "grades": s.grades,
                "thesis": getattr(s, "thesis_title", None)
            }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                for sid, info in data.items():
                    if info["thesis"]:
                        s = GraduateStudent(sid, info["name"], info["thesis"])
                    else:
                        s = Student(sid, info["name"])
                    s.grades = info["grades"]
                    self.students[sid] = s
        except FileNotFoundError:
            pass


def main():
    gb = Gradebook()
    gb.load()

    while True:
        print("\n--- Menu ---")
        print("1. Add student\n2. Add/update grade\n3. Show all\n4. Show ranking")
        print("5. Show failing\n6. Common courses\n7. Save and exit")

        choice = input("Choose (1-7): ").strip()

        try:
            if choice == "1":
                sid = input("ID: ").strip()
                if sid in gb.students:
                    print("Error: Student ID already exists.")
                    continue
                name = input("Name: ").strip()
                is_grad = input("Graduate? (y/n): ").strip().lower() == "y"
                if is_grad:
                    thesis = input("Thesis: ").strip()
                    gb.students[sid] = GraduateStudent(sid, name, thesis)
                else:
                    gb.students[sid] = Student(sid, name)
                print("Student added.")

            elif choice == "2":
                sid = input("Student ID: ").strip()
                student = gb.get_student(sid)  # Raises StudentNotFoundError if missing
                course = input("Course name: ").strip()
                grade = float(input("Grade (0-20): "))
                student.add_grade(course, grade)
                print("Grade saved.")

            elif choice == "3":
                print(f"Total students: {len(gb)}")
                unique_courses = gb.get_unique_courses()
                print(f"All offered courses: {', '.join(unique_courses) if unique_courses else 'None'}")
                for s in gb.students.values():
                    print(s)

            elif choice == "4":
                for rank, s in enumerate(gb.get_ranking(), 1):
                    print(f"{rank}. {s.name} | Avg: {s.get_average():.1f}")

            elif choice == "5":
                failing = gb.get_failing_students()
                print("Failing students:" if failing else "No failing students.")
                for s in failing:
                    print(f"- {s.name} (Avg: {s.get_average():.1f}, Passing: {s.passing_grade})")

            elif choice == "6":
                id1 = input("First student ID: ").strip()
                id2 = input("Second student ID: ").strip()
                common = gb.get_common_courses(id1, id2)  # Handles lookups via get_student
                print(f"Common courses: {', '.join(common) if common else 'None'}")

            elif choice == "7":
                gb.save()
                print("Saved. Goodbye!")
                break

            else:
                print("Invalid choice, pick 1-7.")

        except ValueError:
            print("Error: Expected a valid number.")
        except (InvalidGradeError, StudentNotFoundError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()