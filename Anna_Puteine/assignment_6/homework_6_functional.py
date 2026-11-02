from functools import reduce

from students_data import students

def examAverage(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3

def homeworkScore(student):
    return student["homework"] / 10 * 100

def finalScore(student):
    return 0.7 * examAverage(student) + 0.3 * homeworkScore(student)

def status(score):
    return "Pass" if score >= 60 else "Fail"

def isExcellent(student):
    return all(student[exam] >= 90 for exam in ("exam1", "exam2", "exam3"))

def recoveryScore(score):
    return min(score + 5, 100)

def addResults(student):
    score = finalScore(student)
    return {**student, "final_score": score, "status": status(score)}

results = list(map(addResults, students))

passing = list(filter(lambda student: student["status"] == "Pass", results))
failing = list(filter(lambda student: student["status"] == "Fail", results))
excellent = list(filter(isExcellent, results))

recovery = list(map(lambda student: (student["name"], recoveryScore(student["final_score"])), failing))

total = reduce(lambda acc, student: acc + student["final_score"], results, 0)
class_average = total / len(results) if results else 0

ranked = sorted(results, key=lambda student: student["final_score"], reverse=True)

print("Student results:")
for student in results:
    print(f"{student['name']}: final {student['final_score']:.2f}, {student['status']}")

print(f"\nPassing: {list(map(lambda student: student['name'], passing))}")
print(f"Failing: {list(map(lambda student: student['name'], failing))}")
print(f"Excellent: {list(map(lambda student: student['name'], excellent))}")

print("\nRecovery scores:")
for name, score in recovery:
    print(f"{name}: {score:.2f} (status stays Fail)")

print(f"\nTotal final score: {total:.2f}")
print(f"Class average: {class_average:.2f}")

print("\nRanking:")
for place, student in enumerate(ranked, start=1):
    print(f"{place}. {student['name']} - {student['final_score']:.2f}")

print(f"\nOriginal data unchanged: {'final_score' not in students[0]}")
