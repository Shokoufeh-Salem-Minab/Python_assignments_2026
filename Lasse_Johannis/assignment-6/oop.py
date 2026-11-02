# Homework 6 - Student Performance Analysis System
# Part 2: Object-Oriented Programming
# Lasse Johannis

from dataset import students


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

    # only for failed students, the status does not change
    def recovery_score(self):
        return min(self.final_score() + 5, 100)

    def __str__(self):
        return f"{self.name}: {self.final_score():.2f} ({self.status()})"


class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        total = 0
        for student in self.students:
            total += student.final_score()
        return total / len(self.students)

    def filter_by_status(self, status):
        return [student for student in self.students if student.status() == status]

    def excellent_students(self):
        return [student for student in self.students if student.is_excellent()]

    def ranking(self):
        return sorted(self.students, key=lambda student: student.final_score(), reverse=True)


classroom = Classroom()
for data in students:
    classroom.add_student(Student(data["name"], data["exam1"], data["exam2"], data["exam3"], data["homework"]))

print("Final scores:")
for student in classroom.students:
    print(student)

print("\nPassed:", [student.name for student in classroom.filter_by_status("Pass")])
print("Failed:", [student.name for student in classroom.filter_by_status("Fail")])
print("Excellent:", [student.name for student in classroom.excellent_students()])

print("\nRecovery scores:")
for student in classroom.filter_by_status("Fail"):
    print(f"{student.name}: {student.recovery_score():.2f} (status stays {student.status()})")

print(f"\nClass average: {classroom.class_average():.2f}")

print("\nRanking:")
place = 1
for student in classroom.ranking():
    print(f"{place}. {student.name} - {student.final_score():.2f}")
    place += 1
