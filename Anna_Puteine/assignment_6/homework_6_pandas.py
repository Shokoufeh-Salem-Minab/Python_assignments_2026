import pandas as pd

from students_data import students

df = pd.DataFrame(students)

df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1).round(2)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = (0.7 * df["exam_average"] + 0.3 * df["homework_score"]).round(2)
df["status"] = df["final_score"].apply(lambda score: "Pass" if score >= 60 else "Fail")

print(df)

print("\nPassing students:")
print(df[df["status"] == "Pass"][["name", "final_score"]])

print("\nExam average >= 85:")
print(df[df["exam_average"] >= 85][["name", "exam_average"]])

print("\nRanking:")
ranked = df.sort_values("final_score", ascending=False)
print(ranked[["name", "final_score", "status"]])

print("\nStatus count:")
print(df["status"].value_counts())

print("\nAverage by status:")
print(df.groupby("status")[["exam_average", "final_score"]].mean().round(2))

ranked.to_csv("student_report.csv", index=False)
print("\nReport saved to student_report.csv")


