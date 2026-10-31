# Assignment 6: student performance analysis using OOP.


class Student:
    def __init__(self, name, exam1, exam2, exam3, homework):
        self.name = name
        self.exam_scores = (exam1, exam2, exam3)
        self.homework = homework

    def exam_average(self):
        return sum(self.exam_scores) / len(self.exam_scores)

    def homework_score(self):
        return self.homework / 10 * 100

    def final_score(self):
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def status(self):
        return "Pass" if self.final_score() >= 60 else "Fail"

    def is_excellent(self):
        return all(score >= 90 for score in self.exam_scores)

    def recovery_score(self):
        return min(self.final_score() + 5, 100) if self.final_score() < 60 else None


class Classroom:
    def __init__(self, students):
        self.students = list(students)

    def class_average(self):
        return sum(student.final_score() for student in self.students) / len(self.students)

    def passing_students(self):
        return [student for student in self.students if student.status() == "Pass"]

    def excellent_students(self):
        return [student for student in self.students if student.is_excellent()]

    def rank_students(self):
        return sorted(self.students, key=lambda student: student.final_score(), reverse=True)


def create_classroom():
    records = [
        ("Anna", 85, 90, 88, 9), ("Peter", 55, 60, 58, 6),
        ("Maria", 95, 92, 98, 10), ("John", 70, 65, 72, 8),
        ("Sofia", 40, 50, 45, 5), ("David", 88, 91, 86, 10),
    ]
    return Classroom(Student(*record) for record in records)


def main():
    classroom = create_classroom()
    print(f"Class average: {classroom.class_average():.2f}")
    print("Excellent students:", ", ".join(student.name for student in classroom.excellent_students()))
    for rank, student in enumerate(classroom.rank_students(), start=1):
        print(f"{rank}. {student.name}: {student.final_score():.2f} - {student.status()}")


if __name__ == "__main__":
    main()
