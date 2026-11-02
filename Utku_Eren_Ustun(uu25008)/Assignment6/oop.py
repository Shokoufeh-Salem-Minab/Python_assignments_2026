students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

class Student:
    def __init__(self, data):
        self.name = data["name"]
        self.exams = [data["exam1"], data["exam2"], data["exam3"]]
        self.homework = data["homework"]

    def exam_avg(self):
        return sum(self.exams) / 3

    def hw_score(self):
        return (self.homework / 10) * 100

    def final_score(self):
        return 0.7 * self.exam_avg() + 0.3 * self.hw_score()

    def status(self):
        return "Pass" if self.final_score() >= 60 else "Fail"

    def is_excellent(self):
        return all(e >= 90 for e in self.exams)

    def recovery_score(self):
        return min(self.final_score() + 5, 100) if self.final_score() < 60 else None

class Classroom:
    def __init__(self, student_list):
        self.students = [Student(s) for s in student_list]

    def class_average(self):
        return sum(s.final_score() for s in self.students) / len(self.students)

    def filter_excellent(self):
        return [s.name for s in self.students if s.is_excellent()]

    def rank_students(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)

room = Classroom(students)
print("Class Average:", round(room.class_average(), 2))
print("Excellent Students:", room.filter_excellent())
print("Ranked:", [(s.name, round(s.final_score(), 2), s.status(), s.recovery_score()) for s in room.rank_students()])