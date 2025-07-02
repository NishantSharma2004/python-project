def count_vowels_consonants(s):
    vowels = 'aeiouAEIOU'
    count_vowels = 0
    count_consonants = 0

    for char in s:
        if char.isalpha():  # check if the character is a letter
            if char in vowels:
                count_vowels += 1
            else:
                count_consonants += 1

    result = {'vowels': count_vowels, 'consonants': count_consonants}
    return result

# Example usage:
s = input("Enter a string: ")
S = count_vowels_consonants(s)
print(S)
