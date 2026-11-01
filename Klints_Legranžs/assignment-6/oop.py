"""Task 2 - Object-oriented programming: Student and Classroom classes."""
from data import (students, PASS_MARK, EXCELLENT_MARK, RECOVERY_BONUS,
                  EXAM_WEIGHT, HOMEWORK_WEIGHT)


class Student:
    def __init__(self, name, exam1, exam2, exam3, homework):
        self.name = name
        self.exams = (exam1, exam2, exam3)
        self.homework = homework

    def exam_average(self):
        return sum(self.exams) / len(self.exams)

    def homework_score(self):
        return self.homework / 10 * 100

    def final_score(self):
        return EXAM_WEIGHT * self.exam_average() + HOMEWORK_WEIGHT * self.homework_score()

    def has_passed(self):
        return self.final_score() >= PASS_MARK

    def status(self):
        return "Pass" if self.has_passed() else "Fail"

    def is_excellent(self):
        return all(e >= EXCELLENT_MARK for e in self.exams)

    def recovery_score(self):
        """+5 (max 100) for students below 60; original status is unchanged."""
        if self.final_score() < PASS_MARK:
            return min(self.final_score() + RECOVERY_BONUS, 100)
        return None

    def __repr__(self):
        return f"Student({self.name!r}, final={self.final_score():.2f})"


class Classroom:
    def __init__(self, students=None):
        self.students = list(students or [])

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        return sum(s.final_score() for s in self.students) / len(self.students)

    def passed(self):
        return [s for s in self.students if s.has_passed()]

    def failed(self):
        return [s for s in self.students if not s.has_passed()]

    def excellent(self):
        return [s for s in self.students if s.is_excellent()]

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


def main():
    room = Classroom(Student(**d) for d in students)

    print("=== OOP ===")
    for s in room.students:
        line = (f"{s.name:<6} exam_avg={s.exam_average():.2f} hw={s.homework_score():.0f} "
                f"final={s.final_score():.2f} {s.status()}")
        if s.is_excellent():
            line += " | EXCELLENT"
        if s.recovery_score() is not None:
            line += f" | recovery={s.recovery_score():.2f}"
        print(line)

    print(f"\nClass average: {room.class_average():.2f}")
    print("Passed:   ", [s.name for s in room.passed()])
    print("Failed:   ", [s.name for s in room.failed()])
    print("Excellent:", [s.name for s in room.excellent()])
    print("Ranking:")
    for place, s in enumerate(room.ranking(), start=1):
        print(f"  {place}. {s.name:<6} {s.final_score():.2f}")


if __name__ == "__main__":
    main()
