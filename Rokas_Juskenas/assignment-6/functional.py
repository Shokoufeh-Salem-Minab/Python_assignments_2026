# functional.py
from functools import reduce

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

calc_exam_avg = lambda s: ( s[ 'exam1' ] + s[ "exam2" ] + s[ 'exam3' ] ) / 3.0
calcHwScore = lambda s: ( s[ "homework" ] / 10.0 ) * 100.0
calc_final_sc = lambda s: 0.7 * calc_exam_avg( s ) + 0.3 * calcHwScore( s )
check_status = lambda score: "Pass" if ( score >= 60 ) else 'Fail'
is_exc = lambda s: True if ( ( s[ 'exam1' ] >= 90 ) and ( s[ 'exam2' ] >= 90 ) and ( s[ 'exam3' ] >= 90 ) ) else False
calcRec = lambda score: ( score + 5.0 if ( score + 5.0 <= 100.0 ) else 100.0 ) if ( score < 60 ) else score

def enrich_student( student ):
    fin = calc_final_sc( student )
    d = {}
    d[ 'name' ] = student[ 'name' ]
    d[ 'exam1' ] = student[ 'exam1' ]
    d[ 'exam2' ] = student[ 'exam2' ]
    d[ 'exam3' ] = student[ 'exam3' ]
    d[ 'homework' ] = student[ 'homework' ]
    d[ 'exam_avg' ] = calc_exam_avg( student )
    d[ 'hw_score' ] = calcHwScore( student )
    d[ 'final_score' ] = fin
    d[ "status" ] = check_status( fin )
    d[ 'is_excellent' ] = is_exc( student )
    d[ 'recovery_score' ] = calcRec( fin )
    return d

proc_st = list( map( enrich_student , students ) )

exc_st = list( filter( lambda s: s[ 'is_excellent' ] == True , proc_st ) )

fail_st = list( filter( lambda s: s[ 'status' ] == "Fail" , proc_st ) )

tot_sc = reduce( lambda acc , s: acc + s[ "final_score" ] , proc_st , 0.0 )

if len( proc_st ) > 0:
    c_avg = tot_sc / len( proc_st )
else:
    c_avg = 0.0

rnk_st = sorted( proc_st , key=lambda s: s[ 'final_score' ] , reverse=True )

if __name__ == '__main__':
    print( "--- Functional Programming Results ---" )
    print( f"Class Average Score: {c_avg:.2f}" )
    
    exc_names = []
    for i in range( len( exc_st ) ):
        exc_names.append( exc_st[ i ][ 'name' ] )
    print( "Excellent Students:" , exc_names )

    fail_names = []
    for i in range( len( fail_st ) ):
        fail_names.append( fail_st[ i ][ 'name' ] )
    print( "Failing Students:" , fail_names )

    print( "\nRankings:" )
    rk = 1
    for i in range( len( rnk_st ) ):
        st = rnk_st[ i ]
        print( str( rk ) + ". " + st[ 'name' ] + ": " + "%.2f" % st[ 'final_score' ] )
        rk = rk + 1