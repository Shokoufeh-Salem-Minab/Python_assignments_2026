import numpy as np

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

scores_matrix = np.array([[s["exam1"], s["exam2"], s["exam3"]] for s in students])
np_student_averages = np.mean(scores_matrix, axis=1)
np_exam_means = np.mean(scores_matrix, axis=0)
np_exam_max = np.max(scores_matrix, axis=0)
np_exam_min = np.min(scores_matrix, axis=0)

np_mask = np_student_averages >= 85
student_names = np.array([s["name"] for s in students])
np_high_achievers = student_names[np_mask]
