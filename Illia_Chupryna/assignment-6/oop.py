students = [{'name': 'Anna', 'exam1': 85, 'exam2': 90, 'exam3': 88, 'homework': 9}, {'name': 'Peter', 'exam1': 55, 'exam2': 60, 'exam3': 58, 'homework': 6}, {'name': 'Maria', 'exam1': 95, 'exam2': 92, 'exam3': 98, 'homework': 10}, {'name': 'John', 'exam1': 70, 'exam2': 65, 'exam3': 72, 'homework': 8}, {'name': 'Sofia', 'exam1': 40, 'exam2': 50, 'exam3': 45, 'homework': 5}, {'name': 'David', 'exam1': 88, 'exam2': 91, 'exam3': 86, 'homework': 10}]

class Student:
    def __init__(self, data):
        self.name = data["name"]
        self.exams = [data["exam1"], data["exam2"], data["exam3"]]
        self.homework = data["homework"]

    def exam_average(self):
        return sum(self.exams) / 3

    def homework_score(self):
        return self.homework * 10

    def final_score(self):
        return self.exam_average() * 0.7 + self.homework_score() * 0.3

    def status(self):
        return "Pass" if self.final_score() >= 60 else "Fail"

    def excellent(self):
        return all(x >= 90 for x in self.exams)

    def recovery_score(self):
        return min(self.final_score() + 5, 100) if self.status() == "Fail" else None


class Classroom:
    def __init__(self, data):
        self.students = [Student(s) for s in data]

    def average(self):
        return sum(s.final_score() for s in self.students) / len(self.students)

    def filter_students(self, condition):
        return [s for s in self.students if condition(s)]

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


room = Classroom(students)
for s in room.ranking():
    print(s.name, round(s.final_score(), 2), s.status())
print("Class average:", round(room.average(), 2))
print("Excellent:", [s.name for s in room.filter_students(lambda x: x.excellent())])
print("Failing:", [s.name for s in room.filter_students(lambda x: x.status() == "Fail")])
print("Recovery:", [(s.name, round(s.recovery_score(), 2)) for s in room.filter_students(lambda x: x.status() == "Fail")])
