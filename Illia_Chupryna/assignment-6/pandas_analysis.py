students = [{'name': 'Anna', 'exam1': 85, 'exam2': 90, 'exam3': 88, 'homework': 9}, {'name': 'Peter', 'exam1': 55, 'exam2': 60, 'exam3': 58, 'homework': 6}, {'name': 'Maria', 'exam1': 95, 'exam2': 92, 'exam3': 98, 'homework': 10}, {'name': 'John', 'exam1': 70, 'exam2': 65, 'exam3': 72, 'homework': 8}, {'name': 'Sofia', 'exam1': 40, 'exam2': 50, 'exam3': 45, 'homework': 5}, {'name': 'David', 'exam1': 88, 'exam2': 91, 'exam3': 86, 'homework': 10}]

import pandas as pd

df = pd.DataFrame(students)
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = df["homework"] * 10
df["final_score"] = df["exam_average"] * 0.7 + df["homework_score"] * 0.3
df["status"] = df["final_score"].apply(lambda x: "Pass" if x >= 60 else "Fail")
df["excellent"] = (df[["exam1", "exam2", "exam3"]] >= 90).all(axis=1)
df["recovery_score"] = df.apply(
    lambda r: min(r["final_score"] + 5, 100) if r["status"] == "Fail" else None,
    axis=1
)

print(df.round(2))
print("\nRanking:")
print(df.sort_values("final_score", ascending=False)[["name", "final_score", "status"]].round(2))
print("\nStatus counts:")
print(df["status"].value_counts())
print("\nAverage by status:")
print(df.groupby("status")["final_score"].mean().round(2))
df.to_csv("student_report.csv", index=False)
print("Saved student_report.csv")
