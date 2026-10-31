students = [{'name': 'Anna', 'exam1': 85, 'exam2': 90, 'exam3': 88, 'homework': 9}, {'name': 'Peter', 'exam1': 55, 'exam2': 60, 'exam3': 58, 'homework': 6}, {'name': 'Maria', 'exam1': 95, 'exam2': 92, 'exam3': 98, 'homework': 10}, {'name': 'John', 'exam1': 70, 'exam2': 65, 'exam3': 72, 'homework': 8}, {'name': 'Sofia', 'exam1': 40, 'exam2': 50, 'exam3': 45, 'homework': 5}, {'name': 'David', 'exam1': 88, 'exam2': 91, 'exam3': 86, 'homework': 10}]

def calculate(s):
    exam = (s["exam1"] + s["exam2"] + s["exam3"]) / 3
    homework = s["homework"] * 10
    final = exam * 0.7 + homework * 0.3
    status = "Pass" if final >= 60 else "Fail"
    excellent = all(s[k] >= 90 for k in ("exam1", "exam2", "exam3"))
    recovery = min(final + 5, 100) if status == "Fail" else None
    return {**s, "exam_average": exam, "homework_score": homework,
            "final_score": final, "status": status, "excellent": excellent,
            "recovery_score": recovery}

results = []
for s in students:
    results.append(calculate(s))

ranking = sorted(results, key=lambda s: s["final_score"], reverse=True)
average = sum(s["final_score"] for s in results) / len(results)
for s in ranking:
    print(s["name"], round(s["final_score"], 2), s["status"])
print("Class average:", round(average, 2))
print("Excellent:", [s["name"] for s in results if s["excellent"]])
print("Failing:", [s["name"] for s in results if s["status"] == "Fail"])
print("Recovery:", [(s["name"], round(s["recovery_score"], 2)) for s in results if s["status"] == "Fail"])
