# Homework 6 - Part 1: Procedural Programming

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
    return student["homework"] / 10 * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(score):
    if score >= 60:
        return "Pass"
    else:
        return "Fail"


def is_excellent(student):
    return student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90


def recovery_score(score):
    return min(score + 5, 100)


# calculate everything for every student and store it in a new list
results = []
for s in students:
    score = final_score(s)
    result = {
        "name": s["name"],
        "exam_average": exam_average(s),
        "homework_score": homework_score(s),
        "final_score": score,
        "status": get_status(score),
        "excellent": is_excellent(s),
    }
    if score < 60:
        result["recovery_score"] = recovery_score(score)
    results.append(result)

print("=== Results ===")
for r in results:
    print(f"{r['name']:6} | exam avg: {r['exam_average']:.2f} | homework: {r['homework_score']:.0f} "
          f"| final: {r['final_score']:.2f} | {r['status']}")

print("\n=== Excellent students ===")
for r in results:
    if r["excellent"]:
        print(r["name"])

print("\n=== Recovery scores (status stays the same) ===")
for r in results:
    if "recovery_score" in r:
        print(f"{r['name']}: {r['final_score']:.2f} -> {r['recovery_score']:.2f} (status: {r['status']})")

# class average
total = 0
for r in results:
    total += r["final_score"]
class_average = total / len(results)
print(f"\nClass average: {class_average:.2f}")

# ranking with a simple bubble sort, so we don't change the original list
ranking = results.copy()
for i in range(len(ranking)):
    for j in range(len(ranking) - 1 - i):
        if ranking[j]["final_score"] < ranking[j + 1]["final_score"]:
            ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]

print("\n=== Ranking ===")
place = 1
for r in ranking:
    print(f"{place}. {r['name']} - {r['final_score']:.2f}")
    place += 1
