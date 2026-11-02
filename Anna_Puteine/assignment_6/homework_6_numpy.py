import numpy as np

from students_data import students

names = np.array([student["name"] for student in students])
exams = np.array([[student["exam1"], student["exam2"], student["exam3"]] for student in students])
homework = np.array([student["homework"] for student in students])

student_averages = exams.mean(axis=1)
homework_scores = homework / 10 * 100
final_scores = 0.7 * student_averages + 0.3 * homework_scores

print(f"Exam scores:\n{exams}")
print(f"\nStudent averages: {np.round(student_averages, 2)}")
print(f"Final scores: {np.round(final_scores, 2)}")

print("\nExam statistics:")
print(f"Mean: {np.round(exams.mean(axis=0), 2)}")
print(f"Min: {exams.min(axis=0)}")
print(f"Max: {exams.max(axis=0)}")
print(f"Std: {np.round(exams.std(axis=0), 2)}")

mask = student_averages >= 85
print(f"\nStudents with exam average >= 85: {names[mask]}")

excellent_mask = np.all(exams >= 90, axis=1)
print(f"Excellent students: {names[excellent_mask]}")

print(f"Passing students: {names[final_scores >= 60]}")
print(f"Class average: {final_scores.mean():.2f}")
