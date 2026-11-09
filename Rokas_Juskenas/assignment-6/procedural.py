# procedural.py

students = [
    {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
    {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
    {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
    {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
    {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
    {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
]

def get_exam_avg( st ):
    tot = 0
    tot = tot + st[ 'exam1' ]
    tot=tot+st['exam2']
    tot = tot + st["exam3"]
    return tot / 3.0

def calc_hw(st):
    res=(st[ "homework" ]/10.0)* 100.0
    return res

def calc_final(st):
    e_a=get_exam_avg(st)
    h_s = calc_hw( st )
    fin = 0.7* e_a + 0.3 *h_s
    return fin

def checkStatus( fin_sc ):
    if fin_sc >= 60:
        return 'Pass'
    else:
        return "Fail"

def check_is_excellent(st):
    if st[ 'exam1' ] >= 90:
        if st[ "exam2" ] >= 90:
            if st[ 'exam3' ] >= 90:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def calc_recovery( fin_sc ):
    if fin_sc < 60:
        rec = fin_sc + 5.0
        if rec > 100.0:
            rec=100.0
        return rec
    else:
        return fin_sc

def process_all_students( data ):
    processed = []
    for i in range( len( data ) ):
        s = data[ i ]
        e_a = get_exam_avg( s )
        h_s = calc_hw( s )
        fin = calc_final( s )
        st_val = checkStatus( fin )
        exc = check_is_excellent( s )
        rec = calc_recovery( fin )

        d = {}
        d[ 'name' ] = s[ 'name' ]
        d[ "exam_avg" ] = round( e_a , 2 )
        d[ 'hw_score' ] = round( h_s , 2 )
        d[ 'final_score' ] = round( fin , 2 )
        d[ 'status' ] = st_val
        d[ 'excellent' ] = exc
        d[ 'recovery_score' ] = round( rec , 2 )
        processed.append( d )
    return processed

def classAvg( proc_data ):
    if len( proc_data ) == 0:
        return 0.0
    tot_score = 0.0
    for i in range( len( proc_data ) ):
        item = proc_data[ i ]
        tot_score = tot_score + item[ "final_score" ]
    return tot_score / len( proc_data )

def rank_students( proc_data ):
    arr = proc_data.copy()
    for i in range( len( arr ) ):
        for j in range( 0, len( arr ) - i - 1 ):
            if arr[ j ][ 'final_score' ] < arr[ j + 1 ][ 'final_score' ]:
                temp = arr[ j ]
                arr[ j ] = arr[ j + 1 ]
                arr[ j + 1 ] = temp
    return arr

if __name__ == "__main__":
    res = process_all_students( students )
    ranked = rank_students( res )
    c_avg = classAvg( res )

    print( "--- Procedural Results ---" )
    print( "Class Average Final Score: " + str( round( c_avg, 2 ) ) )
    print( "\nStudent Rankings:" )
    rk = 1
    for i in range( len( ranked ) ):
        s = ranked[ i ]
        print( "%d. %s | Final Score: %s | Status: %s | Excellent: %s | Recovery: %s" % ( rk, s[ 'name' ], str( s[ 'final_score' ] ), s[ 'status' ], str( s[ 'excellent' ] ), str( s[ 'recovery_score' ] ) ) )
        rk = rk + 1