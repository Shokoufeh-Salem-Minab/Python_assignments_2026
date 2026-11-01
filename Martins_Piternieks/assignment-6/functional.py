from functools import reduce

from data import students, PASS_SCORE, EXCELLENT_SCORE, RECOVERY_POINTS, MAX_SCORE


# ----- Pure Functions (they never change their input) -----
def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return student["homework"] / 10 * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(score):
    return "Pass" if score >= PASS_SCORE else "Fail"


def is_excellent(student):
    return all(student[exam] >= EXCELLENT_SCORE for exam in ("exam1", "exam2", "exam3"))


def recovery_score(score):
    return min(score + RECOVERY_POINTS, MAX_SCORE)


def add_results(student):
    # returns a NEW dictionary, the original student stays the same
    score = final_score(student)
    return {**student, "final_score": score, "status": get_status(score)}


# ----- map, filter, reduce, sorted -----
def main():
    results = list(map(add_results, students))

    excellent = list(filter(is_excellent, results))
    failing = list(filter(lambda student: student["status"] == "Fail", results))

    total = reduce(lambda subtotal, student: subtotal + student["final_score"], results, 0)
    average = total / len(results)

    ranking = sorted(results, key=lambda student: student["final_score"], reverse=True)

    print("===== FUNCTIONAL PROGRAMMING =====")

    print("\n----- FINAL SCORES -----")
    for student in results:
        print(f"{student['name']}: {student['final_score']:.2f} ({student['status']})")

    print("\n----- EXCELLENT STUDENTS -----")
    for student in excellent:
        print(student["name"])

    print("\n----- RECOVERY SCORES -----")
    for student in failing:
        print(f"{student['name']}: {student['final_score']:.2f} -> "
              f"{recovery_score(student['final_score']):.2f} (status stays {student['status']})")

    print(f"\nTotal final score: {total:.2f}")
    print(f"Class average: {average:.2f}")

    print("\n----- RANKING -----")
    for place, student in enumerate(ranking, start=1):
        print(f"{place}. {student['name']} - {student['final_score']:.2f}")

    # proof that the original dataset was not changed
    print("\nOriginal data unchanged:", "final_score" not in students[0])


main()
