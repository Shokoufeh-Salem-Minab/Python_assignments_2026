# 1. Ask for input, Tested with "Eren" as first name and "Ustun" for last
first_name = input("Enter your first name: ").strip()
last_name = input("Enter your last name: ").strip()

print("STRING ANALYSIS")
# Print the length of the first and last name
len_first = len(first_name)
len_last = len(last_name)
print(f"Length of first name: {len_first}")
print(f"Length of last name: {len_last}")

# Count vowels and consonants in first name
vowels = "aeiou"
vowel_count = 0
consonant_count = 0

for char in first_name.lower():
    if char.isalpha():
        if char in vowels:
            vowel_count += 1
        else:
            consonant_count += 1

print(f"Vowels in first name: {vowel_count}")
print(f"Consonants in first name: {consonant_count}")

# Print first name in uppercase and lowercase
print(f"Uppercase: {first_name.upper()}")
print(f"Lowercase: {first_name.lower()}")

# Print the last name reversed
print(f"Reversed last name: {last_name[::-1]}")
print("LOOP PRACTICE")

# For loop: print each character of the first name
print("Printing each character using a for loop:")
for char in first_name:
    print(char)

# While loop: print and remove characters until nothing is left
print("\nRemoving characters using a while loop:")
temp_first = first_name
while len(temp_first) > 0:
    print(f"Current string: {temp_first}")
    temp_first = temp_first[:-1]  # Removes the last character each iteration
print(f"Final state: '{temp_first}' (empty)")
print("CONDITIONS (IF / ELIF / ELSE)")


# Compare lengths
if len_first > len_last:
    print("Your first name is longer than your last name.")
elif len_first < len_last:
    print("Your first name is shorter than your last name.")
else:
    print("Your first name and last name have the exact same length.")

print("PERSONAL PASSWORD GENERATOR")


# Password: first letter of first name + last letter of last name + total length
if first_name and last_name:
    first_letter = first_name[0]
    last_letter = last_name[-1]
    total_length = len_first + len_last
    password = f"{first_letter}{last_letter}{total_length}"
    print(f"Generated Password: {password}")
else:
    print("Cannot generate password with empty names.")

print("LIST METHODS PRACTICE")


# Create a list containing each character of the last name
last_name_list = list(last_name)
print(f"Original list: {last_name_list}")

# Use .append() to add "*" to the end
last_name_list.append("*")
print(f"After append('*'): {last_name_list}")

# Use .insert() to add "@" at the beginning
last_name_list.insert(0, "@")
print(f"After insert(0, '@'): {last_name_list}")

# Use .pop() to delete one character (removes the second element if available)
if len(last_name_list) > 1:
    removed_item = last_name_list.pop(1)
    print(f"After removing '{removed_item}': {last_name_list}")

# Use .reverse() to reverse the list
last_name_list.reverse()
print(f"After reverse(): {last_name_list}")