import numpy as np

from data import students

# ----- Create the arrays -----
names = np.array([student["name"] for student in students])

# 2D array: one row per student, one column per exam -> shape (6, 3)
exams = np.array([[student["exam1"], student["exam2"], student["exam3"]] for student in students])

# ----- Student averages (axis=1 -> across each row) -----
student_averages = exams.mean(axis=1)

# ----- Exam statistics (axis=0 -> down each column) -----
exam_means = exams.mean(axis=0)
exam_mins = exams.min(axis=0)
exam_maxs = exams.max(axis=0)
exam_stds = exams.std(axis=0)

# ----- Boolean masking -----
mask = student_averages >= 85
top_students = names[mask]


# ----- Report -----
print("===== NUMPY ANALYSIS =====")
print("\nExam scores (rows = students, columns = exams):")
print(exams)

print("\n----- STUDENT AVERAGES -----")
for name, average in zip(names, student_averages):
    print(f"{name}: {average:.2f}")

print("\n----- EXAM STATISTICS -----")
print("Mean:", np.round(exam_means, 2))
print("Min: ", exam_mins)
print("Max: ", exam_maxs)
print("Std: ", np.round(exam_stds, 2))

print("\n----- STUDENTS WITH EXAM AVERAGE >= 85 -----")
print("Mask:", mask)
print("Students:", top_students)
