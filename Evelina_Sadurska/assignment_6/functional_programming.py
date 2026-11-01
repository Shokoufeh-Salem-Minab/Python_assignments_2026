from functools import reduce

students = [{"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
            {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
            {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
            {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
            {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
            {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}]

def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3

def homework_score(student):
    return (student["homework"] / 10) * 100

def final_score(student):
    return 0.7 * exam_average(student) + 0.3 * homework_score(student)

def final_passed(student):
    if final_score(student) >= 60:
        return True
    return False

def final_failed(student):
    if final_score(student) < 60:
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

def get_name(student):
    return student["name"]

def add_score(total, student):
    return total + final_score(student)


print("Exam averages: ")
exam_averages = list(map(lambda s: (s["name"], round(exam_average(s), 2)), students))
print(exam_averages)

print("Homework scores: ")
homework_scores = list(map(lambda s: (s["name"], round(homework_score(s), 2)), students))
print(homework_scores)

print("Final scores: ")
final_scores = list(map(lambda s: (s["name"], round(final_score(s), 2)), students))
print(final_scores)

print("Students who passed: ")
passed = list(filter(final_passed, students))
print(list(map(get_name, passed)))

print("Students who failed: ")
failed = list(filter(final_failed, students))
print(list(map(get_name, failed)))

print("Students who got excellent scores: ")
excellent_scores = list(filter(excellent_score, students))
print(list(map(get_name, excellent_scores)))

print("Recovery scores (status stays Fail): ")
print(list(map(lambda s: (s["name"], round(recovery_score(s), 2), "Fail"), failed)))

total = reduce(add_score, students, 0)
print("Total final score:", round(total, 2))
print("Class average:", round(total / len(students), 2))

print("Ranking: ")
ranked = sorted(students, key=final_score, reverse=True)
print(list(enumerate(map(get_name, ranked), start=1)))

# Comparison and reflection - Functional Programming:
# Instead of loops that change variables step by step, the program is built from small
# independent functions that take data and return new results without changing the
# original list (map transforms, filter selects, reduce combines, sorted ranks).
# Strengths: each function is easy to test on its own, there are no hidden side effects,
# and the code is short. Limitations: chains of map/filter/reduce can be harder to read
# for beginners than a simple loop, and it is less natural for programs that need to
# keep and update state.
