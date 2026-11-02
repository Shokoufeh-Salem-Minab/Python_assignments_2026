# Homework 6 - Student Performance Analysis System
# Part 5: Pandas
# Lasse Johannis

import pandas as pd
from dataset import students

df = pd.DataFrame(students)
exams = ["exam1", "exam2", "exam3"]

df["exam_average"] = df[exams].mean(axis=1)
df["homework_score"] = df["homework"] / 10 * 100
df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
df["status"] = "Fail"
df.loc[df["final_score"] >= 60, "status"] = "Pass"

df = df.round(2)
columns = ["name", "exam_average", "homework_score", "final_score", "status"]
print(df[columns])

print("\nPassed students:")
print(df[df["status"] == "Pass"][columns])

print("\nExam average at least 85 and full homework:")
print(df[(df["exam_average"] >= 85) & (df["homework"] == 10)][columns])

report = df.sort_values("final_score", ascending=False)
print("\nSorted by final score:")
print(report[columns])

print("\nStatus counts:")
print(report["status"].value_counts())

print("\nAverage final score per status:")
print(report.groupby("status")["final_score"].mean().round(2))

report.to_csv("student_report.csv", index=False)
print("\nReport saved to student_report.csv")


# ----- Part 6: Comparison and Reflection -----
#
# Procedural programming writes the program as a list of steps: functions,
# loops and conditions that work on the data one after another. It is the
# easiest to read for a small task like this, but the data and the functions
# are separate, so a bigger program gets harder to organize.
#
# Object-oriented programming puts the data and the behaviour together. A
# Student object knows its own scores and can calculate its final score and
# status, and the Classroom manages all students. This is clear and easy to
# extend (for example a new kind of student through inheritance), but it needs
# more code and the objects keep a state that can change.
#
# Functional programming transforms data with pure functions and higher-order
# functions like map(), filter(), reduce() and sorted(). The original list is
# never changed, which avoids side effects and makes each function easy to
# test. The limitation is that long chains of map/filter/lambda are harder to
# read than a simple loop.
#
# NumPy is useful for numbers in arrays: the averages and statistics of all
# students are calculated at once without loops, which is shorter and faster
# for big data. Pandas is useful for tables with mixed data (names, scores,
# status): adding columns, filtering, sorting, grouping and exporting to CSV
# need only one line each, so it is the best choice for a report like this.
