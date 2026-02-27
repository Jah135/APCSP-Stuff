target_length = int(input("target word length: ")) + 1

with open("big_dictionary.txt", "r") as f:
    processed = [word for word in f.readlines() if len(word) == target_length]

with open("dictionary.txt", "w") as f:
    f.writelines(processed)