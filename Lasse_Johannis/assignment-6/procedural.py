# Homework 6 - Student Performance Analysis System
# Part 1: Procedural Programming
# Lasse Johannis

from dataset import students


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


# +5 points, but never more than 100
def recovery_score(score):
    new_score = score + 5
    if new_score > 100:
        new_score = 100
    return new_score


def class_average(results):
    total = 0
    for result in results:
        total += result["final_score"]
    return total / len(results)


# bubble sort by final score, highest first
def rank_students(results):
    ranking = results.copy()
    for i in range(len(ranking)):
        for j in range(len(ranking) - 1 - i):
            if ranking[j]["final_score"] < ranking[j + 1]["final_score"]:
                ranking[j], ranking[j + 1] = ranking[j + 1], ranking[j]
    return ranking


results = []
for student in students:
    score = final_score(student)
    results.append({"name": student["name"], "final_score": score, "status": get_status(score)})

print("Final scores:")
for result in results:
    print(f"{result['name']}: {result['final_score']:.2f} ({result['status']})")

print("\nExcellent students:")
for student in students:
    if is_excellent(student):
        print(student["name"])

print("\nRecovery scores:")
for result in results:
    if result["final_score"] < 60:
        print(f"{result['name']}: {recovery_score(result['final_score']):.2f} (status stays {result['status']})")

print(f"\nClass average: {class_average(results):.2f}")

print("\nRanking:")
place = 1
for result in rank_students(results):
    print(f"{place}. {result['name']} - {result['final_score']:.2f}")
    place += 1
