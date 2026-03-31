from wordle import WordleGame, LetterValidity, get_word_validity
from wordle.game import Guess
from wordle.formatting import format_guess


def merge_validities(*values: list[LetterValidity]):
    if len(values) == 1:
        return values[0]
    return list(map(max, *values))


class XordleGame(WordleGame):
    def __init__(self, target_words: list[str], max_guesses: int = 8) -> None:
        super().__init__()
        self.remaining_words = target_words[:]
        self.max_guesses = max_guesses

    @property
    def is_won(self) -> bool:
        return len(self.remaining_words) == 0

    @property
    def is_done(self) -> bool:
        return len(self.guess_history) >= self.max_guesses or self.is_won

    def check_validity(self, word: str) -> list[LetterValidity]:
        return merge_validities(
            *[get_word_validity(word, secret) for secret in self.remaining_words]
        )

    def make_guess(self, word: str) -> Guess:
        guess = super().make_guess(word)
        if word in self.remaining_words:
            self.remaining_words.remove(word)
        return guess


secret_words = ["brain", "storm"]
game = XordleGame(secret_words)
game.make_guess("study")

while not game.is_done:
    for guess in game.guess_history:
        print(format_guess(guess))

    game.make_guess(input("> "))

for guess in game.guess_history:
    print(format_guess(guess))

print(f"The secret words were {', '.join(secret_words)}")
