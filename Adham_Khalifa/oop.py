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
        return "Pass" if self.final_score() >= 60 else "Fail"

    def excellent(self):
        return self.exam1 >= 90 and self.exam2 >= 90 and self.exam3 >= 90

    def recovery_score(self):
        score = self.final_score()
        return min(score + 5, 100) if score < 60 else score


class Classroom:
    def __init__(self, students):
        self.students = students

    def class_average(self):
        total = 0
        for student in self.students:
            total += student.final_score()
        return total / len(self.students)

    def passed_students(self):
        passed = []
        for student in self.students:
            if student.status() == "Pass":
                passed.append(student)
        return passed

    def ranking(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)


students = [
    Student("Anna",85,90,88,9), Student("Peter",55,60,58,6),
    Student("Maria",95,92,98,10), Student("John",70,65,72,8),
    Student("Sofia",40,50,45,5), Student("David",88,91,86,10)
]
classroom = Classroom(students)

for s in students:
    print(s.name, round(s.final_score(),2), s.status(),
          "Excellent:", s.excellent(), "Recovery:", round(s.recovery_score(),2))
print("Class average:", round(classroom.class_average(),2))
print("Passed:", [s.name for s in classroom.passed_students()])
print("Ranking:", [s.name for s in classroom.ranking()])
