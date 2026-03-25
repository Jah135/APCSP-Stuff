ALPHABET = "abcdefghijklmnopqrstuvwxyz"
VOWELS = "aeiou"
CONSONANTS = "".join([l for l in ALPHABET if l not in VOWELS])

TARGET_LENGTH = int(input("target word length: ")) + 1


def word_filter(word: str):
    if len(word) != TARGET_LENGTH:
        return False
    # if word[-2] == "s" and (word[-3] in CONSONANTS or word[-3] == "e"):
    #     return False
    return True


with open("data/scrabble_dictionary.txt", "r") as f:
    processed = [word.casefold() for word in f.readlines() if word_filter(word)]

with open("dictionary.txt", "w") as f:
    f.writelines(processed)
