students = [    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
                {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
                {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
                {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
                {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
                {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}]

def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"])/3


def homework_score(student):
    return (student["homework"]/10) * 100


def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)


def final_passed(student):
    if final_score(student) >= 60:
        return True
    return False

def excellent_score(student):
    if student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90:
        return True
    return False

def recovery_score(student):
    if final_score(student) < 60:
        return min(final_score(student) + 5, 100)
    return None

def class_average(students):
    total = 0
    for student in students:
        total += final_score(student)
    return total / len(students)

def ranking(students):
    return sorted(students, key=final_score, reverse=True)


print("Average exam grades: ")
for student in students:
    ex_average = exam_average(student)
    print(student["name"], round(ex_average,2))

print("Average homework scores: ")
for student in students:
    hm_score = homework_score(student)
    print(student["name"], round(hm_score,2))

print("Student final scores: ")
for student in students:
    final = final_score(student)
    print(student["name"], round(final,2))

print("Students who failed and passed: ")
for student in students:
    passed = final_passed(student)
    if passed:
        print(student["name"], "Pass")
    else:
        print(student["name"], "Fail")

print("Students who qualify for Excellent Performance: ")
for student in students:
    good_score = excellent_score(student)
    if good_score:
        print(student["name"])

print("Student recovery scores: ")
for student in students:
    recovery_scr = recovery_score(student)
    if recovery_scr is not None:
        print(student["name"], "recovery score:", round(recovery_scr,2), "Fail")

class_avg = class_average(students)
print(f"Class average: {round(class_avg,2)}")

print("Ranking: ")
ranked = ranking(students)
position = 1
for student in ranked:
    print(position, ".", student["name"], round(final_score(student), 2))
    position += 1


# Comparison and reflection - Procedural Programming:
# The program is a list of steps run from top to bottom, using functions, loops and if
# statements. Strengths: it is the simplest and most readable approach, so it is perfect
# for small scripts like this one. Limitations: the data (dictionaries) and the functions
# that use it are kept separate, so in a bigger program it gets hard to keep track of
# which function works with which data, and the code is harder to reuse.
