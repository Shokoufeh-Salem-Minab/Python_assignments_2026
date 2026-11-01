from data import students, PASS_SCORE, EXCELLENT_SCORE, RECOVERY_POINTS, MAX_SCORE


# ----- Calculations -----
def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return student["homework"] / 10 * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(score):
    if score >= PASS_SCORE:
        return "Pass"
    return "Fail"


def is_excellent(student):
    return (student["exam1"] >= EXCELLENT_SCORE
            and student["exam2"] >= EXCELLENT_SCORE
            and student["exam3"] >= EXCELLENT_SCORE)


def recovery_score(score):
    # only students below the pass score get a recovery score
    if score < PASS_SCORE:
        return min(score + RECOVERY_POINTS, MAX_SCORE)
    return None


def class_average(results):
    total = 0
    for result in results:
        total += result["final_score"]
    return total / len(results)


def rank_students(results):
    return sorted(results, key=lambda result: result["final_score"], reverse=True)


# ----- Build the results -----
def build_results():
    results = []
    for student in students:
        score = final_score(student)
        results.append({
            "name": student["name"],
            "final_score": score,
            "status": get_status(score),
            "excellent": is_excellent(student),
            "recovery": recovery_score(score),
        })
    return results


# ----- Report -----
def print_report(results):
    print("===== PROCEDURAL PROGRAMMING =====")

    print("\n----- FINAL SCORES -----")
    for result in results:
        print(f"{result['name']}: {result['final_score']:.2f} ({result['status']})")

    print("\n----- EXCELLENT STUDENTS -----")
    for result in results:
        if result["excellent"]:
            print(result["name"])

    print("\n----- RECOVERY SCORES -----")
    for result in results:
        if result["recovery"] is not None:
            print(f"{result['name']}: {result['final_score']:.2f} -> {result['recovery']:.2f} "
                  f"(status stays {result['status']})")

    print(f"\nClass average: {class_average(results):.2f}")

    print("\n----- RANKING -----")
    place = 1
    for result in rank_students(results):
        print(f"{place}. {result['name']} - {result['final_score']:.2f}")
        place += 1


def main():
    results = build_results()
    print_report(results)


main()
