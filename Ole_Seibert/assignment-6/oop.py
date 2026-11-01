# Homework 6 - Part 2: Object-Oriented Programming

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


class Student:
    def __init__(self, name, exam1, exam2, exam3, homework):
        self.name = name
        self.exams = [exam1, exam2, exam3]
        self.homework = homework

    def exam_average(self):
        return sum(self.exams) / len(self.exams)

    def homework_score(self):
        return self.homework / 10 * 100

    def final_score(self):
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def status(self):
        if self.final_score() >= 60:
            return "Pass"
        return "Fail"

    def is_excellent(self):
        for exam in self.exams:
            if exam < 90:
                return False
        return True

    def recovery_score(self):
        # only for students below 60, status is not changed
        if self.final_score() < 60:
            return min(self.final_score() + 5, 100)
        return None

    def __str__(self):
        return f"{self.name:6} | exam avg: {self.exam_average():.2f} | final: {self.final_score():.2f} | {self.status()}"


class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        total = 0
        for s in self.students:
            total += s.final_score()
        return total / len(self.students)

    def passed_students(self):
        return [s for s in self.students if s.status() == "Pass"]

    def failed_students(self):
        return [s for s in self.students if s.status() == "Fail"]

    def excellent_students(self):
        return [s for s in self.students if s.is_excellent()]

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


classroom = Classroom()
for d in students:
    classroom.add_student(Student(d["name"], d["exam1"], d["exam2"], d["exam3"], d["homework"]))

print("=== All students ===")
for s in classroom.students:
    print(s)

print("\nPassed:", [s.name for s in classroom.passed_students()])
print("Failed:", [s.name for s in classroom.failed_students()])
print("Excellent:", [s.name for s in classroom.excellent_students()])

print("\n=== Recovery scores ===")
for s in classroom.failed_students():
    print(f"{s.name}: {s.final_score():.2f} -> {s.recovery_score():.2f} (status: {s.status()})")

print(f"\nClass average: {classroom.class_average():.2f}")

print("\n=== Ranking ===")
for i, s in enumerate(classroom.ranking(), start=1):
    print(f"{i}. {s.name} - {s.final_score():.2f}")
