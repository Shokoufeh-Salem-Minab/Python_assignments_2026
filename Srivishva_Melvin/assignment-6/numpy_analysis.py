# Homework 6 
# Srivishva Melvin Marimouttou, sm25017
# Program created on: 27/10/2026

import numpy as np

names = np.array(["Anna", "Peter", "Maria", "John", "Sofia", "David"])
scores = np.array([
    [85, 90, 88],
    [55, 60, 58],
    [95, 92, 98],
    [70, 65, 72],
    [40, 50, 45],
    [88, 91, 86],
])

student_averages = scores.mean(axis=1) # axis is 1 to keep each values seperate for each students
print("Student averages:")
print(np.round(student_averages, 2))

print("\nExam statistics: ")
print("Mean: ", np.round(scores.mean(axis=0), 2))
print("Min: ", scores.min(axis=0))
print("Max: ", scores.max(axis=0))
print("Std: ", np.round(scores.std(axis=0), 2))
print("Median: ", np.median(scores, axis=0))
print("\nWhole array: mean", round(scores.mean(), 2), ", min", scores.min(), ", max", scores.max())

mask = student_averages >= 85
print("\nMask:", mask)
print("Students with exam average >= 85:", names[mask])
print("Their averages:", np.round(student_averages[mask], 2))
