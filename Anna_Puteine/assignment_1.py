# Anna Puteine ap24096

name = input("Enter your first name: ")
surname = input("Enter your last name: ")

name_len = len(name)
surname_len = len(surname)

print(f'Length of first name: {name_len}')
print(f'Length of last name: {surname_len}')

vowels = ['a', 'e', 'i', 'o', 'u']

vow_cnt = 0
cons_cnt = name_len

for a in name:
    if a in vowels:
        vow_cnt += 1
        cons_cnt -= 1

print(f'Vowels in first name: {vow_cnt}')
print(f'Consonants in first name: {cons_cnt}')

print(f'First name (upper): {name.upper()}')
print(f'First name (lower): {name.lower()}')
print(f'Last name (reversed): {surname[::-1]}')

print('Characters in first name (for loop):')
for a in name:
    print(a)

print('Characters in first name (while loop):')
name_copy = name
while len(name_copy) > 0:
    print(name_copy[0])
    name_copy = name_copy[1:]

if name_len == surname_len:
    print('Comparison result: First name and last name have equal length.')
elif name_len > surname_len:
    print('Comparison result: First name is longer than last name.')
else:
    print('Comparison result: First name is shorter than last name.')

print(f'Generated password: {name[0]}{surname[-1]}{name_len + surname_len}')

surname = list(surname)

surname.append('*')
surname.insert(0, '@')
surname.pop(1)
surname.reverse()
print(surname)
