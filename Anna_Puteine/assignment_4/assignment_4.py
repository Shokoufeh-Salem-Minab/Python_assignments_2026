import json

import student as student_classes
from gradebook import Gradebook, InvalidOperation

gradebook = Gradebook()

try:
    gradebook.loadFromStorage()
except Exception as ex:
    print(f"Error: could not read the saved file ({ex}). Starting with an empty gradebook.")
    gradebook = Gradebook()

while True:
    print("\n1. Add student (regular or graduate)")
    print("2. Add or update a grade")
    print("3. Show all students")
    print("4. Show ranking")
    print("5. Show failing students")
    print("6. Show common courses of two students")
    print("7. Save and exit")
    print(f"Students in gradebook: {len(gradebook)}")

    choice = input("Choose an option: ")

    try:
        if choice == "1":
            answer = input("Graduate student? (y/n): ").lower()

            if answer == "y":
                thesis_title = input("Thesis title: ")
                gradebook.addStudent(student_classes.GraduateStudent({}, thesis_title))
            elif answer == "n":
                gradebook.addStudent(student_classes.Student({}))
            else:
                raise InvalidOperation("Please answer y or n")

        elif choice == "2":
            student_id = int(input("Student id: "))
            course = input("Course: ").strip()

            if course == "":
                raise InvalidOperation("Course name cannot be empty")

            grade = input("Grade (0-20): ")
            gradebook.addGrade(student_id, course, grade)

        elif choice == "3":
            gradebook.showStudents()

        elif choice == "4":
            gradebook.showRanking()

        elif choice == "5":
            gradebook.showFailing()

        elif choice == "6":
            first_id = int(input("First student id: "))
            second_id = int(input("Second student id: "))
            common = gradebook.getCommonCourses(first_id, second_id)
            print("\n Common courses:\n")
            print(common)

        elif choice == "7":
            gradebook.saveToStorage()
            print("Data saved. Goodbye!")
            break

        else:
            print("Error: unknown option, choose 1-7.")

    except (InvalidOperation, student_classes.InvalidGrade) as ex:
        print(f"Error: {ex}")
    except Exception:
        print("Something went wrong")
