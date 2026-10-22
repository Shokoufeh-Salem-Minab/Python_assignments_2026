from student import Student, GraduateStudent, GradeValidationError
from gradebook import Gradebook



def add_student(gradebook):
    student_type = input("Regular or graduate student? (1 | 2): ")
    student_id = input("Student ID: ").strip()
    name = input("Student name: ").strip()

    if not student_id or not name:
        print("Student ID and name cannot be empty.")
        return

    if student_type == "1":
        student = Student(student_id, name)

    elif student_type == "2":
        thesis_title = input("Thesis title: ").strip()

        if not thesis_title:
            print("Thesis title cannot be empty.")
            return

        student = GraduateStudent(student_id, name, thesis_title)

    else:
        print("Invalid student type.")
        return

    try:
        gradebook.add_student(student)
        print("Student added successfully.")
    
    except ValueError as error:
        print(f"Error: {error}")


def add_grade(gradebook):
    student_id = input("Student ID: ").strip()
    course = input("Course name: ").strip()

    try:
        grade = float(input("Grade (0-20): "))
        gradebook.add_grade(student_id, course, grade)
        print("Grade added successfully.")

    except ValueError as error:
        print(f"Invalid grade input or value: {error}")

    except GradeValidationError as error:
        print(f"Error: {error}")

    except KeyError as error:
        print(f"Error: {error}")


def show_students(gradebook):
    if len(gradebook) == 0:
        print("There are no students.")
        return

    for student in gradebook.students.values():
        print(student)

        result = student.best_course()

        if result is not None:
            course, grade = result
            print(f"Best course: {course}, grade: {grade}")


def show_ranking(gradebook):
    students = gradebook.ranking()

    if not students:
        print("There are no student with grades.")
        return

    for position, student in enumerate(students, start = 1):
        print(
            f"{position}. {student.name} - "
            f"Average: {student.average_grade():.2f}"
        )


def show_failing_students(gradebook):
    students = gradebook.failing_student()

    if not students:
        print("There are no failing students.")
        return

    for student in students:
        print(student)


def show_common_courses(gradebook):
    first_id = input("First student ID: ").strip()
    second_id = input("Second student ID: ").strip()

    try:
        courses = gradebook.common_course(first_id, second_id)

        if courses:
            print("Common courses:", ", ".join(sorted(courses)))
        else:
            print("These students have no common courses.")

    except KeyError as error:
        print(f"Error: {error}")

def main():
    gradebook = Gradebook()
    gradebook.load()

    while True:
        print("\n1. Add student (regular or graduate)")
        print("2. Add or update a grade")
        print("3. Show all students")
        print("4. Show ranking (highest to lowest average)")
        print("5. Show failing students")
        print("6. Show common courses of two students")
        print("7. Save and exit")

        choice = input("Choose an option: ")

        match choice:
            case "1":
                add_student(gradebook)
            case "2":
                add_grade(gradebook)
            case "3":
                show_students(gradebook)
            case "4":
                show_ranking(gradebook)
            case "5":
                show_failing_students(gradebook)
            case "6":
                show_common_courses(gradebook)
            case "7":
                try:
                    gradebook.save()
                    print("Data saved successfully.")
                    break
                
                except OSError as error:
                    print(f"Could not save the data: {error}")    
            case _:
                print("Invalid menu choice. Try again.")


if __name__ == "__main__":
    main()