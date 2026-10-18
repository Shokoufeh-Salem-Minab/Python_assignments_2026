import json
import os

import student as student_classes

class InvalidOperation(Exception):
    pass



class Gradebook:
    filename = "gradebook.json"
    

    def __init__(self):
            self.students = {}
            self.courses = set()

    def __len__(self):
        return len(self.students)

    # Storage

    def saveToStorage(self):
        students_data = {}

        for student_id, student in self.students.items():
            if isinstance(student, student_classes.GraduateStudent):
                student_type = "graduate"
            else:
                student_type = "student"

            students_data[student_id] = {
                "type": student_type,
                "grades": student.grades,
                "thesis_title": getattr(student, "thesis_title", None)
            }

        data = {
            "students": students_data,
            "courses": list(self.courses)
        }

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)
        

    def loadFromStorage(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

            self.students = {}
            for student_id, info in data["students"].items():
                if info["type"] == "graduate":
                    student = student_classes.GraduateStudent(info["grades"], info["thesis_title"])
                else:
                    student = student_classes.Student(info["grades"])
                self.students[int(student_id)] = student

            self.courses = set(data["courses"])
        else:
            # no exception - no file saved means no info to load
            return

    # Menu functions

    def addStudent(self, student):
        if not isinstance(student, student_classes.Student):
            raise InvalidOperation("Expected input type: student")
    
        id = 0 

        while id in self.students.keys():
            id +=1

        self.courses.update(set(student.grades.keys()))
             
        self.students[id] = student

        print(f"Student added! Student id: {id}")

    def addGrade(self, student_id, course, grade):
        if student_id not in self.students.keys():
            raise InvalidOperation("No such student")

        self.students[student_id].addGrade(course, grade)
        self.courses.add(course)

        print("Grade saved!")

    def showStudents(self):
        print("\n All students:\n")

        for student_id,student in self.students.items():
            best_course, best_grade = student.bestCourse()

            if best_course is None:
                best = "no grades yet"
            else:
                best = f"{best_course} ({best_grade})"

            print(f"Student id: {student_id} \n Student average: {student.average:.2f}\n Best course: {best}\n All info: {student} ")

    def showRanking(self):
        print("\n Ranking:\n")

        students_sorted = sorted(
        self.students.items(),
        key=lambda item: item[1].average,
        reverse=True
        )
    
        for student_id,student in students_sorted:
            print(f"Student id: {student_id} \n Student average: {student.average:.2f}")

    def showFailing(self):
        print("\nFailing students:\n")

        failing = [(student_id, student)
                   for student_id, student in self.students.items()
                   if student.average < student.passing_grade]

        for student_id, student in failing:
            print(f"Student id: {student_id}")
            print(f"Student average: {student.average:.2f}")

    def getCommonCourses(self, first_id, second_id):
            students = self.students

            if first_id not in students.keys() or second_id not in students.keys():
                 raise InvalidOperation("No such student")
            
            first_courses = set(self.students[first_id].grades.keys())
            second_courses = set(self.students[second_id].grades.keys())

            return first_courses.intersection(second_courses)

