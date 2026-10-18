import json

class InvalidGrade(Exception):
    pass

class Student:
    minimum_grade = 0
    maximum_grade = 20
    passing_grade = 10

    def __init__(self, grades):
        for grade in grades.values():
            self.checkGrade(grade)

        self.grades = dict(grades)
        self.average = 0
        self.calculateAverage()

    def __str__(self):
         return json.dumps({
                     "grades": self.grades,
                 })

    def checkGrade(self, grade):
        if (isinstance(grade, bool)
                or not isinstance(grade, (int, float))
                or not (self.minimum_grade <= grade <= self.maximum_grade)):
            raise InvalidGrade("Invalid grade")

    def calculateAverage(self):
        course_num = len(self.grades)

        if(course_num ==0):
            self.average = 0
            return
        
        course_total = 0

        for grade in self.grades.values():
            course_total +=grade

        self.average = course_total/course_num

    def bestCourse(self):
        if not self.grades:
            return (None, None)

        course = max(self.grades, key=self.grades.get)
        return (course, self.grades[course])
    
    def addGrade(self, course, grade):
        if isinstance(grade, str):
            try:
                grade = float(grade)
            except ValueError:
                raise InvalidGrade("Invalid grade")

        self.checkGrade(grade)

        self.grades[course] = grade
        self.calculateAverage()

class GraduateStudent(Student):
    passing_grade = 14

    def __init__(self, grades, thesis_title):
        super().__init__(grades)
        self.thesis_title = thesis_title

    def __str__(self):
        return json.dumps({
            "grades": self.grades,
            "thesis_title": self.thesis_title
        })
