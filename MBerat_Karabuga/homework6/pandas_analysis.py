import pathlib
import pandas as pd
from data import students


def build_report(records):
    df = pd.DataFrame(records)
    exam_columns = ["exam1", "exam2", "exam3"]

    df["exam_average"] = df[exam_columns].mean(axis=1)
    df["homework_score"] = df["homework"] * 10
    df["final_score"] = 0.7 * df["exam_average"] + 0.3 * df["homework_score"]
    df["status"] = df["final_score"].gt(59).map({True: "Pass", False: "Fail"})
    df["excellent"] = df[exam_columns].gt(89).all(axis=1)
    # Only students below 60 get a recovery score; status stays unchanged.
    df["recovery_score"] = (df["final_score"] + 5).clip(upper=100).where(df["final_score"] < 60)
    df["rank"] = df["final_score"].rank(method="min", ascending=False).astype(int)
    return df


def main():
    df = build_report(students)

    # Filtering, sorting, value_counts(), and groupby() as required.
    passing = df.loc[df["status"] == "Pass"]
    high_exam = df.loc[df["exam_average"] >= 85]
    excellent = df.loc[df["excellent"]]
    ranking = df.sort_values(["final_score", "name"], ascending=[False, True])
    status_counts = df["status"].value_counts()
    by_status = df.groupby("status")["final_score"].agg(["count", "mean", "min", "max"])

    print("PANDAS ANALYSIS")
    print("\nRanked report:\n", ranking.round(2).to_string(index=False))
    print("\nPassing students:", passing["name"].tolist())
    print("Students with exam average >= 85:", high_exam["name"].tolist())
    print("Excellent students:", excellent["name"].tolist())
    print("\nStatus counts (value_counts):\n", status_counts.to_string())
    print("\nGrouped final score statistics (groupby):\n", by_status.round(2).to_string())
    print(f"\nClass average: {df['final_score'].mean():.2f}")

    output_path = pathlib.Path(__file__).with_name("student_report.csv")
    ranking.round(2).to_csv(output_path, index=False)
    print(f"\nExported CSV: {output_path}")


if __name__ == "__main__":
    main()