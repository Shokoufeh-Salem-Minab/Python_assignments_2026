first_name = input('Enter your first name: ')
while not first_name:
    first_name = input('The name is empty, please enter your first name: ')

last_name = input('Enter your last name: ')
while not last_name:
    last_name = input('The name is empty, please enter your last name: ')

print('Length of first name:',len(first_name))
print('Length of last name:',len(last_name))

vowels = 0
for char in first_name:
    if char.lower() in 'aeiou':
        vowels += 1
print('Vowels in first name:', vowels)

consonants = 0
for char in first_name:
    if char.lower() in 'bcdfghjklmnpqrstvwxyz':
        consonants += 1
print('Consonants in first name:', consonants)

print('First name (upper):', first_name.upper())
print('First name (lower):', first_name.lower())
print('Last name (reversed):', last_name[::-1])

print('Characters in first name (for loop):')
for char in first_name:
    print(char)

print('Characters in first name (while loop):')
temp = first_name
while len(temp) != 0:
    print(temp[0])
    temp = temp[1:]

if len(first_name)>len(last_name):
    print('Comparison result: First name is longer than last name.')
elif len(last_name)>len(first_name):
    print('Comparison result: Last name is longer than first name.')
else: 
    print('Comparison result: First name and last name have the same length.')

pswd = first_name[0]+last_name[-1]+str(len(first_name+last_name))
print('Generated password:', pswd)

name_list = list(last_name)
name_list.append('*')
name_list.insert(0,'@')
name_list.pop(1)
name_list.reverse()
print(name_list)


