# Homework 6 
# Srivishva Melvin Marimouttou, sm25017
# Program created on: 27/10/2026

import pandas as pd

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]

pd.set_option("display.width", 200) # show all columns in the terminal
pd.set_option("display.max_columns", None)

df = pd.DataFrame(students)
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = (df["homework"] / 10) * 100
df["final_score"] = (0.7 * df["exam_average"]) + (0.3 * df["homework_score"])
df["status"] = (df["final_score"] >= 60).map({True: "Pass", False: "Fail"})

print("Full table:")
print(df.round(2))

print("\nPassing students (filter):")
print(df[df["status"] == "Pass"][["name", "final_score"]].round(2))

print("\nRanking (sorted by final_score, highest first):")
ranked = df.sort_values("final_score", ascending=False)
print(ranked[["name", "final_score", "status"]].round(2).to_string(index=False))

print("\nvalue_counts() of status:")
print(df["status"].value_counts())

print("\ngroupby('status') averages:")
print(df.groupby("status")[["exam_average", "homework_score", "final_score"]].mean().round(2))

# export the report
report = ranked[["name", "exam1", "exam2", "exam3", "homework",
                 "exam_average", "homework_score", "final_score", "status"]].round(2)
report.to_csv("student_report.csv", index=False)
print("\nSaved student_report.csv")
