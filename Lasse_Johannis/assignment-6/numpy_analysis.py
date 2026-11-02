# Homework 6 - Student Performance Analysis System
# Part 4: NumPy
# Lasse Johannis

import numpy as np
from dataset import students

names = np.array([student["name"] for student in students])

# rows = students, columns = exam1, exam2, exam3
exams = np.array([[student["exam1"], student["exam2"], student["exam3"]] for student in students])
print("Exam scores:")
print(exams)
print("Shape:", exams.shape)

# axis=1 -> per student (row), axis=0 -> per exam (column)
student_averages = exams.mean(axis=1)
print("\nStudent averages:", np.round(student_averages, 2))

print("\nExam statistics (exam1, exam2, exam3):")
print("Mean:", np.round(exams.mean(axis=0), 2))
print("Min:", exams.min(axis=0))
print("Max:", exams.max(axis=0))
print("Std:", np.round(exams.std(axis=0), 2))

# Boolean masking
mask = student_averages >= 85
print("\nMask:", mask)
print("Exam average at least 85:", names[mask])
print("Their averages:", np.round(student_averages[mask], 2))
