# Homework 6 
# Srivishva Melvin Marimouttou, sm25017
# Program created on: 27/10/2026

from functools import reduce

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

def is_excellent(student):
    return min(student["exam1"], student["exam2"], student["exam3"]) >= 90

def recovery_score(final):
    return min(final + 5, 100) if final < 60 else None

def with_scores(student):
    new_student = dict(student)
    final = final_score(student)
    new_student["final"] = final
    new_student["status"] = "Pass" if final >= 60 else "Fail"
    new_student["excellent"] = is_excellent(student)
    new_student["recovery"] = recovery_score(final)
    return new_student

def is_passing(student):
    return student["status"] == "Pass"

def add_final(total, student):
    return total + student["final"]

original = [dict(s) for s in students] # copy, only used to prove nothing changed
scored = list(map(with_scores, students)) # calculate scores
passing = list(filter(is_passing, scored)) # select passing students
excellent = list(filter(lambda s: s["excellent"], scored)) # check for excellent students
needs_recovery = list(filter(lambda s: s["recovery"] is not None, scored)) # check for failing students
total = reduce(add_final, scored, 0) # total of all final scores
ranking = sorted(scored, key=lambda s: s["final"], reverse=True) # students ranked, using their final score, from highest to lowest

print("Name Final Status")
for s in scored:
    print(s["name"], round(s["final"], 2), s["status"])

print("\nPassing students:", ", ".join(map(lambda s: s["name"], passing)))
print("Excellent students:", ", ".join(map(lambda s: s["name"], excellent)))

print("\nRecovery scores:")
for s in needs_recovery:
    print(s["name"] + ":", round(s["final"], 2), "to", round(s["recovery"], 2), "(status stays", s["status"] + ")")

print("\nTotal of final scores:", round(total, 2))
print("Class average:", round(total / len(scored), 2))

print("\nRanking:")
for place, s in enumerate(ranking, start=1):
    print(str(place) + ".", s["name"], "-", round(s["final"], 2))

print("\nOriginal dataset unchanged:", students == original)
