from game import WordleGame, LetterValidity, DICTIONARY
from player import WordlePlayer
from regex import match
from random import choice

VOWELS = "aeiou"

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

def get_game_filtered_words(words_list: list[str], word: str, word_validity: list[LetterValidity]):
	pattern = build_regex_pattern(word, word_validity)

	return [word for word in words_list if match(pattern, word)]

class WordleGuesser(WordlePlayer):
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.available = DICTIONARY
		
		self.unknown_letters = [char for char in "abcdefghijklmnopqrstuvwxyz"]
		self.existing_letters = [] # letters that are in the word, but we don't know where
		self.onlyone_letters = [] # letters that are in the word only once
	
	def choose_word(self) -> str:
		letter_frequencies: dict[str, int] = {}

		for word in self.available:
			for letter in word:
				if letter in self.unknown_letters:
					letter_frequencies[letter] = letter_frequencies.get(letter, 0) + 1
		
		# frequencies_list = [(key, frequency) for key, frequency in letter_frequencies.items()]
		# frequencies_list.sort(key=lambda info: info[1], reverse=True)

		words_scores: list[tuple[str, float]] = []

		for word in self.available:
			word_score = 0

			repeating_letters: dict[str, int] = {}

			for letter in word:
				repeat_count = repeating_letters.get(letter, 0) # discount words with repeating letters, as choosing them is probably not a good idea

				if letter in self.onlyone_letters and repeat_count > 1: # disregard words with confirmed repeats, if the repeat can't plausibly exist
					word_score = -9e9
					break

				repeating_letters[letter] = repeat_count + 1
				
				exists_in_word = letter in self.existing_letters
				is_vowel = letter in VOWELS # boost vowels a little bit

				repeating_discount = 1 / (repeat_count + 1) ** 2
				exist_boost = 20 if exists_in_word else 1
				vowel_boost = 1.1 if is_vowel else 1

				word_score += letter_frequencies.get(letter, 0) * repeating_discount * exist_boost * vowel_boost

			words_scores.append((word, word_score))
		words_scores.sort(key=lambda info: info[1], reverse=True)

		print(words_scores, letter_frequencies)

		return words_scores[0][0] #choice(self.available)

	def prompt_guess(self):
		word, word_validity = self.game.make_guess(self.choose_word())
		
		old_available = self.available
		new_available = get_game_filtered_words(old_available, word, word_validity)

		for letter, validity in zip(word, word_validity):
			if (validity != LetterValidity.Exists and validity != LetterValidity.OnlyOne) and letter in self.unknown_letters:
				self.unknown_letters.remove(letter)
			if validity == LetterValidity.Exists and letter not in self.existing_letters:
				self.existing_letters.append(letter)
			if validity == LetterValidity.OnlyOne and letter not in self.onlyone_letters:
				self.onlyone_letters.append(letter)

		# initial_count = len(old_available)
		# current_count = len(new_available)
		# percentage = 1 - (current_count / initial_count)

		# print(f"initial #: {initial_count}")
		# print(f"current #: {current_count}")
		# print(f"reduction: {percentage*100:.2f}% ({current_count - initial_count})")
		# print(f"guessed word: {word}")
		# print(f"feedback: {info[1]}")
		# print(f"pattern: {pattern}")

		self.available = new_available
		
		return (word, word_validity)