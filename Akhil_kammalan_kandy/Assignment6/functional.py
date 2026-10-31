# Assignment 6: student performance analysis using functional programming.

from functools import reduce

STUDENTS = (
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
)


def score_record(student):
    # Return a new result record without changing the supplied student.
    exam_average = sum(student[f"exam{number}"] for number in range(1, 4)) / 3
    homework_score = student["homework"] / 10 * 100
    final_score = 0.7 * exam_average + 0.3 * homework_score
    return {
        **student,
        "exam_average": exam_average,
        "homework_score": homework_score,
        "final_score": final_score,
        "status": "Pass" if final_score >= 60 else "Fail",
        "excellent": all(student[f"exam{number}"] >= 90 for number in range(1, 4)),
        "recovery_score": min(final_score + 5, 100) if final_score < 60 else None,
    }


def analyze(students):
    scored_students = list(map(score_record, students))
    passing_students = list(filter(lambda student: student["status"] == "Pass", scored_students))
    excellent_students = list(filter(lambda student: student["excellent"], scored_students))
    total_score = reduce(lambda total, student: total + student["final_score"], scored_students, 0.0)
    ranking = sorted(scored_students, key=lambda student: student["final_score"], reverse=True)
    return scored_students, passing_students, excellent_students, total_score / len(scored_students), ranking


def main():
    _, passing, excellent, average, ranking = analyze(STUDENTS)
    print(f"Class average: {average:.2f}")
    print("Passing students:", ", ".join(student["name"] for student in passing))
    print("Excellent students:", ", ".join(student["name"] for student in excellent))
    print("Ranking:", ", ".join(student["name"] for student in ranking))


if __name__ == "__main__":
    main()
