"""Task 1 - Procedural programming: functions, loops and conditions."""
from data import (students, PASS_MARK, EXCELLENT_MARK, RECOVERY_BONUS,
                  EXAM_WEIGHT, HOMEWORK_WEIGHT)


def exam_average(student):
    return (student["exam1"] + student["exam2"] + student["exam3"]) / 3


def homework_score(student):
    return student["homework"] / 10 * 100


def final_score(student):
    return EXAM_WEIGHT * exam_average(student) + HOMEWORK_WEIGHT * homework_score(student)


def status(score):
    return "Pass" if score >= PASS_MARK else "Fail"


def is_excellent(student):
    return (student["exam1"] >= EXCELLENT_MARK
            and student["exam2"] >= EXCELLENT_MARK
            and student["exam3"] >= EXCELLENT_MARK)


def recovery_score(score):
    """Only for final < 60: +5 points, capped at 100. Status is not changed."""
    if score < PASS_MARK:
        return min(score + RECOVERY_BONUS, 100)
    return None


def class_average(results):
    total = 0
    for r in results:
        total += r["final"]
    return total / len(results)


def rank_students(results):
    """Simple selection sort (descending by final score) using loops."""
    ranked = results[:]
    for i in range(len(ranked)):
        best = i
        for j in range(i + 1, len(ranked)):
            if ranked[j]["final"] > ranked[best]["final"]:
                best = j
        ranked[i], ranked[best] = ranked[best], ranked[i]
    return ranked


def main():
    results = []
    for s in students:
        final = final_score(s)
        results.append({
            "name": s["name"],
            "exam_avg": exam_average(s),
            "hw": homework_score(s),
            "final": final,
            "status": status(final),
            "excellent": is_excellent(s),
            "recovery": recovery_score(final),
        })

    print("=== PROCEDURAL ===")
    for r in results:
        line = (f"{r['name']:<6} exam_avg={r['exam_avg']:.2f} hw={r['hw']:.0f} "
                f"final={r['final']:.2f} {r['status']}")
        if r["excellent"]:
            line += " | EXCELLENT"
        if r["recovery"] is not None:
            line += f" | recovery={r['recovery']:.2f}"
        print(line)

    print(f"\nClass average: {class_average(results):.2f}")
    print("Ranking:")
    for place, r in enumerate(rank_students(results), start=1):
        print(f"  {place}. {r['name']:<6} {r['final']:.2f}")


if __name__ == "__main__":
    main()
