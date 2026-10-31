# Assignment 6: vectorised examination analysis with NumPy.

import numpy as np

NAMES = np.array(["Anna", "Peter", "Maria", "John", "Sofia", "David"])
EXAM_SCORES = np.array([
    [85, 90, 88], [55, 60, 58], [95, 92, 98],
    [70, 65, 72], [40, 50, 45], [88, 91, 86],
], dtype=float)


def analyze_exams(scores=EXAM_SCORES, names=NAMES):
    # Calculate examination measures using array operations.
    student_averages = scores.mean(axis=1)
    statistics = {
        "minimum": scores.min(), "maximum": scores.max(),
        "mean": scores.mean(), "standard_deviation": scores.std(),
        "exam_means": scores.mean(axis=0),
    }
    high_achievers = names[student_averages >= 85]
    return student_averages, statistics, high_achievers


def main():
    averages, statistics, high_achievers = analyze_exams()
    print("Student examination averages:", dict(zip(NAMES, np.round(averages, 2))))
    print("Examination statistics:", statistics)
    print("Students with exam average >= 85:", ", ".join(high_achievers))


if __name__ == "__main__":
    main()
