# Homework 6 - Pandas
import pandas as pd

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

df = pd.DataFrame(students)

# new columns
df["exam_average"] = (df["exam1"] + df["exam2"] + df["exam3"]) / 3
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = df["exam_average"] * 0.7 + df["homework_score"] * 0.3
df["status"] = df["final_score"].apply(lambda x: "Pass" if x >= 60 else "Fail")

# extra columns: excellent and recovery score
df["excellent"] = (df["exam1"] >= 90) & (df["exam2"] >= 90) & (df["exam3"] >= 90)
df["recovery_score"] = df["final_score"].apply(lambda x: min(x + 5, 100) if x < 60 else None)

print("Full report:")
print(df.round(2))

# filter - only passed students
print("\nPassed students:")
print(df[df["status"] == "Pass"][["name", "final_score"]].round(2))

# sort by final score
print("\nSorted by final score:")
sorted_df = df.sort_values("final_score", ascending=False)
print(sorted_df[["name", "final_score", "status"]].round(2))

# value_counts
print("\nHow many passed and failed:")
print(df["status"].value_counts())

# groupby
print("\nAverages by status:")
print(df.groupby("status")[["exam_average", "homework_score", "final_score"]].mean().round(2))

# save to csv
df.round(2).to_csv("student_report.csv", index=False)
print("\nSaved to student_report.csv")



# Comparison of the paradigms
#
# Procedural: step-by-step functions and loops. Simple and good for small
# programs, but gets messy and hard to reuse when the program grows.
#
# OOP: data and methods are together in classes (Student, Classroom).
# Well organized and easy to extend, but needs more code and planning.
#
# Functional: small functions that don't change the original data, using
# map, filter, reduce and sorted. Safe and easy to test, but lambda and
# reduce can be hard to read.
#
# NumPy is good for fast number calculations on arrays without loops.
# Pandas is good for tables with different data types: adding columns,
# filtering, sorting, grouping and saving to CSV.