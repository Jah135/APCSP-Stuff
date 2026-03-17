with open("dictionary.txt", "r") as f:
	DICTIONARY = [x.strip() for x in f.readlines()]