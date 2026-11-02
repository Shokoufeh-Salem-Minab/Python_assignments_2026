students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

from functools import reduce

def calc_student(s):
    exam_avg = (s["exam1"] + s["exam2"] + s["exam3"]) / 3
    hw_score = (s["homework"] / 10) * 100
    final = 0.7 * exam_avg + 0.3 * hw_score
    return {
        **s,
        "final": final,
        "status": "Pass" if final >= 60 else "Fail",
        "excellent": s["exam1"] >= 90 and s["exam2"] >= 90 and s["exam3"] >= 90,
        "recovery": min(final + 5, 100) if final < 60 else None
    }

processed = list(map(calc_student, students))
excellent = list(filter(lambda s: s["excellent"], processed))
passed = list(filter(lambda s: s["status"] == "Pass", processed))
total_final = reduce(lambda acc, s: acc + s["final"], processed, 0)
class_avg = total_final / len(processed)
ranked = sorted(processed, key=lambda s: s["final"], reverse=True)

print("Class Average:", round(class_avg, 2))
print("Excellent Students:", [s["name"] for s in excellent])
print("Ranked:", [(s["name"], round(s["final"], 2), s["status"], s["recovery"]) for s in ranked])

# --- Task 6: Comparison of the Three Programming Paradigms ---
# 1. Procedural Programming: Relies on step-by-step instructions, loops, and modifying state directly. 
#    Strength: Simple and straightforward for small scripts. Limitation: Harder to scale and maintain as logic grows.
# 2. Object-Oriented Programming (OOP): Bundles data (attributes) and behaviors (methods) into classes (Student, Classroom). 
#    Strength: Modular, reusable, and great for modeling real-world entities. Limitation: Requires more boilerplate code.
# 3. Functional Programming (FP): Uses pure functions and immutable data transformations (map, filter, reduce, sorted). 
#    Strength: Predictable and avoids side effects (does not alter the original dataset). Limitation: Can feel less intuitive for complex state changes.