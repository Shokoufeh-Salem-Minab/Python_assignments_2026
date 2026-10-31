# Assignment 6: student performance analysis using procedural programming.

STUDENTS = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def exam_average(student):
    # Return the average of the student's three examination scores.
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    # Convert completed homework assignments to a percentage.
    return student["homework"] / 10 * 100


def final_score(student):
    # Return the weighted final score.
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def status(student):
    return "Pass" if final_score(student) >= 60 else "Fail"


def is_excellent(student):
    return all(student[f"exam{number}"] >= 90 for number in range(1, 4))


def recovery_score(student):
    # Return a recovery score only for failing students.
    score = final_score(student)
    return min(score + 5, 100) if score < 60 else None


def build_report(students):
    # Use loops and conditions to build result dictionaries.
    report = []
    for student in students:
        score = final_score(student)
        report.append(
            {
                "name": student["name"],
                "exam_average": exam_average(student),
                "homework_score": homework_score(student),
                "final_score": score,
                "status": status(student),
                "excellent": is_excellent(student),
                "recovery_score": recovery_score(student),
            }
        )
    return report


def class_average(report):
    return sum(student["final_score"] for student in report) / len(report)


def rank_students(report):
    # Rank students from highest to lowest final score.
    return sorted(report, key=lambda student: student["final_score"], reverse=True)


def main():
    report = build_report(STUDENTS)
    print(f"Class average: {class_average(report):.2f}")
    print("\nRanking:")
    for rank, student in enumerate(rank_students(report), start=1):
        recovery = "" if student["recovery_score"] is None else f", recovery {student['recovery_score']:.2f}"
        excellent = " (Excellent Performance)" if student["excellent"] else ""
        print(f"{rank}. {student['name']}: {student['final_score']:.2f} - {student['status']}{excellent}{recovery}")


if __name__ == "__main__":
    main()
