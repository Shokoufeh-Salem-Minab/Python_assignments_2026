# numpy_analysis.py
import numpy as np

stNames = np.array( [ "Anna" , 'Peter' , "Maria" , 'John' , "Sofia" , 'David' ] )

exScores = np.array([
    [ 85 , 90 , 88 ],
    [55, 60, 58],
    [95,92,98],
    [ 70, 65, 72 ],
    [40, 50, 45],
    [ 88 , 91 , 86 ]
])

st_avg = np.mean( exScores , axis= 1 )

overallMean = np.mean( exScores )
ov_std = np.std( exScores )
ov_min = np.min( exScores )
ov_max = np.max( exScores )

examMeans = np.mean( exScores , axis =0 )

mask = ( st_avg >= 85 ) == True
high_perf_n = stNames[ mask ]
high_perf_a = st_avg[ mask ]

if __name__ == "__main__":
    print( "--- NumPy Analysis Results ---" )
    print( "Student Exam Averages:" , np.round( st_avg , 2 ) )
    print( "Overall Mean: %.2f" % overallMean )
    print( "Overall Std Dev: " + str( round( ov_std , 2 ) ) )
    print( "Overall Min: " + str( ov_min ) + ", Max: " + f"{ov_max}" )
    print( "Exam-by-Exam Averages (Exams 1-3):" , np.round( examMeans , 2 ) )
    print( "\nBoolean Mask Selection (Exam Average >= 85):" )
    for i in range( len( high_perf_n ) ):
        name = high_perf_n[ i ]
        avg = high_perf_a[ i ]
        print( "- {}: {:.2f}".format( name , avg ) )