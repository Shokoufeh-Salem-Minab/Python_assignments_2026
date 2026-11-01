# Homework 6 - Part 4: NumPy

import numpy as np

names = np.array(["Anna", "Peter", "Maria", "John", "Sofia", "David"])

# rows = students, columns = exam1, exam2, exam3
exams = np.array([
    [85, 90, 88],
    [55, 60, 58],
    [95, 92, 98],
    [70, 65, 72],
    [40, 50, 45],
    [88, 91, 86],
])
homework = np.array([9, 6, 10, 8, 5, 10])

# averages per student (axis=1 -> along the row)
student_avg = exams.mean(axis=1)
homework_score = homework / 10 * 100
final_score = 0.7 * student_avg + 0.3 * homework_score

print("Exam averages:", np.round(student_avg, 2))
print("Final scores: ", np.round(final_score, 2))

# statistics per exam (axis=0 -> along the column)
print("\n=== Exam statistics ===")
print("Mean:", np.round(exams.mean(axis=0), 2))
print("Max: ", exams.max(axis=0))
print("Min: ", exams.min(axis=0))
print("Std: ", np.round(exams.std(axis=0), 2))

# boolean masking
mask = student_avg >= 85
print("\nStudents with exam average >= 85:", names[mask])

# some extra masks without loops
print("Passed:", names[final_score >= 60])
print("Excellent:", names[np.all(exams >= 90, axis=1)])
print(f"Class average: {final_score.mean():.2f}")
