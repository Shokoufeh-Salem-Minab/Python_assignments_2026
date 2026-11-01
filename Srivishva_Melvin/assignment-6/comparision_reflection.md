Comparision and reflection
1. Procedural: 

The program is a list of steps, and functions work on plain data, the list of dictionaries
    Strengths: simple, easy to read from top to bottom, good for small scripts
    Limits: when the program grows, data and functions are separate, so it gets harder to keep organised and to reuse

2. OOP:

Data and the functions that use it live together in classes (Student has its own scores and methods, Classroom manages many students)
    Strengths: organised, reusable, easy to extend 
    Limits: more code and more setup for a small problem, and objects can hide changing state

3. Functional: 

Small independent functions that never change the original data and are combined with functions like map, filter, reduce and sorted
    Strengths: predictable (same input gives the same output), easy to test, the original dataset is safe
    Limits: can be harder for beginners to read and it is not ideal when you need to keep and change a lot of state

4. NumPy: 

Fast maths on whole arrays of numbers without loops (averages per row or column, statistics, boolean masks). Useful when all data is numeric.

5. Pandas: 

Tables with named columns, built on NumPy. Useful for real-world data like adding columns, filtering, sorting, groupby, and reading and writing files like CSV. Less useful for tiny problems or when data is not tabular.

Conclusion: All three paradigms give the same result. The difference is how the code is organised.
