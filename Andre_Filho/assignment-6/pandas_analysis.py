# Andre Filho - Homework 6 - Student Performance Analysis System
# 5. Pandas

import os
import pandas as pd

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]

if __name__ == "__main__":
    df = pd.DataFrame(students)

    df["exam_average"] = df[["exam1", "exam2", "exam3"]].mean(axis=1)
    df["homework_score"] = (df["homework"] / 10) * 100
    df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
    df["status"] = df["final_score"].apply(lambda score: "Pass" if score >= 60 else "Fail")

    print("--- Full report ---")
    print(df[["name", "exam_average", "homework_score", "final_score", "status"]].round(2))

    # filter: students who passed
    passed_df = df[df["status"] == "Pass"]
    print("\nStudents who passed:")
    print(passed_df[["name", "final_score"]].round(2))

    # sort: rank students best to worst
    ranking_df = df.sort_values("final_score", ascending=False)
    print("\nRanking (best to worst):")
    print(ranking_df[["name", "final_score"]].round(2))

    # value_counts(): how many students passed vs failed
    print("\nPass/Fail counts:")
    print(df["status"].value_counts())

    # groupby(): average final score per status group
    print("\nAverage final score by status:")
    print(df.groupby("status")["final_score"].mean().round(2))

    report_path = os.path.join(os.path.dirname(__file__), "student_report.csv")
    df.to_csv(report_path, index=False)
    print(f"\nReport exported to {report_path}")


# 6. Comparison and Reflection
#
# Procedural programming organizes the solution as a sequence of plain functions
# that receive a student dict and return a value (exam_average, final_score, ...).
# It is simple and direct, but all the functions are independent of each other and
# every function has to be told explicitly which dataset/list to work on - there is
# nothing bundling "a student" and "the operations on a student" together.
#
# OOP groups data and behaviour: a Student knows its own scores and how to compute
# its own final_score/status, and a Classroom knows how to manage a list of
# Students (average, filter, rank). This reads closer to the real-world problem
# ("a classroom of students") and scales better when more behaviour is added later,
# at the cost of more boilerplate (constructors, methods) for a problem this small.
#
# Functional programming avoids mutating state: map()/filter()/reduce()/sorted()
# all return new values instead of changing the original list of dicts in place,
# which makes it easier to reason about (no hidden side effects) but can be a bit
# less readable than a loop for someone not used to map/filter/reduce.
#
# NumPy is the right tool when the data is purely numeric (the exam scores matrix):
# vectorized operations (.mean(axis=...), boolean masking) replace explicit loops
# and are much faster on large datasets, but NumPy arrays do not carry labels
# (student names), so names have to be tracked separately in a parallel list.
#
# Pandas is the most convenient option for this kind of tabular, mixed data (names
# + numeric scores + a derived "status" label): the DataFrame keeps everything
# aligned by row, and high-level operations (value_counts(), groupby(), sort_values(),
# to_csv()) replace a lot of manual code. For a very small, one-off script the four
# previous approaches would already be enough, but Pandas becomes clearly useful as
# soon as the report needs to be filtered, grouped, or exported.
