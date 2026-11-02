from students_data import students

class Student:
    passing_score = 60
    excellent_score = 90

    def __init__(self, name, exam1, exam2, exam3, homework):
        self.name = name
        self.exams = [exam1, exam2, exam3]
        self.homework = homework

    def __str__(self):
        return f"{self.name}: final {self.finalScore():.2f}, {self.status()}"

    def examAverage(self):
        return sum(self.exams) / len(self.exams)

    def homeworkScore(self):
        return self.homework / 10 * 100

    def finalScore(self):
        return 0.7 * self.examAverage() + 0.3 * self.homeworkScore()

    def isPassing(self):
        return self.finalScore() >= self.passing_score

    def status(self):
        if self.isPassing():
            return "Pass"
        return "Fail"

    def isExcellent(self):
        for exam in self.exams:
            if exam < self.excellent_score:
                return False
        return True

    def recoveryScore(self):
        if self.isPassing():
            return None
        return min(self.finalScore() + 5, 100)

class Classroom:
    def __init__(self):
        self.students = []

    def __len__(self):
        return len(self.students)

    def addStudent(self, student):
        self.students.append(student)

    def classAverage(self):
        if len(self.students) == 0:
            return 0

        total = 0
        for student in self.students:
            total += student.finalScore()

        return total / len(self.students)

    def passingStudents(self):
        return [student for student in self.students if student.isPassing()]

    def failingStudents(self):
        return [student for student in self.students if not student.isPassing()]

    def excellentStudents(self):
        return [student for student in self.students if student.isExcellent()]

    def ranking(self):
        return sorted(self.students, key=lambda student: student.finalScore(), reverse=True)

classroom = Classroom()

for data in students:
    classroom.addStudent(Student(data["name"], data["exam1"], data["exam2"], data["exam3"], data["homework"]))

print(f"Students in classroom: {len(classroom)}")
for student in classroom.students:
    print(student)

print(f"\nPassing: {[student.name for student in classroom.passingStudents()]}")
print(f"Failing: {[student.name for student in classroom.failingStudents()]}")
print(f"Excellent: {[student.name for student in classroom.excellentStudents()]}")

print("\nRecovery scores:")
for student in classroom.failingStudents():
    print(f"{student.name}: {student.recoveryScore():.2f} (status stays {student.status()})")

print(f"\nClass average: {classroom.classAverage():.2f}")

print("\nRanking:")
for place, student in enumerate(classroom.ranking(), start=1):
    print(f"{place}. {student.name} - {student.finalScore():.2f}")
