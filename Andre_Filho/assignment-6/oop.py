# Andre Filho - Homework 6 - Student Performance Analysis System
# 2. Object-Oriented Programming

STUDENTS_DATA = [
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
        self.exam1 = exam1
        self.exam2 = exam2
        self.exam3 = exam3
        self.homework = homework

    def exam_average(self):
        return (self.exam1 + self.exam2 + self.exam3) / 3

    def homework_score(self):
        return (self.homework / 10) * 100

    def final_score(self):
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def passed(self):
        return self.final_score() >= 60

    def is_excellent(self):
        return self.exam1 >= 90 and self.exam2 >= 90 and self.exam3 >= 90

    def recovery_score(self):
        score = self.final_score()
        if score >= 60:
            return None
        return min(score + 5, 100)

    def status(self):
        return "Pass" if self.passed() else "Fail"

    def __repr__(self):
        return f"Student({self.name}, final={self.final_score():.2f}, {self.status()})"


class Classroom:
    def __init__(self, students):
        self.students = students

    def class_average(self):
        total = sum(student.final_score() for student in self.students)
        return total / len(self.students)

    def filter_passed(self):
        return [student for student in self.students if student.passed()]

    def filter_excellent(self):
        return [student for student in self.students if student.is_excellent()]

    def rank(self):
        return sorted(self.students, key=lambda student: student.final_score(), reverse=True)


if __name__ == "__main__":
    students = [Student(**data) for data in STUDENTS_DATA]
    classroom = Classroom(students)

    print("--- Student results ---")
    for student in students:
        line = (
            f"{student.name}: exam_avg={student.exam_average():.2f}, "
            f"hw_score={student.homework_score():.2f}, "
            f"final={student.final_score():.2f}, status={student.status()}"
        )
        if student.is_excellent():
            line += ", Excellent Performance"
        recovery = student.recovery_score()
        if recovery is not None:
            line += f", recovery_score={recovery:.2f}"
        print(line)

    print("\nExcellent students:", [s.name for s in classroom.filter_excellent()])
    print(f"\nClass average (final score): {classroom.class_average():.2f}")

    print("\nRanking (best to worst):")
    for position, student in enumerate(classroom.rank(), start=1):
        print(f"{position}. {student.name}")
