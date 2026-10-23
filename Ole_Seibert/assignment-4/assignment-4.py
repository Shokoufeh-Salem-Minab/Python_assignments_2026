# Homework 4 - Student Gradebook

import json

FILE_NAME = 'gradebook.json'


# my own exceptions
class InvalidGradeError(Exception):
    pass


class StudentNotFoundError(Exception):
    pass


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.grades = {}  # {course: grade}
        self.passing_grade = 10

    def add_grade(self, course, grade):
        if not (0 <= grade <= 20):
            raise InvalidGradeError('grade must be between 0 and 20')
        self.grades[course] = grade

    def average(self):
        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) / len(self.grades)

    def best_course(self):
        # returns a tuple (course, grade)
        best_course = ''
        best_grade = -1
        for course, grade in self.grades.items():
            if grade > best_grade:
                best_course = course
                best_grade = grade
        return (best_course, best_grade)

    def is_failing(self):
        return len(self.grades) > 0 and self.average() < self.passing_grade

    def to_dict(self):
        return {'type': 'regular', 'id': self.student_id,
                'name': self.name, 'grades': self.grades}

    def __str__(self):
        text = f'{self.student_id}: {self.name}'
        if len(self.grades) == 0:
            return text + ' (no grades yet)'
        course, grade = self.best_course()
        text += f', average {self.average():.2f}, best course {course} ({grade})'
        text += f'\n   grades: {self.grades}'
        return text


class GraduateStudent(Student):
    def __init__(self, student_id, name, thesis_title):
        super().__init__(student_id, name)
        self.thesis_title = thesis_title
        self.passing_grade = 14

    def to_dict(self):
        data = super().to_dict()
        data['type'] = 'graduate'
        data['thesis_title'] = self.thesis_title
        return data

    def __str__(self):
        return super().__str__() + f'\n   thesis: {self.thesis_title}'


def student_from_dict(item):
    if item['type'] == 'graduate':
        student = GraduateStudent(item['id'], item['name'], item['thesis_title'])
    else:
        student = Student(item['id'], item['name'])
    student.grades = item['grades']
    return student


class Gradebook:
    def __init__(self):
        self.students = {}  # {student_id: Student}

    def __len__(self):
        return len(self.students)

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError('this student ID already exists')
        self.students[student.student_id] = student

    def get_student(self, student_id):
        if student_id not in self.students:
            raise StudentNotFoundError(f'no student with ID {student_id}')
        return self.students[student_id]

    def all_courses(self):
        courses = set()
        for student in self.students.values():
            for course in student.grades:
                courses.add(course)
        return courses

    def common_courses(self, id1, id2):
        courses1 = set(self.get_student(id1).grades.keys())
        courses2 = set(self.get_student(id2).grades.keys())
        return courses1 & courses2

    def ranking(self):
        students = [s for s in self.students.values() if len(s.grades) > 0]
        return sorted(students, key=lambda s: s.average(), reverse=True)

    def failing_students(self):
        failing = [s for s in self.students.values() if s.is_failing()]
        return sorted(failing, key=lambda s: s.average())

    def save(self):
        data = [s.to_dict() for s in self.students.values()]
        with open(FILE_NAME, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def load(self):
        try:
            with open(FILE_NAME, 'r') as f:
                data = json.loads(f.read())
        except FileNotFoundError:
            print('No saved file found, starting with an empty gradebook.')
            return
        except json.JSONDecodeError:
            print('Saved file is broken, starting with an empty gradebook.')
            return
        for item in data:
            self.add_student(student_from_dict(item))
        print(f'Loaded {len(self)} students from {FILE_NAME}.')


def read_grade():
    text = input('Grade (0-20): ')
    try:
        return float(text)
    except ValueError:
        raise InvalidGradeError(f'"{text}" is not a number')


def add_student_menu(book):
    student_type = input('Regular or graduate student? (r/g): ').strip().lower()
    if student_type != 'r' and student_type != 'g':
        print('Please enter r or g.')
        return
    student_id = input('Student ID: ').strip()
    name = input('Name: ').strip()
    if student_id == '' or name == '':
        print('ID and name cannot be empty.')
        return
    if student_type == 'g':
        thesis = input('Thesis title: ').strip()
        book.add_student(GraduateStudent(student_id, name, thesis))
    else:
        book.add_student(Student(student_id, name))
    print(f'{name} was added.')


def add_grade_menu(book):
    student = book.get_student(input('Student ID: ').strip())
    course = input('Course: ').strip()
    if course == '':
        print('Course cannot be empty.')
        return
    grade = read_grade()
    student.add_grade(course, grade)
    print(f'{student.name} now has {grade} in {course}.')


def show_all_menu(book):
    if len(book) == 0:
        print('No students yet.')
        return
    print(f'There are {len(book)} students:')
    for student in book.students.values():
        print(student)
    print('All courses:', ', '.join(sorted(book.all_courses())))


def show_ranking_menu(book):
    ranking = book.ranking()
    if len(ranking) == 0:
        print('No grades yet.')
        return
    place = 1
    for student in ranking:
        print(f'{place}. {student.name} - average {student.average():.2f}')
        place += 1


def show_failing_menu(book):
    failing = book.failing_students()
    if len(failing) == 0:
        print('Nobody is failing.')
        return
    for student in failing:
        print(f'{student.name} - average {student.average():.2f}, '
              f'needs at least {student.passing_grade}')


def common_courses_menu(book):
    id1 = input('First student ID: ').strip()
    id2 = input('Second student ID: ').strip()
    common = book.common_courses(id1, id2)
    if len(common) == 0:
        print('They have no courses in common.')
    else:
        print('Common courses:', ', '.join(sorted(common)))


def print_menu():
    print('\n--- Student Gradebook ---')
    print('1. Add student (regular or graduate)')
    print('2. Add or update a grade')
    print('3. Show all students')
    print('4. Show ranking (highest to lowest average)')
    print('5. Show failing students')
    print('6. Show common courses of two students')
    print('7. Save and exit')


def handle_choice(book, choice):
    # returns False when the program should stop
    if choice == '1':
        add_student_menu(book)
    elif choice == '2':
        add_grade_menu(book)
    elif choice == '3':
        show_all_menu(book)
    elif choice == '4':
        show_ranking_menu(book)
    elif choice == '5':
        show_failing_menu(book)
    elif choice == '6':
        common_courses_menu(book)
    elif choice == '7':
        book.save()
        print('Data saved. Bye!')
        return False
    else:
        print('Invalid option, please choose 1-7.')
    return True


def main():
    book = Gradebook()
    book.load()
    running = True
    while running:
        print_menu()
        choice = input('Choose an option: ').strip()
        try:
            running = handle_choice(book, choice)
        except InvalidGradeError as e:
            print('Invalid grade:', e)
        except StudentNotFoundError as e:
            print('Error:', e)
        except ValueError as e:
            print('Error:', e)


main()
