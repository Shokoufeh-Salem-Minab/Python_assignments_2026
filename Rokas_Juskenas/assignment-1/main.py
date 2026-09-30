fn=input("Enter first name: ")
ln = input( "Enter last name: " )

# lengths
f_len = len(fn)
l_len=len(ln )

print("fn len:",f_len)
print( "ln len:" , l_len )

# vowels and consonants
vow=0
cons= 0
for c in fn.lower():
    if c in ['a','e' ,'i','o','u']:
        vow= vow +1
    elif c.isalpha( ):
        cons +=1

print("vowels:",vow)
print( "consonants:" ,cons)

# upper lower
print( "UPPER:" , fn.upper() )
print("lower:",fn.lower( ))

# rev name
rev_ln=""
for x in ln:
    rev_ln = x+rev_ln
print("last name reversed:", rev_ln )

# loops practice
print( "for loop chars:" )
for char in fn:
    print( char)

print("while loop chars:")
temp=fn
while len( temp )>0:
    print(temp[ 0 ])
    temp =temp[1: ]

# compare names
if f_len> l_len:
    print("fn is longer than ln")
elif f_len <l_len:
    print( "fn is shorter than ln" )
else:
    print("names are equal length")

# pass gen
pwd = fn[0]+ ln[-1] + str( f_len + l_len)
print( "Password:" ,pwd)

# list practice
lst =[]
for letter in ln:
    lst.append( letter)

lst.append( "*" )
lst.insert(0,"@")
lst.remove( ln[ 0] )
lst.reverse( )

print( lst )