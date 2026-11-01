# Task 5: Pandas
# make a DataFrame, add the new columns, filter, sort, group and save a csv.

import pandas as pd

# the dataset from the homework
students = [
    {"name": "Anna",  "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John",  "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def check_students(data):
    # small safety check so the programs stop with a clear message
    # if the data is broken (empty list, missing key, score out of range)
    if len(data) == 0:
        raise ValueError("the student list is empty")

    for s in data:
        for key in ["name", "exam1", "exam2", "exam3", "homework"]:
            if key not in s:
                raise ValueError(f"student {s} is missing the key '{key}'")

        for key in ["exam1", "exam2", "exam3", "homework"]:
            value = s[key]
            # bool is also a number in python so i block it separately
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{s['name']}: {key} must be a number")

        for key in ["exam1", "exam2", "exam3"]:
            if s[key] < 0 or s[key] > 100:
                raise ValueError(f"{s['name']}: {key} must be between 0 and 100")

        # homework is how many of the 10 assignments were submitted
        if s["homework"] < 0 or s["homework"] > 10:
            raise ValueError(f"{s['name']}: homework must be between 0 and 10")


check_students(students)

# so the whole table is visible in the terminal and not cut with "..."
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)

df = pd.DataFrame(students)

# new columns (pandas does it for the whole column at once, no loop needed)
df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = df["final_score"].apply(lambda x: "Pass" if x >= 60 else "Fail")

# two extra columns from the assessment rules
# excellent = all 3 exams are 90+
df["excellent"] = (df[["exam1", "exam2", "exam3"]] >= 90).all(axis=1)
# recovery = final + 5 (max 100), but only for final < 60, others stay empty (NaN)
df["recovery_score"] = (df["final_score"] + 5).clip(upper=100).where(df["final_score"] < 60)

# round at the end so the status above was calculated with the real numbers
df = df.round(2)

print("--- Pandas ---")
print(df, "\n")

# filter: only students who passed, best one first
passed = df[df["status"] == "Pass"].sort_values("final_score", ascending=False, kind="stable")
print("Passed students (best first):")
print(passed[["name", "final_score"]], "\n")

# value_counts = how many Pass and how many Fail
print("Status counts:")
print(df["status"].value_counts(), "\n")

# groupby = average numbers separately for Pass and Fail
print("Averages by status:")
print(df.groupby("status")[["exam_average", "homework_score", "final_score"]].mean().round(2), "\n")

# save the report, best student on top
report = df.sort_values("final_score", ascending=False, kind="stable")
report.to_csv("student_report.csv", index=False)
print("Saved student_report.csv")


# ----------------------------------------------------------------------
# Task 6: Comparison and reflection (my own words)
#
# Procedural: just functions and loops, step by step from top to bottom.
#   + simple and easy to follow, good for small programs like this one
#   - the data (dicts) and the functions are separate, so when the program
#     gets bigger it gets messy and hard to keep track of
#
# OOP: the data and the functions that use it are together in a class
#   (Student, Classroom).
#   + organized, easy to reuse and add new things later
#   - more code and setup, a bit too much for such a small problem
#
# Functional: small functions that don't change anything outside, with
#   map / filter / reduce / sorted. The original data stays the same.
#   + easy to test and no surprise side effects
#   - lambdas and reduce can be hard to read at first
#
# NumPy is good when there are lots of numbers in arrays. It does math on
# the whole array at once (mean, std, masks) without loops, and it is fast.
# Pandas is good for tables with column names: adding columns, filtering,
# sorting, groupby, and reading / saving csv files.
# With only 6 students normal python is enough, but with thousands of
# rows NumPy and Pandas would be much shorter and faster.
# ----------------------------------------------------------------------
