from data import students, PASS_SCORE, EXCELLENT_SCORE, RECOVERY_POINTS, MAX_SCORE


# ----- Student Class -----
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
        if self.final_score() >= PASS_SCORE:
            return "Pass"
        return "Fail"

    def is_excellent(self):
        return all(exam >= EXCELLENT_SCORE for exam in self.exams)

    def recovery_score(self):
        # only students below the pass score get a recovery score
        if self.final_score() < PASS_SCORE:
            return min(self.final_score() + RECOVERY_POINTS, MAX_SCORE)
        return None

    def __str__(self):
        return f"{self.name}: {self.final_score():.2f} ({self.status()})"


# ----- Classroom Class -----
class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        total = sum(student.final_score() for student in self.students)
        return total / len(self.students)

    def excellent_students(self):
        return [student for student in self.students if student.is_excellent()]

    def failing_students(self):
        return [student for student in self.students if student.status() == "Fail"]

    def ranking(self):
        return sorted(self.students, key=lambda student: student.final_score(), reverse=True)


# ----- Report -----
def build_classroom():
    classroom = Classroom()
    for item in students:
        student = Student(item["name"], item["exam1"], item["exam2"], item["exam3"], item["homework"])
        classroom.add_student(student)
    return classroom


def main():
    classroom = build_classroom()
    print("===== OBJECT-ORIENTED PROGRAMMING =====")

    print("\n----- FINAL SCORES -----")
    for student in classroom.students:
        print(student)

    print("\n----- EXCELLENT STUDENTS -----")
    for student in classroom.excellent_students():
        print(student.name)

    print("\n----- RECOVERY SCORES -----")
    for student in classroom.failing_students():
        print(f"{student.name}: {student.final_score():.2f} -> {student.recovery_score():.2f} "
              f"(status stays {student.status()})")

    print(f"\nClass average: {classroom.class_average():.2f}")

    print("\n----- RANKING -----")
    for place, student in enumerate(classroom.ranking(), start=1):
        print(f"{place}. {student.name} - {student.final_score():.2f}")


main()
