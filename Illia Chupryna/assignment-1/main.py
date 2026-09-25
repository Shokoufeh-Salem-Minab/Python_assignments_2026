firstName = input("Enter your first name: ")
lastName = input("Enter your last name: ")

firstName_len = len(firstName)
lastName_len = len(lastName)

print('Length of the first name: ' + str(firstName_len))
print('Length of the last name: ' + str(lastName_len))

vowels = ["a", "e", "i", "o", "u"]

vowelsCount = consonantsCount = 0

for l in firstName:
    if l.lower() in vowels:
        vowelsCount += 1
    else:
        consonantsCount += 1
        
print('Vowels in first name: ' + str(vowelsCount))
print('Consonants in first name: ' + str(consonantsCount))

print('First name (upper): ' + str(firstName.upper()))
print('First name (lower): ' + str(firstName.lower()))

print('Last name (reversed): ' + str(lastName[::-1]))

print('Characters in first name (for loop):')
for c in firstName:
    print(c)

print('Characters in first name (while loop):')
firstNameCopy = firstName
while len(firstNameCopy) > 0:
    print(firstNameCopy[0])
    firstNameCopy = firstNameCopy[1:]
    
if (firstName_len > lastName_len):
    print('Comparison result: First name is longer than last name')
elif (firstName_len == lastName_len):
    print('Comparison result: First name has an equal amount of letters as the last name')
else:
    print('Comparison result: First name is shorter than first name')

password = firstName[0] + lastName[0] + str(firstName_len + lastName_len)
print('Generated password: ' + password)

lastNameCharacters = []
for c in lastName:
    lastNameCharacters.append(c)
    
lastNameCharacters.append("*")
lastNameCharacters.insert(0, "@")
lastNameCharacters.pop(1)
lastNameCharacters.reverse()

print(lastNameCharacters)