from game import WordleGame, LetterValidity, DICTIONARY
from player import WordlePlayer
from regex import match
from random import choice

VOWELS = "aeiou"

VOWEL_BOOST_MULT = 1.01
EXISTS_BOOST_MULT = 30

def calculate_repeating_letter_weight(count: int) -> float:
	return -(count - 1) ** 3 / 9

def build_regex_pattern(word: str, word_validity: list[LetterValidity]) -> str:
	incorrect = ""
	correct: dict[int, str] = {}
	exists: dict[int, list[str]] = {}

	for index, info in enumerate(zip(word, word_validity)):
		char, validity = info

		if validity == LetterValidity.Correct:
			correct[index] = char
		elif validity == LetterValidity.Exists or validity == LetterValidity.OnlyOne:
			chars = exists.get(index, [])

			if char not in chars:
				chars.append(char)

			exists[index] = chars

		elif validity == LetterValidity.Incorrect and char not in incorrect:
			incorrect += char
	
	pattern = ""

	for index in range(len(word)):
		correct_char = correct.get(index)

		if correct_char != None:
			pattern += correct_char
			continue
		
		nobueno = incorrect

		for char in exists.get(index, []):
			nobueno += char
		
		pattern += f"[^{nobueno}]"

	return pattern

def has_letters(word: str, letters: list[str]) -> bool:
	for letter in letters:
		if letter not in word:
			return False
	return True

def extract_letter_frequencies(words_list: list[str], allowed_letters: list[str] = []) -> dict[str, int]:
	letter_frequencies: dict[str, int] = {}

	# TODO: change letter frequency allow list to store also position, might be better???

	for word in words_list:
		for letter in word:
			if letter in allowed_letters:
				letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1

	return letter_frequencies

class WordleGuesser(WordlePlayer):
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.available: list[str] = DICTIONARY
		
		self.unknown_letters: list[str] = [char for char in "abcdefghijklmnopqrstuvwxyz"]
		self.known_letters: dict[int, str] = {}
		self.existing_letters: list[str] = [] # letters that are in the word, but we don't know where
		self.onlyone_letters: list[str] = [] # letters that are in the word only once
	
	def choose_word(self) -> str:
		if len(self.available) == 1:
			return self.available[0]

		words_scores: list[tuple[str, float]] = []

		# determine if remaining words are similar (e.g. worse, horse, morse) and try to find a word with as many possible letters as possible
		if len(self.available) > 2 and len(self.known_letters) >= len(self.game.secret_word) * 0.7:
			search_for = []

			# filter for letters that we should look for in the dictionary
			for word in self.available:
				for letter in self.unknown_letters:
					if letter in word and letter not in search_for:
						search_for.append(letter)
			
			for _, letter in self.known_letters.items():
				if letter not in search_for:
					search_for.append(letter)

			# print(self.known_letters, self.available, search_for)
			print(self.available, search_for)
			for word in DICTIONARY:
				score = 0

				for letter in search_for:
					if letter in word:
						score += 20 if letter not in self.known_letters else 10

				for letter in self.unknown_letters:
					if letter in word:
						score += 0
				
				# for _, letter in self.known_letters.items():
				# 	if letter in word:
				# 		score -= 6

				if score > 0:
					words_scores.append((word, score))
		else:
			letter_frequencies = extract_letter_frequencies(self.available, self.unknown_letters)

			for word in self.available:
				score = 0

				repeating_letters: dict[str, int] = {}

				for letter in word:
					repeat_count = repeating_letters.get(letter, 0) # discount words with repeating letters, as choosing them is probably not a good idea

					if letter in self.onlyone_letters and repeat_count > 1: # disregard words with confirmed repeats, if the repeat can't plausibly exist
						score = -9e9
						break
					
					repeating_letters[letter] = repeat_count + 1
					
					exists_in_word = letter in self.existing_letters
					is_vowel = letter in VOWELS # boost vowels a little bit

					weight_repeating = calculate_repeating_letter_weight(repeat_count)
					weight_exists = EXISTS_BOOST_MULT if exists_in_word else 1
					weight_vowel = VOWEL_BOOST_MULT if is_vowel else 1

					score += letter_frequencies.get(letter, 0) * weight_repeating * weight_exists * weight_vowel

				words_scores.append((word, score))
		
		words_scores.sort(key=lambda info: info[1], reverse=True)

		# print(words_scores)

		return words_scores[0][0]

	def prompt_guess(self):
		if len(self.available) == 0:
			print("UNABLE TO DEDUCE WORD")
			self.available = DICTIONARY

		word, word_validity = self.game.make_guess(self.choose_word())
		pattern = build_regex_pattern(word, word_validity)
		
		for index, letter, validity in zip(range(len(word)), word, word_validity):
			if (validity != LetterValidity.Exists and validity != LetterValidity.OnlyOne) and letter in self.unknown_letters:
				self.unknown_letters.remove(letter)
			if validity == LetterValidity.Exists and letter not in self.existing_letters:
				self.existing_letters.append(letter)
			if validity == LetterValidity.OnlyOne and letter not in self.onlyone_letters:
				self.onlyone_letters.append(letter)
			if validity == LetterValidity.Correct:
				self.known_letters[index] = letter

		self.available = [word for word in self.available if match(pattern, word) != None and has_letters(word, self.existing_letters)]
		
		return (word, word_validity)