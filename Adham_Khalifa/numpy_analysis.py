import numpy as np

names = np.array(["Anna","Peter","Maria","John","Sofia","David"])
exams = np.array([
    [85,90,88], [55,60,58], [95,92,98],
    [70,65,72], [40,50,45], [88,91,86]
])

averages = np.mean(exams, axis=1)
print("Exam averages:", averages)
print("Overall exam average:", np.mean(exams))
print("Highest exam score:", np.max(exams))
print("Lowest exam score:", np.min(exams))
print("Standard deviation:", np.std(exams))

mask = averages >= 85
print("Students with exam average >= 85:", names[mask])
