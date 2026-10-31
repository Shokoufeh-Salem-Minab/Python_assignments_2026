students = [{'name': 'Anna', 'exam1': 85, 'exam2': 90, 'exam3': 88, 'homework': 9}, {'name': 'Peter', 'exam1': 55, 'exam2': 60, 'exam3': 58, 'homework': 6}, {'name': 'Maria', 'exam1': 95, 'exam2': 92, 'exam3': 98, 'homework': 10}, {'name': 'John', 'exam1': 70, 'exam2': 65, 'exam3': 72, 'homework': 8}, {'name': 'Sofia', 'exam1': 40, 'exam2': 50, 'exam3': 45, 'homework': 5}, {'name': 'David', 'exam1': 88, 'exam2': 91, 'exam3': 86, 'homework': 10}]

import numpy as np

exams = np.array([[s["exam1"], s["exam2"], s["exam3"]] for s in students])
averages = exams.mean(axis=1)
print("Student exam averages:", np.round(averages, 2))
print("Exam averages:", np.round(exams.mean(axis=0), 2))
print("Exam minimums:", exams.min(axis=0))
print("Exam maximums:", exams.max(axis=0))
print("Overall average:", round(float(exams.mean()), 2))
print("Students with exam average at least 85:")
print([students[i]["name"] for i in np.where(averages >= 85)[0]])
