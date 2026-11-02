# Homework 6 - Student Performance Analysis System
# Part 3: Functional Programming
# Lasse Johannis

from functools import reduce
from dataset import students


# pure functions: same input -> same output, no side effects
def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return student["homework"] / 10 * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def get_status(score):
    if score >= 60:
        return "Pass"
    return "Fail"


def is_excellent(student):
    return student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90


def recovery_score(score):
    return min(score + 5, 100)


# builds a new dictionary, the original student is not changed
def with_scores(student):
    score = final_score(student)
    return {"name": student["name"], "final_score": score, "status": get_status(score)}


results = list(map(with_scores, students))
passed = list(filter(lambda result: result["status"] == "Pass", results))
failed = list(filter(lambda result: result["status"] == "Fail", results))
excellent = list(filter(is_excellent, students))
recovery = list(map(lambda result: (result["name"], recovery_score(result["final_score"])), failed))
total = reduce(lambda a, b: a + b, map(lambda result: result["final_score"], results))
ranking = sorted(results, key=lambda result: result["final_score"], reverse=True)

print("Final scores:")
for result in results:
    print(f"{result['name']}: {result['final_score']:.2f} ({result['status']})")

print("\nPassed:", list(map(lambda result: result["name"], passed)))
print("Failed:", list(map(lambda result: result["name"], failed)))
print("Excellent:", list(map(lambda student: student["name"], excellent)))

print("\nRecovery scores:")
for name, score in recovery:
    print(f"{name}: {score:.2f} (status stays Fail)")

print(f"\nTotal final score: {total:.2f}")
print(f"Class average: {total / len(results):.2f}")

print("\nRanking:")
place = 1
for result in ranking:
    print(f"{place}. {result['name']} - {result['final_score']:.2f}")
    place += 1
