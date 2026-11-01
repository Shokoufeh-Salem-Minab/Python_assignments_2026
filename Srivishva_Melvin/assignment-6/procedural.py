# Homework 6 
# Srivishva Melvin Marimouttou, sm25017
# Program created on: 27/10/2026

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
    return (student["homework"] / 10) * 100

def final_score(student):
    return (0.7 * exam_average(student)) + (0.3 * homework_score(student))

def get_status(final):
    if final >= 60:
        return "Pass"
    return "Fail"

def is_excellent(student):
    return student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90

def recovery_score(final):
    if final < 60:
        new_score = final + 5
        if new_score > 100:
            new_score = 100
        return new_score
    return None

def class_average(finals):
    total = 0
    for f in finals:
        total = total + f
    return total / len(finals)

def get_final(result):
    return result["final"]

results = []
for student in students:
    final = final_score(student)
    result = {
        "name": student["name"],
        "final": final,
        "status": get_status(final),
        "excellent": is_excellent(student),
        "recovery": recovery_score(final),
    }
    results.append(result)

print("Name Final Status")
for r in results:
    print(r["name"], round(r["final"], 2), r["status"])

print("\nExcellent students:")
for r in results:
    if r["excellent"]:
        print(" ", r["name"])

print("\nRecovery scores:")
for r in results:
    if r["recovery"] is not None:
        print(r["name"] + ":", round(r["final"], 2), "to", round(r["recovery"], 2), "(status stays", r["status"] + ")")

finals = []
for r in results:
    finals.append(r["final"])
print("\nClass average:", round(class_average(finals), 2))

print("\nRanking:")
place = 1
for r in sorted(results, key=get_final, reverse=True):
    print(str(place) + ".", r["name"], "-", round(r["final"], 2))
    place += 1
