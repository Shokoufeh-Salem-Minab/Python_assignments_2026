# Task 4: NumPy
# exam scores go into a 2D array: every row is a student, every column is an exam.
# after that i dont use any loops, only numpy functions.

import numpy as np

# the dataset from the homework
students = [
    {"name": "Anna",  "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John",  "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10},
]


def check_students(data):
    # small safety check so the programs stop with a clear message
    # if the data is broken (empty list, missing key, score out of range)
    if len(data) == 0:
        raise ValueError("the student list is empty")

    for s in data:
        for key in ["name", "exam1", "exam2", "exam3", "homework"]:
            if key not in s:
                raise ValueError(f"student {s} is missing the key '{key}'")

        for key in ["exam1", "exam2", "exam3", "homework"]:
            value = s[key]
            # bool is also a number in python so i block it separately
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{s['name']}: {key} must be a number")

        for key in ["exam1", "exam2", "exam3"]:
            if s[key] < 0 or s[key] > 100:
                raise ValueError(f"{s['name']}: {key} must be between 0 and 100")

        # homework is how many of the 10 assignments were submitted
        if s["homework"] < 0 or s["homework"] > 10:
            raise ValueError(f"{s['name']}: homework must be between 0 and 10")


check_students(students)

# only this part reads the dictionaries, the calculations below are loop free
names = np.array([s["name"] for s in students])
exams = np.array([[s["exam1"], s["exam2"], s["exam3"]] for s in students])

# axis=1 means "along the row", so one average for each student
student_avg = exams.mean(axis=1)

print("--- NumPy ---")
print("Exam scores (rows = students, columns = exams):")
print(exams)

print("\nStudent averages:", np.round(student_avg, 2))

# axis=0 means "down the column", so one number for each exam
print("\nStatistics for exam1, exam2, exam3:")
print("Mean:  ", np.round(exams.mean(axis=0), 2))
print("Median:", np.median(exams, axis=0))
print("Std:   ", np.round(exams.std(axis=0), 2))
print("Min:   ", exams.min(axis=0))
print("Max:   ", exams.max(axis=0))

# Boolean mask: True where the exam average is 85 or more
mask = student_avg >= 85
print("\nMask:", mask)
print("Students with exam average >= 85:", names[mask])
print("Their averages:", np.round(student_avg[mask], 2))
