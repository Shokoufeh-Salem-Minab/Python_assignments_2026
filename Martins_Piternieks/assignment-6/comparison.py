# ===== COMPARISON AND REFLECTION =====
#
# ----- Procedural Programming (procedural.py) -----
# The program is a list of steps: functions, loops and if-conditions that run
# from top to bottom.
# + Strengths: easy to read and write, good for small scripts.
# - Limitations: data and functions are separate, so in a big program it is
#   hard to keep track of who changes what.
#
# ----- Object-Oriented Programming (oop.py) -----
# Data and the methods that use it are grouped together in classes
# (Student knows its own scores, Classroom manages the students).
# + Strengths: code is organized and reusable, easy to extend
#   (for example with inheritance), models real things well.
# - Limitations: more code to write, too much structure for a small task.
#
# ----- Functional Programming (functional.py) -----
# The program is built from small pure functions that return new values and
# never change the original data. map(), filter(), reduce() and sorted()
# replace most loops.
# + Strengths: no side effects, so functions are easy to test and to combine.
# - Limitations: long chains of map/filter/lambda can be harder to read for
#   beginners, and creating new copies of data uses more memory.
#
# ----- Main difference -----
# All three give the same results. Procedural focuses on STEPS, OOP on OBJECTS,
# and functional on FUNCTIONS that transform data.
#
# ----- When are NumPy and Pandas useful? -----
# NumPy: fast math on numbers stored in arrays (averages, statistics, masks)
# without writing loops. Best for large numeric data.
# Pandas: works with tables (rows and columns with names). Best for filtering,
# sorting, grouping and saving data to files like CSV.
