# Homework 6 - Functional programming
from functools import reduce

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]


def exam_average(s):
    return (s["exam1"] + s["exam2"] + s["exam3"]) / 3


def homework_score(s):
    return s["homework"] / 10 * 100


def final_score(s):
    return exam_average(s) * 0.7 + homework_score(s) * 0.3


def get_status(final):
    return "Pass" if final >= 60 else "Fail"


def is_excellent(s):
    return s["exam1"] >= 90 and s["exam2"] >= 90 and s["exam3"] >= 90


def recovery_score(final):
    if final < 60:
        return min(final + 5, 100)
    return None


def add_scores(s):
    # make a copy so the original dictionary is not changed
    new_s = s.copy()
    new_s["final"] = final_score(s)
    new_s["status"] = get_status(new_s["final"])
    new_s["excellent"] = is_excellent(s)
    new_s["recovery"] = recovery_score(new_s["final"])
    return new_s


# map - calculate scores for all students
results = list(map(add_scores, students))

# filter - select students
passed = list(filter(lambda r: r["status"] == "Pass", results))
failed = list(filter(lambda r: r["status"] == "Fail", results))
excellent = list(filter(lambda r: r["excellent"], results))

# reduce - total of all final scores
total = reduce(lambda a, r: a + r["final"], results, 0)
average = total / len(results)

# sorted - ranking
ranking = sorted(results, key=lambda r: r["final"], reverse=True)

print("Student results:")
for r in results:
    print(r["name"], "- final score:", round(r["final"], 2), "-", r["status"])
    if r["recovery"] is not None:
        print("   Recovery score:", round(r["recovery"], 2))

print("\nPassed:", [r["name"] for r in passed])
print("Failed:", [r["name"] for r in failed])
print("Excellent:", [r["name"] for r in excellent])

print("\nTotal final score:", round(total, 2))
print("Class average:", round(average, 2))

print("\nRanking:")
for i, r in enumerate(ranking):
    print(i + 1, r["name"], round(r["final"], 2))

# check that the original data was not changed
print("\nOriginal first student:", students[0])