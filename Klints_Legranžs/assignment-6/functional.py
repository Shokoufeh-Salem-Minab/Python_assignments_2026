"""Task 3 - Functional programming: pure functions, map/filter/reduce/sorted.

The original dataset is never modified: every function returns new values.
"""
from functools import reduce
from data import (students, PASS_MARK, EXCELLENT_MARK, RECOVERY_BONUS,
                  EXAM_WEIGHT, HOMEWORK_WEIGHT)


def exam_average(s):
    return (s["exam1"] + s["exam2"] + s["exam3"]) / 3


def homework_score(s):
    return s["homework"] / 10 * 100


def final_score(s):
    return EXAM_WEIGHT * exam_average(s) + HOMEWORK_WEIGHT * homework_score(s)


def recovery_score(final):
    return min(final + RECOVERY_BONUS, 100) if final < PASS_MARK else None


def is_excellent(s):
    return all(s[k] >= EXCELLENT_MARK for k in ("exam1", "exam2", "exam3"))


def with_scores(s):
    """Return a NEW dict (the input is copied, not mutated)."""
    final = final_score(s)
    return {
        **s,
        "exam_avg": exam_average(s),
        "hw_score": homework_score(s),
        "final": final,
        "status": "Pass" if final >= PASS_MARK else "Fail",
        "excellent": is_excellent(s),
        "recovery": recovery_score(final),
    }


def total_final(results):
    return reduce(lambda acc, r: acc + r["final"], results, 0)


def class_average(results):
    return total_final(results) / len(results)


def main():
    results = list(map(with_scores, students))                    
    passed = list(filter(lambda r: r["status"] == "Pass", results))
    failed = list(filter(lambda r: r["status"] == "Fail", results))
    excellent = list(filter(lambda r: r["excellent"], results))
    ranking = sorted(results, key=lambda r: r["final"], reverse=True)

    print("=== FUNCTIONAL ===")
    for r in results:
        line = (f"{r['name']:<6} exam_avg={r['exam_avg']:.2f} hw={r['hw_score']:.0f} "
                f"final={r['final']:.2f} {r['status']}")
        if r["excellent"]:
            line += " | EXCELLENT"
        if r["recovery"] is not None:
            line += f" | recovery={r['recovery']:.2f}"
        print(line)

    print(f"\nTotal final score: {total_final(results):.2f}")
    print(f"Class average: {class_average(results):.2f}")
    print("Passed:   ", [r["name"] for r in passed])
    print("Failed:   ", [r["name"] for r in failed])
    print("Excellent:", [r["name"] for r in excellent])
    print("Ranking:")
    for place, r in enumerate(ranking, start=1):
        print(f"  {place}. {r['name']:<6} {r['final']:.2f}")

    assert all(set(s) == {"name", "exam1", "exam2", "exam3", "homework"} for s in students)


if __name__ == "__main__":
    main()
