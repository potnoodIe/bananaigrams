import enchant
import itertools
import random
from typing import List
import copy
from numba import njit

class Tile:
    def __init__(self, position, letter, score) -> None:
        self.position = position
        self.letter = letter
        self.score = score
        
totalNumberOfTiles = 144

class Player:
    def __init__(self, tiles=[]) -> None:
        self.tiles = tiles
        
    def updateScore(self):
        self.score = sum([tile.score for tile in self.tiles])
        
    totalScore = 0
    
all_tiles = ( ["a"] * 13
            + ["b"] * 3
            + ["c"] * 3
            + ["d"] * 6
            + ["e"] * 18
            + ["f"] * 3
            + ["g"] * 4
            + ["h"] * 3
            + ["i"] * 12
            + ["j"] * 2
            + ["k"] * 2
            + ["l"] * 5
            + ["m"] * 3
            + ["n"] * 8
            + ["o"] * 11
            + ["p"] * 3
            + ["q"] * 2
            + ["r"] * 9
            + ["s"] * 6
            + ["t"] * 9
            + ["u"] * 6
            + ["v"] * 3
            + ["w"] * 3
            + ["x"] * 2
            + ["y"] * 3
            + ["z"] * 2
)

def choose_tiles(n):
    tiles = random.sample(all_tiles, n)
    return tiles

def find_longest_word(tiles, num_iterations):
    d = enchant.Dict("en_UK")
    words : List[str] = []
    
    for word_length in range(len(tiles), 2, -1):
        # candidates = list(map("".join, itertools.permutations(tiles, word_length)))
        for _ in range(num_iterations):
            candidate = "".join(random.sample(tiles, word_length))
            if d.check(candidate):
                words.append(candidate)
        if len(words) > 0:
            break
    
    remaining_tiles = copy.deepcopy(tiles)
    
    if len(words) == 0:
        return "", remaining_tiles
    
    for char in words[0]:
        remaining_tiles.remove(char)
    
    return words[0], remaining_tiles

def attempt_soltuion(tiles: List[str]):
    words = []
    remaining_tiles = copy.deepcopy(tiles)
    
    for i in range(10):        
        print(f"--------\nIteration {i}:")
        word, remaining_tiles = find_longest_word(remaining_tiles, 1000)
        
        if word == "":
            print("No viable word found, restarting.")
            return words, remaining_tiles
        
        words.append(word)
        print(f"Chosen word: {word}")
        print(f"Remaining tiles: {remaining_tiles}")
        
        if len(remaining_tiles) == 0:
            print("All letters used up!")
            return words, []
    
def solve(tiles: List[str], max_iter):
    for i in range(max_iter):
        print(f"\n////// Solution Trial {i} ///////")
        words, remaining_tiles = attempt_soltuion(tiles)
        if len(remaining_tiles) == 0:
            if i == max_iter-1:
                print("No solution was found :(")
            break
    print(f"Final list of words: {words}")
        
    
    
if __name__ == "__main__":
    tiles = choose_tiles(21)
    print("Initial tiles:\n", tiles, "\n-------")
    solve(tiles, 10)
        
        
    # Ideas to try
        # Try to check ahead when choosing "long" words early on that there will be enough useful letters (e.g. vowels) to be able to make a word from them and use up all the letters
        # Instead of taking the first longest word, choose the one with the highest score based on the letters used
        
    # Features to implement
        # Fit words onto a grid and enforce rules like no overlapping & all strings formed by adjacent tiles must be valid words
        # Multiple AI players competing
        # "Split" mechanic when one player runs out of letters from their initial set