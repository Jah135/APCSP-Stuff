from modules.dictionary import DICTIONARY

letters = set(input("Letters (comma sep): ").split(","))

for word in DICTIONARY:
    if not all(letter in word for letter in letters):
        continue
    print(word)
