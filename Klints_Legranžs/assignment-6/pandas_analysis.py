"""Task 5 - Pandas: DataFrame analysis and CSV export."""
import numpy as np
import pandas as pd
from data import students, PASS_MARK, EXCELLENT_MARK, RECOVERY_BONUS

df = pd.DataFrame(students)

df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = np.where(df["final_score"] >= PASS_MARK, "Pass", "Fail")

df["excellent"] = (df[["exam1", "exam2", "exam3"]] >= EXCELLENT_MARK).all(axis=1)
df["recovery_score"] = np.where(
    df["final_score"] < PASS_MARK,
    (df["final_score"] + RECOVERY_BONUS).clip(upper=100),
    np.nan,
)

print("=== PANDAS ===")
print(df.round(2).to_string(index=False))

print("\nStudents with final_score >= 60, sorted (best first):")
print(df[df["final_score"] >= PASS_MARK]
      .sort_values("final_score", ascending=False)[["name", "final_score", "status"]]
      .round(2).to_string(index=False))

print("\nStatus counts (value_counts):")
print(df["status"].value_counts())

print("\nGroupby status (mean scores):")
print(df.groupby("status")[["exam_average", "homework_score", "final_score"]].mean().round(2))

print("\nClass average final score:", round(df["final_score"].mean(), 2))

df.round(2).to_csv("student_report.csv", index=False)
print("\nSaved student_report.csv")

# ---------------------------------------------------------------------------
# TASK 6 - COMPARISON AND REFLECTION
#
# Procedural: a sequence of functions operating on plain data (lists/dicts),
#   using loops and conditions. Strengths: simple, easy to read and trace,
#   great for small scripts. Limits: data and behaviour are separate, so as the
#   program grows, code gets repetitive and harder to reuse and maintain.
#
# OOP: data and behaviour are bundled in classes (Student, Classroom).
#   Strengths: clear structure, encapsulation, easy to extend (new methods,
#   subclasses) and model real-world entities. Limits: more boilerplate and
#   design effort; overkill for tiny tasks; objects carry mutable state.
#
# Functional: small pure functions, no side effects, using map/filter/reduce/
#   sorted; the original data is never changed. Strengths: predictable, easy to
#   test and reason about, composable, safe for parallel work. Limits: can be
#   less readable for beginners (lambdas, reduce), creates new copies of data,
#   and Python is not a purely functional language.
#
# NumPy: fast, vectorised math on n-dimensional arrays with no explicit loops
#   (axis operations, Boolean masks). Best for homogeneous numeric data and
#   statistics. Limits: no column names, one data type per array.
#
# Pandas: labelled tables (DataFrames) for mixed-type data: adding columns,
#   filtering, sorting, value_counts(), groupby(), and CSV import/export. Best
#   for real-world tabular data and reporting. Limits: heavier and slower than
#   NumPy for pure numeric work, and more memory use on very large data.
#
# ---------------------------------------------------------------------------
