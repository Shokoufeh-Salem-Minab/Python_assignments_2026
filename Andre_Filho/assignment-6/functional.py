# Andre Filho - Homework 6 - Student Performance Analysis System
# 3. Functional Programming

from functools import reduce

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


def is_excellent(student):
    return student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90


def with_final_score(student):
    # returns a NEW dict instead of mutating the original student
    return {**student, "final_score": final_score(student)}


if __name__ == "__main__":
    # map(): build a new list of students enriched with their final score,
    # the original 'students' list/dicts are never changed
    scored_students = list(map(with_final_score, students))

    print("--- Student results ---")
    for student in scored_students:
        status = "Pass" if student["final_score"] >= 60 else "Fail"
        print(f"{student['name']}: final={student['final_score']:.2f}, status={status}")

    # filter(): students who passed, and students with Excellent Performance
    passed_students = list(filter(lambda s: s["final_score"] >= 60, scored_students))
    excellent_students = list(filter(is_excellent, students))
    print("\nPassed students:", [s["name"] for s in passed_students])
    print("Excellent students:", [s["name"] for s in excellent_students])

    # reduce(): sum of all final scores, used to compute the class average
    total_final_score = reduce(lambda acc, s: acc + s["final_score"], scored_students, 0)
    class_average = total_final_score / len(scored_students)
    print(f"\nClass average (final score): {class_average:.2f}")

    # sorted(): rank students best to worst by final score
    ranking = sorted(scored_students, key=lambda s: s["final_score"], reverse=True)
    print("\nRanking (best to worst):")
    for position, student in enumerate(ranking, start=1):
        print(f"{position}. {student['name']}")

    # original dataset is left untouched
    assert "final_score" not in students[0]
