# Assignment 6: tabular student performance analysis with pandas.

from pathlib import Path

import pandas as pd

STUDENTS = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]
REPORT_PATH = Path(__file__).with_name("student_report.csv")


def create_report(students=STUDENTS):
    # Create a DataFrame without adding fields to source records.
    dataframe = pd.DataFrame(students)
    dataframe["exam_average"] = dataframe[["exam1", "exam2", "exam3"]].mean(axis=1)
    dataframe["homework_score"] = dataframe["homework"] / 10 * 100
    dataframe["final_score"] = 0.7 * dataframe["exam_average"] + 0.3 * dataframe["homework_score"]
    dataframe["status"] = dataframe["final_score"].ge(60).map({True: "Pass", False: "Fail"})
    dataframe["recovery_score"] = (dataframe["final_score"] + 5).clip(upper=100).mask(
        dataframe["status"] == "Pass"
    )
    return dataframe


def main():
    report = create_report()
    passing_students = report.loc[report["status"] == "Pass"]
    ranking = report.sort_values("final_score", ascending=False)
    status_counts = report["status"].value_counts()
    status_averages = report.groupby("status")["final_score"].mean()
    report.to_csv(REPORT_PATH, index=False, float_format="%.2f")

    print("Passing students:\n", passing_students[["name", "final_score"]])
    print("\nRanked students:\n", ranking[["name", "final_score"]])
    print("\nStatus counts:\n", status_counts)
    print("\nAverage final score by status:\n", status_averages)
    print(f"\nReport exported to {REPORT_PATH}")


if __name__ == "__main__":
    main()
