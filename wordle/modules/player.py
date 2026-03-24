from pyansi import AnsiStyle, PaletteColor, Palette
from wordle import LetterValidity, WordlePlayer
from modules.formatting import render_keyboard

ERROR_STYLE = AnsiStyle(fg=Palette(PaletteColor.BrightRed))


def error(text: str):
    print(ERROR_STYLE.apply_with_reset(text))


class HumanWordlePlayer(WordlePlayer):
    def __init__(self, word_length: int, valid_dictionary: list[str]) -> None:
        self.word_length = word_length
        self.valid_dictionary = valid_dictionary
        self.letter_validity: dict[str, LetterValidity] = {}

    def prompt_word(self, prompt: str = "Guess") -> str:
        while True:
            print("\n" + render_keyboard(self.letter_validity))

            player_guess = input(f"{prompt}: ")

            guess_len = len(player_guess)

            if guess_len < self.word_length:
                error(f"Not enough letters. ({guess_len} < {self.word_length})")
                continue
            elif guess_len > self.word_length:
                error(f"Too many letters. ({guess_len} > {self.word_length})")
                continue
            elif player_guess not in self.valid_dictionary:
                error("Word not in dictionary.")
                continue

            return player_guess

    def on_guess_feedback(self, guessed_word: str, word_validity: list[LetterValidity]):
        for char, validity in zip(guessed_word, word_validity):
            existing_validity = self.letter_validity.get(char)
            new_validity = existing_validity or validity

            if (
                existing_validity == LetterValidity.Exists
                and validity == LetterValidity.Correct
            ):
                new_validity = validity

            self.letter_validity[char] = new_validity
