# Homework 6 
# Srivishva Melvin Marimouttou, sm25017
# Program created on: 27/10/2026

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]

class Student:
    def __init__(self, name, exams, homework):
        self.name = name
        self.exams = exams # list of 3 exam scores
        self.homework = homework # number of submitted assignments (out of 10)

    def exam_average(self):
        return sum(self.exams) / len(self.exams)

    def homework_score(self):
        return (self.homework / 10) * 100

    def final_score(self):
        return (0.7 * self.exam_average()) + (0.3 * self.homework_score())

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
        if self.final_score() < 60:
            return min(self.final_score() + 5, 100)
        return None

    def __str__(self):
        return self.name + " " + str(round(self.final_score(), 2)) + " " + self.status()

class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        total = 0
        for s in self.students:
            total = total + s.final_score()
        return total / len(self.students)

    def passing_students(self):
        return [s for s in self.students if s.status() == "Pass"]

    def excellent_students(self):
        return [s for s in self.students if s.is_excellent()]

    def needing_recovery(self):
        return [s for s in self.students if s.recovery_score() is not None]

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)

classroom = Classroom()
for data in students:
    exams = [data["exam1"], data["exam2"], data["exam3"]]
    classroom.add_student(Student(data["name"], exams, data["homework"]))

print("Name Final Status")
for s in classroom.students:
    print(s)

print("\nPassing students:", ", ".join([s.name for s in classroom.passing_students()]))
print("Excellent students:", ", ".join([s.name for s in classroom.excellent_students()]))

print("\nRecovery scores:")
for s in classroom.needing_recovery():
    print(s.name + ":", round(s.final_score(), 2), "to", round(s.recovery_score(), 2), "(status stays", s.status() + ")")

print("\nClass average:", round(classroom.class_average(), 2))

print("\nRanking:")
place = 1
for s in classroom.ranking():
    print(str(place) + ".", s.name, "-", round(s.final_score(), 2))
    place += 1
