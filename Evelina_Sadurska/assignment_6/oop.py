students = [{"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
            {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
            {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
            {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
            {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
            {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}]


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
        return (self.homework / 10) * 100

    def final_score(self):
        return 0.7 * self.exam_average() + 0.3 * self.homework_score()

    def final_passed(self):
        if self.final_score() >= 60:
            return True
        return False

    def status(self):
        if self.final_passed():
            return "Pass"
        return "Fail"

    def excellent_score(self):
        if self.exam1 >= 90 and self.exam2 >= 90 and self.exam3 >= 90:
            return True
        return False

    def recovery_score(self):
        if self.final_score() < 60:
            return min(self.final_score() + 5, 100)
        return None


class Classroom:
    def __init__(self, students):
        self.students = students          # list of Student objects

    def class_average(self):
        total = 0
        for student in self.students:
            total += student.final_score()
        return total / len(self.students)

    def passed_students(self):
        result = []
        for student in self.students:
            if student.final_passed():
                result.append(student)
        return result

    def failed_students(self):
        result = []
        for student in self.students:
            if not student.final_passed():
                result.append(student)
        return result

    def excellent_students(self):
        result = []
        for student in self.students:
            if student.excellent_score():
                result.append(student)
        return result

    def ranking(self):
        return sorted(self.students, key=lambda student: student.final_score(), reverse=True)


student_objects = []
for s in students:
    student_objects.append(Student(s["name"], s["exam1"], s["exam2"], s["exam3"], s["homework"]))

classroom = Classroom(student_objects)


print("Student results:")
for student in classroom.students:
    print(student.name, round(student.exam_average(), 2), round(student.homework_score(), 2),
          round(student.final_score(), 2), student.status())

print("Passed students:")
for student in classroom.passed_students():
    print(student.name)

print("Failed students:")
for student in classroom.failed_students():
    print(student.name)

print("Students who qualify for Excellent Performance:")
for student in classroom.excellent_students():
    print(student.name)

print("Student recovery scores:")
for student in classroom.failed_students():
    print(student.name, "recovery score:", round(student.recovery_score(), 2), student.status())

print(f"Class average: {round(classroom.class_average(), 2)}")

print("Ranking:")
position = 1
for student in classroom.ranking():
    print(position, ".", student.name, round(student.final_score(), 2))
    position += 1


# Comparison and reflection - Object-Oriented Programming:
# Unlike the procedural version, the data and the functions that use it live together
# inside classes: a Student knows its own scores and how to calculate its result, and a
# Classroom manages a group of students. Strengths: the code is well organised, easy to
# reuse and easy to extend (for example, adding a new method or a new type of student).
# Limitations: it needs more code and planning up front, which feels like overkill for
# a small task like this one.
