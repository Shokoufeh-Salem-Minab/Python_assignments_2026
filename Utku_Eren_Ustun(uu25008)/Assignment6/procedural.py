students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

def analyze_students(data):
    results = []
    total_final = 0
    excellent = []

    for s in data:
        exam_avg = (s["exam1"] + s["exam2"] + s["exam3"]) / 3
        hw_score = (s["homework"] / 10) * 100
        final = 0.7 * exam_avg + 0.3 * hw_score
        status = "Pass" if final >= 60 else "Fail"
        recovery = min(final + 5, 100) if final < 60 else None
        is_exc = s["exam1"] >= 90 and s["exam2"] >= 90 and s["exam3"] >= 90

        if is_exc:
            excellent.append(s["name"])
        total_final += final

        results.append({
            "name": s["name"], "final": final, 
            "status": status, "recovery": recovery
        })

    class_avg = total_final / len(data)

    # Rank using a loop (selection sort)
    ranked = results[:]
    for i in range(len(ranked)):
        for j in range(i + 1, len(ranked)):
            if ranked[j]["final"] > ranked[i]["final"]:
                ranked[i], ranked[j] = ranked[j], ranked[i]

    return results, class_avg, excellent, ranked

results, class_avg, excellent, ranked = analyze_students(students)
print("Class Average:", round(class_avg, 2))
print("Excellent Students:", excellent)
print("Ranked:", [(r["name"], round(r["final"], 2), r["status"], r["recovery"]) for r in ranked])