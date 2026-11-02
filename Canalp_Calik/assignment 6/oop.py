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
        self.exam1 = data["exam1"]
        self.exam2 = data["exam2"]
        self.exam3 = data["exam3"]
        self.homework = data["homework"]

    def exam_avg(self): 
        return (self.exam1 + self.exam2 + self.exam3) / 3
        
    def hw_score(self): 
        return (self.homework / 10) * 100
        
    def final_score(self): 
        return 0.7 * self.exam_avg() + 0.3 * self.hw_score()
        
    def status(self): 
        return "Pass" if self.final_score() >= 60 else "Fail"
        
    def excellent(self): 
        return self.exam1 >= 90 and self.exam2 >= 90 and self.exam3 >= 90
        
    def recovery(self):
        fs = self.final_score()
        return min(fs + 5, 100) if fs < 60 else None

class Classroom:
    def __init__(self, students_data):
        self.students = [Student(s) for s in students_data]

    def class_average(self):
        return sum(s.final_score() for s in self.students) / len(self.students)

    def filter_students(self, status):
        return [s for s in self.students if s.status() == status]

    def rank_students(self):
        return sorted(self.students, key=lambda s: s.final_score(), reverse=True)

classroom = Classroom(students)
oop_avg = classroom.class_average()
oop_passed = classroom.filter_students("Pass")
oop_ranked = classroom.rank_students()
