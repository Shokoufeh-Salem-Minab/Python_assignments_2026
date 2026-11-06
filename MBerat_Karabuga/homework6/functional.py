from functools import reduce
from data import students


def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return student["homework"] * 10


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(score):
    return "Pass" if score > 59 else "Fail"


def is_excellent(student):
    return all(student[exam] > 89 for exam in ("exam1", "exam2", "exam3"))


def recovery_score(score):
    return min(score + 5, 100) if score < 60 else None


def enrich_student(student):
    """Pure transformation: return a new dictionary, leaving student unchanged."""
    score = final_score(student)
    return {
        **student,
        "exam_average": exam_average(student),
        "homework_score": homework_score(student),
        "final_score": score,
        "status": get_status(score),
        "excellent": is_excellent(student),
        "recovery_score": recovery_score(score),
    }


def main():
    # map() calculates all student results without changing the original records.
    results = list(map(enrich_student, students))

    # filter() selects specific students.
    passing = list(filter(lambda student: student["status"] == "Pass", results))
    excellent = list(filter(lambda student: student["excellent"], results))
    recovery = list(filter(lambda student: student["recovery_score"] is not None, results))

    # reduce() adds final scores for the class average.
    total_score = reduce(lambda total, student: total + student["final_score"], results, 0.0)
    class_average = total_score / len(results)

    # sorted() produces a new list, leaving the input order unchanged.
    ranking = sorted(results, key=lambda student: (-student["final_score"], student["name"]))

    print("FUNCTIONAL PROGRAMMING")
    print("Rank | Name   | Final | Status | Excellent | Recovery")
    for rank, student in enumerate(ranking, start=1):
        recovered = student["recovery_score"]
        recovery_text = "-" if recovered is None else f"{recovered:.2f}"
        print(f'{rank:>4} | {student["name"]:<6} | {student["final_score"]:>5.2f} | '
              f'{student["status"]:<6} | {str(student["excellent"]):<9} | {recovery_text}')

    print(f"\nClass average: {class_average:.2f}")
    print("Passing students:", [s["name"] for s in passing])
    print("Excellent students:", [s["name"] for s in excellent])
    print("Recovery students:", [s["name"] for s in recovery])


if __name__ == "__main__":
    main()
