students = [
    {"name":"Anna","exam1":85,"exam2":90,"exam3":88,"homework":9},
    {"name":"Peter","exam1":55,"exam2":60,"exam3":58,"homework":6},
    {"name":"Maria","exam1":95,"exam2":92,"exam3":98,"homework":10},
    {"name":"John","exam1":70,"exam2":65,"exam3":72,"homework":8},
    {"name":"Sofia","exam1":40,"exam2":50,"exam3":45,"homework":5},
    {"name":"David","exam1":88,"exam2":91,"exam3":86,"homework":10}
]

def calculate(student):
    exam_avg = (student["exam1"] + student["exam2"] + student["exam3"]) / 3
    homework = student["homework"] / 10 * 100
    final = exam_avg * 0.7 + homework * 0.3
    status = "Pass" if final >= 60 else "Fail"
    excellent = student["exam1"] >= 90 and student["exam2"] >= 90 and student["exam3"] >= 90
    recovery = min(final + 5, 100) if final < 60 else final
    return {"name":student["name"], "final":final, "status":status,
            "excellent":excellent, "recovery":recovery}

results = []
for student in students:
    results.append(calculate(student))

print("RESULTS")
for s in results:
    print(s["name"], round(s["final"],2), s["status"],
          "Excellent:", s["excellent"], "Recovery:", round(s["recovery"],2))

total = 0
for s in results:
    total += s["final"]
print("Class average:", round(total / len(results), 2))

ranking = sorted(results, key=lambda s: s["final"], reverse=True)
print("Ranking:")
for s in ranking:
    print(s["name"], round(s["final"],2))

# Reflection:
# Procedural programming uses functions and step-by-step instructions.
# OOP groups data and methods in objects, which helps organize larger programs.
# Functional programming uses functions to transform data.
# NumPy is useful for fast calculations with arrays. Pandas is useful for tables,
# filtering, grouping, sorting, and saving CSV files.
