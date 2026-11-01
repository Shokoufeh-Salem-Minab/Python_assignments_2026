# Task 2: Object-oriented programming
# Student = one student, it knows how to calculate its own scores.
# Classroom = holds all the students and does stuff with the whole group.


# the dataset from the homework
students = [
    {"name": "Anna",  "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John",  "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def check_students(data):
    # small safety check so the programs stop with a clear message
    # if the data is broken (empty list, missing key, score out of range)
    if len(data) == 0:
        raise ValueError("the student list is empty")

    for s in data:
        for key in ["name", "exam1", "exam2", "exam3", "homework"]:
            if key not in s:
                raise ValueError(f"student {s} is missing the key '{key}'")

        for key in ["exam1", "exam2", "exam3", "homework"]:
            value = s[key]
            # bool is also a number in python so i block it separately
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{s['name']}: {key} must be a number")

        for key in ["exam1", "exam2", "exam3"]:
            if s[key] < 0 or s[key] > 100:
                raise ValueError(f"{s['name']}: {key} must be between 0 and 100")

        # homework is how many of the 10 assignments were submitted
        if s["homework"] < 0 or s["homework"] > 10:
            raise ValueError(f"{s['name']}: homework must be between 0 and 10")


class Student:
    def __init__(self, name, exams, homework):
        self.name = name
        self.exams = exams          # list with the 3 exam scores
        self.homework = homework    # how many assignments were submitted (out of 10)

    def exam_average(self):
        return sum(self.exams) / len(self.exams)

    def homework_score(self):
        return self.homework / 10 * 100

    def final_score(self):
        # 70% exams + 30% homework
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def status(self):
        # 60 or more = Pass
        if self.final_score() >= 60:
            return "Pass"
        return "Fail"

    def is_excellent(self):
        # all exams 90+
        return all(score >= 90 for score in self.exams)

    def recovery_score(self):
        # only students under 60 get it, everyone else gets None
        # status() is not touched so a failed student is still Fail
        final = self.final_score()
        if final < 60:
            return min(final + 5, 100)
        return None

    def __str__(self):
        return f"{self.name} (final {self.final_score():.2f}, {self.status()})"


class Classroom:
    def __init__(self):
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def class_average(self):
        if len(self.students) == 0:
            return 0  # empty class, avoid dividing by zero
        total = sum(s.final_score() for s in self.students)
        return total / len(self.students)

    def filter_students(self, condition):
        # general filter, i give it a function that says True/False for a student
        return [s for s in self.students if condition(s)]

    def passed(self):
        return self.filter_students(lambda s: s.status() == "Pass")

    def failed(self):
        return self.filter_students(lambda s: s.status() == "Fail")

    def excellent(self):
        return self.filter_students(lambda s: s.is_excellent())

    def ranking(self):
        # highest final score first (sorted keeps the old order if scores are equal)
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


def main():
    check_students(students)

    room = Classroom()
    for d in students:
        exams = [d["exam1"], d["exam2"], d["exam3"]]
        room.add_student(Student(d["name"], exams, d["homework"]))

    print("--- OOP ---")
    for s in room.students:
        line = f"{s.name:6} final={s.final_score():.2f} status={s.status()}"
        if s.is_excellent():
            line += " | Excellent Performance"
        if s.recovery_score() is not None:
            line += f" | recovery={s.recovery_score():.2f}"
        print(line)

    print(f"\nClass average: {room.class_average():.2f}")
    print("Passed:   ", [s.name for s in room.passed()])
    print("Failed:   ", [s.name for s in room.failed()])
    print("Excellent:", [s.name for s in room.excellent()])

    print("\nRanking:")
    place = 1
    for s in room.ranking():
        print(f"{place}. {s}")
        place += 1


if __name__ == "__main__":
    main()
