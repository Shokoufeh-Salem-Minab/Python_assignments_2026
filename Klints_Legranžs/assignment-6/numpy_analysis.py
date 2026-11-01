"""Task 4 - NumPy: vectorised analysis without loops."""
import numpy as np
from data import students

names = np.array([s["name"] for s in students])
exams = np.array([[s["exam1"], s["exam2"], s["exam3"]] for s in students])

student_avg = exams.mean(axis=1)
exam_mean = exams.mean(axis=0)
exam_max = exams.max(axis=0)
exam_min = exams.min(axis=0)
exam_std = exams.std(axis=0)
exam_median = np.median(exams, axis=0)

mask = student_avg >= 85

print("=== NUMPY ===")
print("Exam scores array:\n", exams)
print("\nStudent averages:")
print(np.column_stack((names, student_avg.round(2))))
print("\nPer-exam statistics (exam1, exam2, exam3):")
print("  mean:  ", exam_mean.round(2))
print("  median:", exam_median)
print("  max:   ", exam_max)
print("  min:   ", exam_min)
print("  std:   ", exam_std.round(2))
print("\nOverall mean of all exams:", exams.mean().round(2))
print("\nStudents with exam average >= 85:", names[mask].tolist())
print("Their averages:", student_avg[mask].round(2))
