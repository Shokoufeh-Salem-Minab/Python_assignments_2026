# Homework 6 - Object-oriented programming

students_data = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
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
        return self.homework / 10 * 100

    def final_score(self):
        return self.exam_average() * 0.7 + self.homework_score() * 0.3

    def status(self):
        if self.final_score() >= 60:
            return "Pass"
        return "Fail"

    def is_excellent(self):
        return self.exam1 >= 90 and self.exam2 >= 90 and self.exam3 >= 90

    def recovery_score(self):
        final = self.final_score()
        if final < 60:
            return min(final + 5, 100)
        return None


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

    def get_passed(self):
        passed = []
        for s in self.students:
            if s.status() == "Pass":
                passed.append(s)
        return passed

    def get_failed(self):
        failed = []
        for s in self.students:
            if s.status() == "Fail":
                failed.append(s)
        return failed

    def get_excellent(self):
        result = []
        for s in self.students:
            if s.is_excellent():
                result.append(s)
        return result

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


# create the classroom and add students
room = Classroom()
for d in students_data:
    s = Student(d["name"], d["exam1"], d["exam2"], d["exam3"], d["homework"])
    room.add_student(s)

print("Student results:")
for s in room.students:
    print(s.name, "- final score:", round(s.final_score(), 2), "-", s.status())
    if s.is_excellent():
        print("   Excellent performance!")
    if s.recovery_score() is not None:
        print("   Recovery score:", round(s.recovery_score(), 2))

print("\nClass average:", round(room.class_average(), 2))

print("\nPassed students:")
for s in room.get_passed():
    print(s.name)

print("\nFailed students:")
for s in room.get_failed():
    print(s.name)

print("\nExcellent students:")
for s in room.get_excellent():
    print(s.name)

print("\nRanking:")
place = 1
for s in room.ranking():
    print(place, s.name, round(s.final_score(), 2))
    place += 1