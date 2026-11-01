import numpy as np

names = np.array(["Anna", "Peter", "Maria", "John", "Sofia", "David"])

exams = np.array([
    [85, 90, 88],
    [55, 60, 58],
    [95, 92, 98],
    [70, 65, 72],
    [40, 50, 45],
    [88, 91, 86],
])

student_averages = exams.mean(axis=1).round(2)
print("Student averages:")
for name, avg in zip(names, student_averages):
    print(name, avg)

print("Exam averages:", exams.mean(axis=0).round(2))
print("Highest scores:", exams.max(axis=0))
print("Lowest scores:", exams.min(axis=0))

mask = student_averages >= 85
print("Average >= 85:")
for name, avg in zip(names[mask], student_averages[mask]):
    print(name, avg)

# Comparison and reflection - NumPy:
# NumPy stores the scores in a 2D array and calculates averages, maximums and minimums
# for the whole table at once, without writing loops (axis=1 = per student, axis=0 = per
# exam). Boolean masking selects students with one simple condition. It is useful when
# working with lots of numbers, because it is much faster and shorter than plain Python
# loops. Its limitation is that arrays work best with one type of data (here just
# numbers), so names and labels have to be kept in a separate array.
