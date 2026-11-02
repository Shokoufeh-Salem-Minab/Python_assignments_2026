import numpy as np

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

names = np.array([s["name"] for s in students])
exams = np.array([[s["exam1"], s["exam2"], s["exam3"]] for s in students])

student_avgs = np.mean(exams, axis=1)
exam_means = np.mean(exams, axis=0)
exam_max = np.max(exams, axis=0)
exam_min = np.min(exams, axis=0)

mask = student_avgs >= 85
top_students = names[mask]

print("Student Exam Averages:", np.round(student_avgs, 2))
print("Exam Means:", np.round(exam_means, 2), "Max:", exam_max, "Min:", exam_min)
print("Students with Exam Avg >= 85:", top_students)

# --- Task 6: When NumPy is Useful ---
# NumPy is useful when working with numerical data and multi-dimensional arrays (matrices). 
# It allows fast, vectorized mathematical and statistical operations (like mean, min, max, and Boolean masking) 
# across rows and columns simultaneously without needing slow Python loops.