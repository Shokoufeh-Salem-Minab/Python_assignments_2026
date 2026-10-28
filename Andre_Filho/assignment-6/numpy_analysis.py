# Andre Filho - Homework 6 - Student Performance Analysis System
# 4. NumPy

import numpy as np

names = ["Anna", "Peter", "Maria", "John", "Sofia", "David"]

# one row per student, one column per exam
exam_scores = np.array([
    [85, 90, 88],
    [55, 60, 58],
    [95, 92, 98],
    [70, 65, 72],
    [40, 50, 45],
    [88, 91, 86],
])

if __name__ == "__main__":
    # average exam score per student, no explicit loop
    student_averages = exam_scores.mean(axis=1)
    print("--- Student exam averages ---")
    for name, avg in zip(names, student_averages):
        print(f"{name}: {avg:.2f}")

    # exam statistics across all students, no explicit loop
    exam_means = exam_scores.mean(axis=0)
    exam_mins = exam_scores.min(axis=0)
    exam_maxs = exam_scores.max(axis=0)
    exam_stds = exam_scores.std(axis=0)

    print("\n--- Exam statistics ---")
    for i in range(exam_scores.shape[1]):
        print(
            f"Exam {i + 1}: mean={exam_means[i]:.2f}, "
            f"min={exam_mins[i]}, max={exam_maxs[i]}, std={exam_stds[i]:.2f}"
        )

    # boolean masking: students whose exam average is at least 85
    mask = student_averages >= 85
    strong_students = np.array(names)[mask]
    print("\nStudents with exam average >= 85:", strong_students.tolist())
