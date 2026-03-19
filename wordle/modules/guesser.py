from modules.player import WordlePlayer
from modules.game import WordleGame, LetterValidity, DICTIONARY

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_LIST = {letter for letter in ALPHABET}

def analyze_letter_frequencies(word_set: list[str], allowed_letters: set[str] = ALPHABET_LIST) -> tuple[dict[str, int], list[dict[str, int]]]:
	frequencies: dict[str, int] = {letter:sum(word.count(letter) for word in word_set) for letter in allowed_letters}
	frequencies_per_position: list[dict[str, int]] = [{letter:sum(1 for word in word_set if word[index] == letter) for letter in allowed_letters} for index in range(max(len(word) for word in word_set))]

	return (frequencies, frequencies_per_position)

IGP_UNKNOWN_LETTER_MULT = 1.1
IGP_POSITIONAL_FREQUENCY_WEIGHT = 10
IGP_GENERAL_FREQUENCY_WEIGHT = 1

DUPLICATE_PENALTY_FALLOFF = 10
KNOWN_PENALTY = -20

CONFIDENCE_THRESHOLD = 0.65
CONFIDENCE_WORD_FALLOFF = 0.8
CONFIDENCE_LETTER_FALLOFF = 0.8
CONFIDENCE_ENDGAME_GROWTH_RATE = 10

class WordleGuesser(WordlePlayer):
	def __init__(self, game: WordleGame) -> None:
		self.game = game
		self.reset()

	def reset(self):
		self.available: list[str] = DICTIONARY.copy()
		self.unknown_letters: set[str] = ALPHABET_LIST.copy()
		self.known_letters: set[str] = set()
		self.invalid_letters: set[str] = set()

		self.existing_letters: dict[int, str] = {}
		self.correct_letters: dict[int, str] = {}

	def determine_word(self) -> str:
		if len(self.available) == 1:
			(word,) = self.available
			return word
		
		game = self.game

		scored_words: list[tuple[str, float]] = []

		look_for_letters: set[str] = {letter for word in self.available for letter in word if letter in self.unknown_letters}
		frequencies, frequencies_per_position = analyze_letter_frequencies(self.available, look_for_letters)


		# confidence grows over the span of a game to force it to make guesses instead of getting greedy with information
		endgame_confidence = (len(game.guesses) / game.max_guesses) ** CONFIDENCE_ENDGAME_GROWTH_RATE
		# confidence grows as more and more letters are eliminated, to discourage needless information gathering
		letter_confidence = CONFIDENCE_LETTER_FALLOFF ** len(look_for_letters)
		# confidencce grows a more and more words are eliminated
		word_confidence = CONFIDENCE_WORD_FALLOFF ** len(self.available)
		
		total_confidence = word_confidence + endgame_confidence + letter_confidence
		# print(f"C:{total_confidence}\nA:{self.available}\nF:{look_for_letters}\nUF:{frequencies}")

		# if we're fairly confident about the word then we can attempt to guess it
		# otherwise try to gather more information
		if total_confidence >= CONFIDENCE_THRESHOLD:
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
				score = 0

				duplicate_letters: dict[str, int] = {}
				for index, letter in enumerate(word):
					# don't give any additional score for correct letters, as they're pointless
					if self.correct_letters.get(index) == letter:
						continue

					frequency = frequencies.get(letter, 0)
					positional_frequency = frequencies_per_position[index].get(letter, 0)

					occurances = duplicate_letters.get(letter, 0)
					duplicate_letters[letter] = occurances + 1

					duplicate_penalty = DUPLICATE_PENALTY_FALLOFF ** -occurances
					known_penalty = KNOWN_PENALTY if letter in self.known_letters else 0

					score += (frequency * IGP_GENERAL_FREQUENCY_WEIGHT + positional_frequency * IGP_UNKNOWN_LETTER_MULT) * duplicate_penalty + known_penalty
				
				for letter in look_for_letters:
					if letter in word:
						score *= IGP_UNKNOWN_LETTER_MULT

				scored_words.append((word, score))

		scored_words.sort(key=lambda x: x[1], reverse=True)

		# print(scored_words)

		return scored_words[0][0]
	
	def make_guess(self, force_word: str | None = None):
		guessed_word, word_validity = self.game.make_guess(force_word or self.determine_word())

		letter_counts: dict[str, int] = {}
		letter_limits: dict[str, int] = {}

		for index, (letter, validity) in enumerate(zip(guessed_word, word_validity)):
			if letter in self.unknown_letters:
				self.unknown_letters.remove(letter)
				self.known_letters.add(letter)
			
			if validity == LetterValidity.Correct or validity == LetterValidity.Exists:
				letter_counts[letter] = letter_counts.get(letter, 0) + 1
			
			if validity == LetterValidity.Incorrect and letter not in self.invalid_letters:
				self.invalid_letters.add(letter)

			if validity == LetterValidity.Exists:
				self.existing_letters[index] = letter

			if validity == LetterValidity.Correct:
				self.correct_letters[index] = letter
				if self.existing_letters.get(index) != None:
					del self.existing_letters[index]

			if validity == LetterValidity.TooMany:
				letter_limits[letter] = letter_limits.get(letter, guessed_word.count(letter)) - 1

		new_available = []

		# word filtering
		for word in self.available:
			# remove words that contain any invalid letters
			if any(True for letter in self.invalid_letters if (letter in word)):
				continue
			# remove words that don't have the correct letters
			if any(True for index, letter in self.correct_letters.items() if (word[index] != letter)):
				continue
			# remove words that have letters in the wrong position, or don't contain any existing letters
			if any(True for index, letter in self.existing_letters.items() if (word[index] == letter or letter not in word)):
				continue
			# remove words that have too many letters
			if any((True for letter, count in letter_limits.items() if word.count(letter) > count)):
				continue
			# remove words that have too little letters
			if any(True for letter, count in letter_counts.items() if (word.count(letter) < count)):
				continue
			
			new_available.append(word)

		self.available = new_available

		return (guessed_word, word_validity)