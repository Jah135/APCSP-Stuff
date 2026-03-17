from modules.player import WordlePlayer
from game import WordleGame, LetterValidity, DICTIONARY

def analyze_letter_frequencies(word_list: list[str], allowed_letters: list[str]) -> tuple[dict[str, int], list[dict[str, int]]]:
	frequencies: dict[str, int] = {letter:sum(word.count(letter) for word in word_list) for letter in allowed_letters}
	frequencies_per_position: list[dict[str, int]] = [{letter:sum(1 for word in word_list if word[index] == letter) for letter in allowed_letters} for index in range(max(len(word) for word in word_list))]

	return (frequencies, frequencies_per_position)


IGP_UNKNOWN_LETTER_MULT = 1.1
IGP_POSITIONAL_FREQUENCY_WEIGHT = 10
IGP_GENERAL_FREQUENCY_WEIGHT = 1

DUPLICATE_PENALTY_FALLOFF = 10
KNOWN_PENALTY = -5

CONFIDENCE_FALLOFF = 0.9
CONFIDENCE_THRESHOLD = 0.72
CONFIDENCE_GROWTH_RATE = 1.2

class WordleGuesser(WordlePlayer):
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.reset()

	def reset(self):
		self.available: list[str] = DICTIONARY
		self.unknown_letters: list[str] = [char for char in "abcdefghijklmnopqrstuvwxyz"]
		self.known_letters: list[str] = []
		self.existing_letters: list[str] = []
		self.invalid_letters: list[str] = []

	def determine_word(self) -> str:
		if len(self.available) == 1:
			return self.available[0]
		
		scored_words: list[tuple[str, float]] = []
		frequencies, frequencies_per_position = analyze_letter_frequencies(self.available, self.unknown_letters)

		game = self.game
		
		# confidence grows over the span of a game to force it to make guesses instead of getting greedy with information
		confidence = CONFIDENCE_FALLOFF ** len(self.available) + (len(game.guesses) / game.max_guesses) ** CONFIDENCE_GROWTH_RATE
		# print(f"C:{confidence}\nA:{self.available}\nU:{self.unknown_letters}\nUF:{frequencies}")

		# if we're fairly confident about the word then we can attempt to guess it
		# otherwise try to gather more information
		if confidence >= CONFIDENCE_THRESHOLD:
			# TODO: not entirely sure what to do here for choosing the target word
			for word in self.available:
				score = 0

				for letter in word:
					frequency = frequencies.get(letter, 0)
					score += frequency
				
				scored_words.append((word, score))
		else:
			# information gathering
			for word in DICTIONARY:
				if any(letter in word for letter in self.invalid_letters):
					continue

				score = 0

				duplicate_letters: dict[str, int] = {}
				for index, letter in enumerate(word):
					frequency = frequencies.get(letter, 0)
					positional_frequency = frequencies_per_position[index].get(letter, 0)

					occurances = duplicate_letters.get(letter, 0)

					duplicate_letters[letter] = occurances + 1

					duplicate_penalty = DUPLICATE_PENALTY_FALLOFF ** -occurances
					known_penalty = KNOWN_PENALTY if letter in self.known_letters else 0

					score += (frequency * IGP_GENERAL_FREQUENCY_WEIGHT + positional_frequency * IGP_UNKNOWN_LETTER_MULT) * duplicate_penalty + known_penalty
				
				for letter in self.unknown_letters:
					if letter in word:
						score *= IGP_UNKNOWN_LETTER_MULT

				scored_words.append((word, score))

		scored_words.sort(key=lambda x: x[1], reverse=True)

		# print(scored_words)

		return scored_words[0][0]
	
	def make_guess(self):
		guessed_word, word_validity = self.game.make_guess(self.determine_word())

		letter_counts: dict[str, int] = {}
		letter_limits: dict[str, int] = {}

		correct_letters: dict[int, str] = {}
		exists_not_in_position: dict[int, str] = {}
		
		for index, (letter, validity) in enumerate(zip(guessed_word, word_validity)):
			if letter in self.unknown_letters:
				self.unknown_letters.remove(letter)
				self.known_letters.append(letter)
			
			if validity == LetterValidity.Correct or validity == LetterValidity.Exists:
				letter_counts[letter] = letter_counts.get(letter, 0) + 1
			
			if validity == LetterValidity.Incorrect and letter not in self.invalid_letters:
				self.invalid_letters.append(letter)

			if validity == LetterValidity.Exists:
				exists_not_in_position[index] = letter
				if letter not in self.existing_letters:
					self.existing_letters.append(letter)

			if validity == LetterValidity.Correct:
				correct_letters[index] = letter

			if validity == LetterValidity.TooMany:
				letter_limits[letter] = letter_limits.get(letter, guessed_word.count(letter)) - 1

		new_available = []

		# word filtering
		for word in self.available:
			# remove words that contain any invalid letters
			if any((letter in word) for letter in self.invalid_letters):
				continue
			# remove words that don't have the correct letters
			if any((word[index] != letter) for index, letter in correct_letters.items()):
				continue
			# remove words that have letters in the wrong position
			if any((word[index] == letter) for index, letter in exists_not_in_position.items()):
				continue
			# remove words that don't have letters that exist
			if any((letter not in word) for letter in self.existing_letters):
				continue
			# remove words that have too many letters
			if any((word.count(letter) > count) for letter, count in letter_limits.items()):
				continue
			# remove words that have too little letters
			if any((word.count(letter) < count) for letter, count in letter_counts.items()):
				continue
			
			print(word)

			new_available.append(word)

		self.available = new_available

		return (guessed_word, word_validity)