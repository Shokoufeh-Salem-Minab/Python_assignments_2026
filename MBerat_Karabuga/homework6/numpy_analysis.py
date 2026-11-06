import numpy as np
from data import students


def main():
    # Input construction uses a comprehension; all numerical calculations below
    # are vectorized NumPy operations (no explicit calculation loops).
    names = np.array([student["name"] for student in students])
    exams = np.array(
        [[student["exam1"], student["exam2"], student["exam3"]] for student in students],
        dtype=float,
    )
    homework = np.array([student["homework"] for student in students], dtype=float)

    # Rows = students; columns = exam1, exam2, exam3.
    exam_averages = exams.mean(axis=1)
    exam_means = exams.mean(axis=0)
    exam_medians = np.median(exams, axis=0)
    exam_minimums = exams.min(axis=0)
    exam_maximums = exams.max(axis=0)
    exam_std = exams.std(axis=0)  # population standard deviation

    homework_scores = homework * 10
    final_scores = 0.7 * exam_averages + 0.3 * homework_scores
    passing_mask = final_scores > 59
    excellent_mask = np.all(exams > 89, axis=1)
    recovery_scores = np.where(final_scores < 60, np.minimum(final_scores + 5, 100), np.nan)
    high_exam_mask = exam_averages >= 85  # Boolean masking required by HW6.
    ranking_indices = np.argsort(-final_scores, kind="stable")

    np.set_printoptions(precision=2, suppress=True)
    print("NUMPY ANALYSIS")
    print("Exam scores (2D array):\n", exams)
    print("Exam averages by student:", exam_averages)
    print("Exam means [1, 2, 3]:", exam_means)
    print("Exam medians:", exam_medians)
    print("Exam minimums:", exam_minimums)
    print("Exam maximums:", exam_maximums)
    print("Exam standard deviations:", exam_std)
    print("Final scores:", final_scores)
    print("Pass mask:", passing_mask)
    print("Excellent students:", names[excellent_mask])
    print("Recovery scores (nan = not applicable):", recovery_scores)
    print("Students with exam average >= 85:", names[high_exam_mask])
    print("Class average:", round(float(final_scores.mean()), 2))
    print("Ranked names:", names[ranking_indices])
    print("Ranked scores:", final_scores[ranking_indices])


if __name__ == "__main__":
    main()
