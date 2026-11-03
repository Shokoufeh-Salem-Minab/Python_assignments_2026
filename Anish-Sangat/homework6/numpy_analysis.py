# Homework 6 - NumPy
import numpy as np

# names and exam scores (each row is one student, each column is one exam)
names = np.array(["Anna", "Peter", "Maria", "John", "Sofia", "David"])
exams = np.array([
    [85, 90, 88],
    [55, 60, 58],
    [95, 92, 98],
    [70, 65, 72],
    [40, 50, 45],
    [88, 91, 86]
])

print("Exam array:")
print(exams)
print("Shape:", exams.shape)

# average for each student (axis=1 means across the row)
student_avg = np.mean(exams, axis=1)
print("\nStudent averages:")
print(student_avg)

# statistics for each exam (axis=0 means down the column)
print("\nExam averages:", np.mean(exams, axis=0))
print("Exam max:", np.max(exams, axis=0))
print("Exam min:", np.min(exams, axis=0))
print("Exam std:", np.std(exams, axis=0))
print("Exam median:", np.median(exams, axis=0))

# overall
print("\nOverall average:", np.mean(exams))

# boolean mask - students with average at least 85
mask = student_avg >= 85
print("\nMask:", mask)
print("Students with average >= 85:", names[mask])
print("Their averages:", student_avg[mask])