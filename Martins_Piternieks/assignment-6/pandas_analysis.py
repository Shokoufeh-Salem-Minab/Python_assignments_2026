import os

import pandas as pd

from data import students, PASS_SCORE

# ----- Global Settings -----
REPORT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "student_report.csv")

# ----- Create the DataFrame -----
df = pd.DataFrame(students)

# ----- Add new columns -----
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = df["final_score"].apply(lambda score: "Pass" if score >= PASS_SCORE else "Fail")
df = df.round(2)

# ----- Filter and sort -----
passed = df[df["status"] == "Pass"]
ranking = df.sort_values("final_score", ascending=False)

# ----- value_counts() and groupby() -----
status_counts = df["status"].value_counts()
average_by_status = df.groupby("status")["final_score"].mean().round(2)

# ----- Export -----
df.to_csv(REPORT_FILE, index=False)


# ----- Report -----
print("===== PANDAS ANALYSIS =====")
print("\n----- FULL TABLE -----")
print(df.to_string())  # to_string() shows all columns

print("\n----- PASSED STUDENTS -----")
print(passed[["name", "final_score"]])

print("\n----- RANKING -----")
print(ranking[["name", "final_score", "status"]])

print("\n----- STATUS COUNTS -----")
print(status_counts)

print("\n----- AVERAGE FINAL SCORE BY STATUS -----")
print(average_by_status)

print(f"\nReport saved to {REPORT_FILE}")
