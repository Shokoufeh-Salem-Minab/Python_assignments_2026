# pandas_analysis.py
import numpy as np
import pandas as pd

stData = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

df = pd.DataFrame( stData )

df[ 'exam_average' ] = df[ [ "exam1" , 'exam2' , "exam3" ] ].mean( axis = 1 )
df[ "homework_score" ] = ( df[ 'homework' ] / 10.0 ) * 100.0
df[ 'final_score' ] = 0.7 * df[ 'exam_average' ] + 0.3 * df[ "homework_score" ]

df[ "status" ] = np.where( df[ 'final_score' ] >= 60 , "Pass" , 'Fail' )

df[ 'is_excellent' ] = ( ( df[ "exam1" ] >= 90 ) & ( df[ 'exam2' ] >= 90 ) & ( df[ 'exam3' ] >= 90 ) )

df[ 'recovery_score' ] = np.where( df[ 'final_score' ] < 60 , np.minimum( 100.0 , df[ 'final_score' ] + 5.0 ) , df[ 'final_score' ] )

filtered_df = df[ df[ "exam_average" ] >= 85 ]

sortedDf = df.sort_values( by = 'final_score' , ascending = False ).reset_index( drop = True )

stat_counts = df[ 'status' ].value_counts()

grpBySummary = df.groupby( 'status' )[ [ "exam_average" , 'homework_score' , "final_score" ] ].mean()

sortedDf.to_csv( "student_report.csv" , index = False )

if __name__ == "__main__":
    print( "--- Pandas Full DataFrame ---" )
    print( sortedDf.to_string() )
    print( "\n--- Filtered Students (Exam Average >= 85) ---" )
    print( filtered_df[ [ "name" , "exam_average" , "final_score" ] ].to_string() )
    print( "\n--- Status Value Counts ---" )
    print( stat_counts )
    print( "\n--- Groupby Summary (Means by Status) ---" )
    print( grpBySummary )
    print( "\nExported " + "student_report.csv" + " successfully." )

# COMPARISON AND REFLECTION
#
# 1. PROGRAMMING PARADIGM COMPARISON
#
# Procedural programming:
# * Difference: The program is a sequence of steps and functions that work on shared, changeable data (mutable state).
# * Strengths: Simple to write and intuitive for short tasks.
# * Limitations: Changing state can cause bugs, and the code is difficult to scale.
#
# Object-oriented programming (OOP):
# * Difference: Data and methods are bundled together in objects (here the Student and Classroom classes).
# * Strengths: Reusable and modular, and it models real-world things in a clear way.
# * Limitations: Needs extra boilerplate code even for simple tasks.
#
# Functional programming (FP):
# * Difference: Uses pure functions such as map(), filter() and reduce() on data that is not modified.
# * Strengths: No side effects, predictable behaviour, and easy to test.
# * Limitations: Creating new data instead of changing it can use more memory, and it has a steeper learning curve.
#
# All three versions gave the same results (for example a class average of 75.64), so the choice
# between them is about structure and style, not correctness.
#
# 2. WHEN NUMPY AND PANDAS ARE USEFUL
#
# NumPy is the best choice for fast numerical work: vectorized operations on multi-dimensional arrays,
# statistics and matrix calculations without writing loops. In this project it was used for the exam score
# statistics and the Boolean mask selection.
# Pandas is best for tabular data: filtering, sorting, grouping (groupby), counting values (value_counts),
# handling missing data and reading or exporting files such as CSV. In this project it was used to build the
# full student report and export student_report.csv.