# oop.py

class Student:
    def calc_recovery( self ):
        fin = self.calcFinalScore()
        if fin < 60:
            rec = fin + 5.0
            if ( rec > 100.0 ):
                rec= 100.0
            return rec
        else:
            return fin

    def is_exc( self ):
        if ( ( self.exam1 >= 90 ) and ( self.exam2 >= 90 ) ):
            if self.exam3 >= 90:
                return True
            else:
                return False
        else:
            return False

    def __init__(self, name, exam1, exam2, exam3, homework):
        self.name = name
        self.exam1= exam1
        self.exam2 =exam2
        self.exam3 = exam3
        self.homework = homework

    def calc_exam_avg(self):
        tot = self.exam1 + self.exam2+self.exam3
        return tot / 3.0

    def calc_hw(self):
        return ( self.homework / 10.0 ) * 100.0

    def calcFinalScore(self):
        e_a = self.calc_exam_avg()
        h_s = self.calc_hw()
        res = 0.7* e_a + 0.3 * h_s
        return res

    def get_status( self ):
        fin = self.calcFinalScore()
        if fin >= 60:
            return 'Pass'
        else:
            return "Fail"


class Classroom:
    def rankStudents(self):
        arr = []
        for i in range( len( self.students ) ):
            arr.append( self.students[ i ] )
        for i in range( len( arr ) ):
            for j in range( 0 , len( arr ) - i - 1 ):
                if arr[ j ].calcFinalScore() < arr[ j + 1 ].calcFinalScore():
                    t = arr[ j ]
                    arr[ j ] = arr[ j + 1 ]
                    arr[ j + 1 ] = t
        return arr

    def get_fail_students( self ):
        res = []
        for i in range( len( self.students ) ):
            st = self.students[ i ]
            if st.get_status() == "Fail":
                res.append( st )
        return res

    def __init__(self):
        self.students = []

    def addStudent( self, st ):
        self.students.append( st )

    def class_avg(self):
        if len( self.students ) == 0:
            return 0.0
        tot = 0.0
        for i in range( len( self.students ) ):
            tot = tot + self.students[ i ].calcFinalScore()
        return tot / len( self.students )

    def get_exc_students(self):
        res = []
        for i in range( len( self.students ) ):
            s = self.students[ i ]
            if s.is_exc() == True:
                res.append( s )
        return res


if __name__ == "__main__":
    raw_data = [
        {"name": "Anna", "exam1": 85, "exam2": 90, "exam3": 88, "homework": 9},
        {"name": "Peter", "exam1": 55, "exam2": 60, "exam3": 58, "homework": 6},
        {"name": "Maria", "exam1": 95, "exam2": 92, "exam3": 98, "homework": 10},
        {"name": "John", "exam1": 70, "exam2": 65, "exam3": 72, "homework": 8},
        {"name": "Sofia", "exam1": 40, "exam2": 50, "exam3": 45, "homework": 5},
        {"name": "David", "exam1": 88, "exam2": 91, "exam3": 86, "homework": 10}
    ]

    c = Classroom()
    for i in range( len( raw_data ) ):
        item = raw_data[ i ]
        s = Student( item[ 'name' ], item[ "exam1" ], item[ 'exam2' ], item[ 'exam3' ], item[ 'homework' ] )
        c.addStudent( s )

    print( "--- OOP Results ---" )
    print( "Class Average: {:.2f}".format( c.class_avg() ) )
    print( "\nRanked Students:" )
    rk = 1
    ranked_list = c.rankStudents()
    for i in range( len( ranked_list ) ):
        st = ranked_list[ i ]
        print( str( rk ) + ". " + st.name + " - Final Score: " + f"{st.calcFinalScore():.2f}" + " (" + st.get_status() + ")" )
        rk = rk + 1

    print( "\nExcellent Students:" )
    exc_list = c.get_exc_students()
    for i in range( len( exc_list ) ):
        print( "- " + exc_list[ i ].name )

    print( "\nFailing Students (with recovery score):" )
    fail_list = c.get_fail_students()
    for i in range( len( fail_list ) ):
        print( "- " + fail_list[ i ].name + " (Recovery: " + f"{fail_list[ i ].calc_recovery():.2f}" + ")" )