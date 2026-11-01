# Homework 6 - Part 3: Functional Programming
# the original list is never changed, every step creates new data

from functools import reduce

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


# pure functions
def exam_average(s):
    return (s["exam1"] + s["exam2"] + s["exam3"]) / 3


def homework_score(s):
    return s["homework"] / 10 * 100


def final_score(s):
    return 0.7 * exam_average(s) + 0.3 * homework_score(s)


def status(score):
    return "Pass" if score >= 60 else "Fail"


def is_excellent(s):
    return all(s[e] >= 90 for e in ["exam1", "exam2", "exam3"])


def recovery_score(score):
    return min(score + 5, 100)


def add_results(s):
    # returns a new dict, the old one stays the same
    score = final_score(s)
    return {**s,
            "exam_average": exam_average(s),
            "homework_score": homework_score(s),
            "final_score": score,
            "status": status(score)}


# map -> calculate scores
results = list(map(add_results, students))

# filter -> select students
passed = list(filter(lambda s: s["status"] == "Pass", results))
failed = list(filter(lambda s: s["status"] == "Fail", results))
excellent = list(filter(is_excellent, results))

# recovery only for failed students (status stays "Fail")
recovery = list(map(lambda s: {"name": s["name"], "recovery_score": recovery_score(s["final_score"]),
                               "status": s["status"]}, failed))

# reduce -> total final score
total = reduce(lambda acc, s: acc + s["final_score"], results, 0)
class_average = total / len(results)

# sorted -> ranking
ranking = sorted(results, key=lambda s: s["final_score"], reverse=True)

print("=== Results ===")
list(map(lambda s: print(f"{s['name']:6} | final: {s['final_score']:.2f} | {s['status']}"), results))

print("\nPassed:", list(map(lambda s: s["name"], passed)))
print("Failed:", list(map(lambda s: s["name"], failed)))
print("Excellent:", list(map(lambda s: s["name"], excellent)))
print("Recovery:", list(map(lambda r: f"{r['name']} {r['recovery_score']:.2f} ({r['status']})", recovery)))

print(f"\nTotal final score: {total:.2f}")
print(f"Class average: {class_average:.2f}")

print("\n=== Ranking ===")
for i, s in enumerate(ranking, start=1):
    print(f"{i}. {s['name']} - {s['final_score']:.2f}")

# check that the original data was not modified
print("\nOriginal data unchanged:", "final_score" not in students[0])
