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
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = (df["homework"] / 10) * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = df["final_score"].apply(lambda x: "Pass" if x >= 60 else "Fail")

passed_df = df[df["status"] == "Pass"]
sorted_df = df.sort_values(by="final_score", ascending=False)

print("Status Counts:\n", df["status"].value_counts())
print("\nGroupby Status (Mean Final Score):\n", df.groupby("status")["final_score"].mean())

sorted_df.to_csv("student_report.csv", index=False)

# --- Task 6: When Pandas is Useful ---
# Pandas is useful for working with structured, tabular data (like spreadsheets or SQL tables) containing mixed data types (strings and numbers). 
# It makes adding calculated columns, filtering, sorting, aggregating data (via groupby and value_counts), and exporting to files like CSV much easier and efficient.