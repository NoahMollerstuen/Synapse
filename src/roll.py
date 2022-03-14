import typing as t
import random


class Roll:
    """Represents the result of a single roll of a dicepool"""

    results: t.List[int]
    hits: int
    glitch: bool
    critical_glitch: bool

    def __init__(self, results: t.List[int]):
        self.results = results
        self.hits = len([i for i in results if i >= 5])

        ones = len([i for i in results if i == 1])
        self.glitch = ones * 2 > len(results)
        self.critical_glitch = self.glitch and self.hits == 0

    @classmethod
    def roll(cls, numb: int):
        results = [random.randint(1, 6) for i in range(0, numb)]
        return Roll(results)
