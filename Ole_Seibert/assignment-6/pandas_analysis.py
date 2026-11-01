# Homework 6 - Part 5: Pandas

import pandas as pd

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]

df = pd.DataFrame(students)

# new columns
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1).round(2)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = (0.7 * df["exam_average"] + 0.3 * df["homework_score"]).round(2)
df["status"] = df["final_score"].apply(lambda x: "Pass" if x >= 60 else "Fail")

print(df)

# filter
print("\n=== Passed students ===")
print(df[df["status"] == "Pass"][["name", "final_score"]])

print("\n=== Excellent students ===")
print(df[(df["exam1"] >= 90) & (df["exam2"] >= 90) & (df["exam3"] >= 90)][["name"]])

# sort
ranking = df.sort_values("final_score", ascending=False)
print("\n=== Ranking ===")
print(ranking[["name", "final_score", "status"]].to_string(index=False))

# value_counts and groupby
print("\n=== Pass / Fail count ===")
print(df["status"].value_counts())

print("\n=== Average per status ===")
print(df.groupby("status")[["exam_average", "final_score"]].mean().round(2))

print(f"\nClass average: {df['final_score'].mean():.2f}")

# export
ranking.to_csv("student_report.csv", index=False)
print("\nReport saved to student_report.csv")


# ============================================================
# Part 6: Comparison and Reflection
# ============================================================
#
# Procedural programming:
# The program is a list of steps with functions, loops and if statements.
# It is easy to read and good for small scripts like this one. The problem
# is that data and functions are separate, so with a bigger project it gets
# hard to keep track of which function changes which data.
#
# Object-Oriented Programming:
# Data and behaviour are put together in classes (Student, Classroom).
# Every student "knows" how to calculate his own score. This makes the code
# more structured and easier to extend (e.g. add a new method or a new kind
# of student). The downside is more code and more planning for a small task.
#
# Functional Programming:
# Uses pure functions and map/filter/reduce/sorted, and the original data is
# never changed. This makes the results predictable and easy to test,
# because the same input always gives the same output. But code with a lot
# of lambdas and nested map/filter can be harder to read for beginners.
#
# NumPy and Pandas:
# NumPy is useful when you have numeric data in arrays and want fast
# calculations without loops (mean per row/column, boolean masks).
# Pandas builds on top of NumPy and is better for table data with column
# names: adding columns, filtering, sorting, grouping and exporting to CSV
# needs only a few lines. For real data analysis these two are much faster
# and shorter than writing everything by hand with loops.
