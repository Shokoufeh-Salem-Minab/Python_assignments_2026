# Andre Filho - Homework 6 - Student Performance Analysis System
# 1. Procedural Programming

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return (student["homework"] / 10) * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def passed(student):
    return final_score(student) >= 60


def is_excellent(student):
    return student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90


def recovery_score(student):
    score = final_score(student)
    if score >= 60:
        return None
    return min(score + 5, 100)


def class_average(students_list):
    total = 0
    for student in students_list:
        total += final_score(student)
    return total / len(students_list)


def rank_students(students_list):
    ranking = sorted(students_list, key=final_score, reverse=True)
    return [student["name"] for student in ranking]


if __name__ == "__main__":
    print("--- Student results ---")
    for student in students:
        status = "Pass" if passed(student) else "Fail"
        line = (
            f"{student['name']}: exam_avg={exam_average(student):.2f}, "
            f"hw_score={homework_score(student):.2f}, "
            f"final={final_score(student):.2f}, status={status}"
        )
        if is_excellent(student):
            line += ", Excellent Performance"
        recovery = recovery_score(student)
        if recovery is not None:
            line += f", recovery_score={recovery:.2f}"
        print(line)

    excellent_students = [s["name"] for s in students if is_excellent(s)]
    print("\nExcellent students:", excellent_students)

    print(f"\nClass average (final score): {class_average(students):.2f}")

    print("\nRanking (best to worst):")
    for position, name in enumerate(rank_students(students), start=1):
        print(f"{position}. {name}")
