from data import students


def calculate_exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def calculate_homework_score(student):
    return student["homework"] * 10


def calculate_final_score(student):
    return 0.7 * calculate_exam_average(student) + 0.3 * calculate_homework_score(student)


def get_status(final_score):
    return "Pass" if final_score > 59 else "Fail"


def is_excellent(student):
    return student["exam1"] > 89 and student["exam2"] > 89 and student["exam3"] > 89


def calculate_recovery_score(final_score):
    # Recovery is a separate, hypothetical score. Never use it to change status.
    if final_score < 60:
        return min(final_score + 5, 100)
    return None


def analyze_students(records):
    results = []
    for student in records:
        exam_average = calculate_exam_average(student)
        final_score = calculate_final_score(student)
        result = {
            **student,
            "exam_average": exam_average,
            "homework_score": calculate_homework_score(student),
            "final_score": final_score,
            "status": get_status(final_score),
            "excellent": is_excellent(student),
            "recovery_score": calculate_recovery_score(final_score),
        }
        results.append(result)
    return results


def calculate_class_average(results):
    return sum(student["final_score"] for student in results) / len(results)


def rank_students(results):
    return sorted(results, key=lambda student: (-student["final_score"], student["name"]))


def main():
    results = analyze_students(students)
    print("PROCEDURAL PROGRAMMING")
    print("Rank | Name   | Final | Status | Excellent | Recovery")
    for rank, student in enumerate(rank_students(results), start=1):
        recovery = "-" if student["recovery_score"] is None else f'{student["recovery_score"]:.2f}'
        print(f'{rank:>4} | {student["name"]:<6} | {student["final_score"]:>5.2f} | '
              f'{student["status"]:<6} | {str(student["excellent"]):<9} | {recovery}')

    print(f"\nClass average: {calculate_class_average(results):.2f}")
    print("Excellent students:", [s["name"] for s in results if s["excellent"]])
    print("Failing students:", [s["name"] for s in results if s["status"] == "Fail"])


if __name__ == "__main__":
    main()
