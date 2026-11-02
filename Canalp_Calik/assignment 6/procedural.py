students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

def p_exam_avg(s): 
    return (s["exam1"] + s["exam2"] + s["exam3"]) / 3

def p_hw_score(s): 
    return (s["homework"] / 10) * 100

def p_final_score(s): 
    return 0.7 * p_exam_avg(s) + 0.3 * p_hw_score(s)

def p_status(s): 
    return "Pass" if p_final_score(s) >= 60 else "Fail"

def p_excellent(s): 
    return s["exam1"] >= 90 and s["exam2"] >= 90 and s["exam3"] >= 90

def p_recovery(s):
    fs = p_final_score(s)
    return min(fs + 5, 100) if fs < 60 else None

proc_results = []
total_score = 0
for student in students:
    fs = p_final_score(student)
    total_score += fs
    proc_results.append({
        "name": student["name"],
        "final_score": fs,
        "status": p_status(student),
        "excellent": p_excellent(student),
        "recovery": p_recovery(student)
    })

proc_class_avg = total_score / len(students)
proc_ranked = sorted(proc_results, key=lambda x: x["final_score"], reverse=True)
