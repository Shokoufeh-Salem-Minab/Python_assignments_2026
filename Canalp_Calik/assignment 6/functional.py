from functools import reduce

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

def map_student(s):
    exam_avg = (s["exam1"] + s["exam2"] + s["exam3"]) / 3
    hw_score = (s["homework"] / 10) * 100
    final = 0.7 * exam_avg + 0.3 * hw_score
    return {
        **s, 
        "exam_average": exam_avg, 
        "homework_score": hw_score, 
        "final_score": final, 
        "status": "Pass" if final >= 60 else "Fail"
    }

fp_mapped = list(map(map_student, students))
fp_filtered = list(filter(lambda s: s["status"] == "Pass", fp_mapped))
fp_total = reduce(lambda acc, s: acc + s["final_score"], fp_mapped, 0)
fp_class_avg = fp_total / len(fp_mapped)
fp_ranked = sorted(fp_mapped, key=lambda s: s["final_score"], reverse=True)
