import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

students = [{"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
            {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
            {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
            {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
            {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
            {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}]


def get_status(score):
    if score >= 60:
        return "Pass"
    return "Fail"

df = pd.DataFrame(students)

# calculate with full precision first, round only at the end
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = df["final_score"].apply(get_status)
df = df.round(2)

print(df)

print("\nStudents who passed:")
print(df[df["status"] == "Pass"])

print("\nRanking:")
df = df.sort_values("final_score", ascending=False)
print(df[["name", "final_score", "status"]])

print("\nNumber of students by status:")
print(df["status"].value_counts())

print("\nAverage final score by status:")
print(df.groupby("status")["final_score"].mean().round(2))

df.to_csv("student_report.csv", index=False)
print("\nReport saved as student_report.csv")


# Comparison and reflection - Pandas:
# Pandas puts the data in a table (DataFrame) with named columns, like a spreadsheet.
# New columns, filtering, sorting, counting (value_counts) and grouping (groupby) each
# take one line, and the result can be saved straight to a CSV file. It is useful for
# real data analysis and reports, especially with mixed data such as names, numbers and
# text. Its limitation is that it is a big library, which is more than needed for very
# simple tasks, and it is slower than NumPy for pure number crunching.
