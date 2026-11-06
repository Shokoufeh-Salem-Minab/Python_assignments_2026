from dataclasses import dataclass
from data import students


@dataclass(frozen=True)
class Student:
    name: str
    exam1: float
    exam2: float
    exam3: float
    homework: float

    def exam_average(self):
        return (self.exam1 + self.exam2 + self.exam3) / 3

    def homework_score(self):
        return self.homework * 10

    def final_score(self):
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def status(self):
        return "Pass" if self.final_score() > 59 else "Fail"

    def is_excellent(self):
        return all(score > 89 for score in (self.exam1, self.exam2, self.exam3))

    def recovery_score(self):
        score = self.final_score()
        return min(score + 5, 100) if score < 60 else None


class Classroom:
    def __init__(self, students):
        self.students = list(students)

    def class_average(self):
        return sum(student.final_score() for student in self.students) / len(self.students)

    def filter_students(self, condition):
        return [student for student in self.students if condition(student)]

    def passing_students(self):
        return self.filter_students(lambda student: student.status() == "Pass")

    def excellent_students(self):
        return self.filter_students(lambda student: student.is_excellent())

    def recovery_students(self):
        return self.filter_students(lambda student: student.recovery_score() is not None)

    def rank_students(self):
        return sorted(self.students, key=lambda student: (-student.final_score(), student.name))


def main():
    classroom = Classroom([Student(**record) for record in students])
    print("OBJECT-ORIENTED PROGRAMMING")
    print("Rank | Name   | Final | Status | Excellent | Recovery")
    for rank, student in enumerate(classroom.rank_students(), start=1):
        recovery = student.recovery_score()
        recovery_text = "-" if recovery is None else f"{recovery:.2f}"
        print(f"{rank:>4} | {student.name:<6} | {student.final_score():>5.2f} | "
              f"{student.status():<6} | {str(student.is_excellent()):<9} | {recovery_text}")

    print(f"\nClass average: {classroom.class_average():.2f}")
    print("Passing students:", [s.name for s in classroom.passing_students()])
    print("Excellent students:", [s.name for s in classroom.excellent_students()])
    print("Recovery students:", [s.name for s in classroom.recovery_students()])


if __name__ == "__main__":
    main()
