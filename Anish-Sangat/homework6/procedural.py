# Homework 6 - Procedural programming

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]


def get_exam_average(student):
    total = student["exam1"] + student["exam2"] + student["exam3"]
    return total / 3


def get_homework_score(student):
    return student["homework"] / 10 * 100


def get_final_score(student):
    exam_avg = get_exam_average(student)
    hw = get_homework_score(student)
    return exam_avg * 0.7 + hw * 0.3


def get_status(final_score):
    if final_score >= 60:
        return "Pass"
    else:
        return "Fail"


def is_excellent(student):
    if student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90:
        return True
    return False


def get_recovery_score(final_score):
    # only for students with final score below 60
    if final_score < 60:
        recovery = final_score + 5
        if recovery > 100:
            recovery = 100
        return recovery
    return None


# calculate everything for every student
results = []
total_final = 0

for s in students:
    final = get_final_score(s)
    result = {
        "name": s["name"],
        "final": final,
        "status": get_status(final),
        "excellent": is_excellent(s),
        "recovery": get_recovery_score(final)
    }
    results.append(result)
    total_final = total_final + final

# print results
print("Student results:")
for r in results:
    print(r["name"], "- final score:", round(r["final"], 2), "-", r["status"])
    if r["excellent"] == True:
        print("   Excellent performance!")
    if r["recovery"] is not None:
        print("   Recovery score:", round(r["recovery"], 2))

# class average
class_average = total_final / len(results)
print("\nClass average:", round(class_average, 2))

# ranking (bubble sort, highest score first)
ranking = results.copy()
for i in range(len(ranking)):
    for j in range(len(ranking) - 1 - i):
        if ranking[j]["final"] < ranking[j + 1]["final"]:
            temp = ranking[j]
            ranking[j] = ranking[j + 1]
            ranking[j + 1] = temp

print("\nRanking:")
place = 1
for r in ranking:
    print(place, r["name"], round(r["final"], 2))
    place = place + 1