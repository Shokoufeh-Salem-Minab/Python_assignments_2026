# Task 3: Functional programming
# small separate functions that only take input and return output.
# no loops for the calculations: map() calculates, filter() selects,
# reduce() adds up, sorted() ranks.
# the original students list is never changed, i always make new dicts.

from functools import reduce

# the dataset from the homework
students = [
    {"name": "Anna",  "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John",  "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def check_students(data):
    # small safety check so the programs stop with a clear message
    # if the data is broken (empty list, missing key, score out of range)
    if len(data) == 0:
        raise ValueError("the student list is empty")

    for s in data:
        for key in ["name", "exam1", "exam2", "exam3", "homework"]:
            if key not in s:
                raise ValueError(f"student {s} is missing the key '{key}'")

        for key in ["exam1", "exam2", "exam3", "homework"]:
            value = s[key]
            # bool is also a number in python so i block it separately
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{s['name']}: {key} must be a number")

        for key in ["exam1", "exam2", "exam3"]:
            if s[key] < 0 or s[key] > 100:
                raise ValueError(f"{s['name']}: {key} must be between 0 and 100")

        # homework is how many of the 10 assignments were submitted
        if s["homework"] < 0 or s["homework"] > 10:
            raise ValueError(f"{s['name']}: homework must be between 0 and 10")


def exam_average(s):
    return (s["exam1"] + s["exam2"] + s["exam3"]) / 3


def homework_score(s):
    return s["homework"] / 10 * 100


def final_score(s):
    return 0.7 * exam_average(s) + 0.3 * homework_score(s)


def is_excellent(s):
    # smallest exam score must still be 90+
    return min(s["exam1"], s["exam2"], s["exam3"]) >= 90


def recovery_score(final):
    # +5 but max 100
    return min(final + 5, 100)


def add_scores(s):
    # this is the function i give to map()
    # {**s, ...} makes a NEW dict with everything from s plus the new keys,
    # so the original dict stays the same
    final = final_score(s)
    return {
        **s,
        "exam_avg": exam_average(s),
        "homework_score": homework_score(s),
        "final": final,
        "status": "Pass" if final >= 60 else "Fail",
        "excellent": is_excellent(s),
        "recovery": recovery_score(final) if final < 60 else None,
    }


def has_passed(s):
    return s["status"] == "Pass"


def has_excellent(s):
    return s["excellent"]


def needs_recovery(s):
    return s["recovery"] is not None


def add_final(total, s):
    # for reduce(): running total + this student's final score
    return total + s["final"]


def class_average(results):
    if len(results) == 0:
        return 0  # nothing to average
    return reduce(add_final, results, 0) / len(results)


def rank(results):
    # highest first
    return sorted(results, key=lambda r: r["final"], reverse=True)


def main():
    check_students(students)

    results = list(map(add_scores, students))

    print("--- Functional ---")
    for r in results:
        print(f"{r['name']:6} final={r['final']:.2f} status={r['status']}")

    passing = list(filter(has_passed, results))
    excellent = list(filter(has_excellent, results))
    recovering = list(filter(needs_recovery, results))

    print("\nPassed:   ", [r["name"] for r in passing])
    print("Excellent:", [r["name"] for r in excellent])
    for r in recovering:
        print(f"Recovery: {r['name']} -> {r['recovery']:.2f}")

    print(f"\nClass average: {class_average(results):.2f}")

    print("\nRanking:")
    for place, r in enumerate(rank(results), start=1):
        print(f"{place}. {r['name']} ({r['final']:.2f})")

    # quick proof that the original data was not touched
    print("\nOriginal keys still:", list(students[0].keys()))


if __name__ == "__main__":
    main()
