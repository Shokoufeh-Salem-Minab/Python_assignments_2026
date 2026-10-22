class GradeValidationError(Exception):
    pass


class Student:

    PASSING_GRADE = 10

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}

    
    def add_grade(self, course, grade):
        if grade < 0 or grade > 20:
            raise GradeValidationError("Grade must be between 0 and 20.")

        self.grades[course] = grade


    def average_grade(self):
        if len(self.grades) == 0:
            return None

        return sum(self.grades.values()) / len(self.grades)

    
    def best_course(self):
        if len(self.grades) == 0:
            return None
        
        best_course = None
        best_grade = -1

        for course, grade in self.grades.items():
            if grade > best_grade:
                best_course = course
                best_grade = grade
        
        return best_course, best_grade

    
    def is_failing(self):
        average = self.average_grade()

        return average is not None and average < self.PASSING_GRADE

    
    def __str__(self):
        return f"{self.student_id} - {self.name} - Grades: {self.grades}"

    
    def to_dict(self):
        return {
            "type": "student",
            "student_id": self.student_id,
            "name": self.name,
            "grades": self.grades
        }

    
class GraduateStudent(Student):

    PASSING_GRADE = 14

    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title


    def __str__(self):
        data = super().to_dict()
        data["type"] = "graduate"
        data["thesis_title"] = self.thesis_title
        return data
