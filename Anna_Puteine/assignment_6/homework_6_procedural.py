from students_data import students

def examAverage(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3

def homeworkScore(student):
    return student["homework"] / 10 * 100

def finalScore(student):
    return 0.7 * examAverage(student) + 0.3 * homeworkScore(student)

def status(student):
    if finalScore(student) >= 60:
        return "Pass"
    return "Fail"

def isExcellent(student):
    if student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90:
        return True
    return False

def recoveryScore(student):
    score = finalScore(student) + 5

    if score > 100:
        score = 100
    return score

def classAverage(students):
    if len(students) == 0:
        return 0

    total = 0

    for student in students:
        total += finalScore(student)

    return total / len(students)

def ranking(students):
    ranked = []

    for student in students:
        ranked.append((student["name"], finalScore(student)))

    ranked.sort(key=lambda item: item[1], reverse=True)
    return ranked

print("Student results:")
for student in students:
    print(f"{student['name']}: exam average {examAverage(student):.2f}, homework {homeworkScore(student):.0f}, "
          f"final {finalScore(student):.2f}, {status(student)}")

print("\nExcellent students:")
for student in students:
    if isExcellent(student):
        print(student["name"])

print("\nRecovery scores:")
for student in students:
    if finalScore(student) < 60:
        print(f"{student['name']}: {recoveryScore(student):.2f} (status stays {status(student)})")

print(f"\nClass average: {classAverage(students):.2f}")

print("\nRanking:")
place = 1
for name, score in ranking(students):
    print(f"{place}. {name} - {score:.2f}")
    place += 1
