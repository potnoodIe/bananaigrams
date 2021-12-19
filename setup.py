from os import X_OK
import enchant
import itertools
import random
from typing import List
import copy
from numba import njit
from matplotlib import pyplot as plt

class Tile:
    def __init__(self, x, y, letter) -> None:
        self.x = x
        self.y = y
        self.position = (x, y)
        self.letter = letter
        # self.score = score
        
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

def placeTiles(letters: List[str]) -> List[Tile]:
    """Function to generate tiles with random positions for testing. 

    Args:
        letters (List[str]): input list of letters to place as tiles

    Returns:
        List[Tile]: output list of tiles with positions set
    """
    tiles: List[Tile] = []
    positions = []
    for i in range(len(letters)):
        successful = False
        while not successful:
            x = random.choice(range(0,15))
            y = random.choice(range(0,15))
            if (x,y) not in positions:
                positions.append((x,y))
                tiles.append(Tile(x, y, letters[i]))
                successful = True
    # plt.scatter(list(zip(*positions))[0], list(zip(*positions))[1])
    # plt.show()
    # print(positions)
    # print(list(zip(*positions))[0])
    return tiles
            

def drawTiles(tiles: List[Tile]) -> None:
    """Function to print tiles as an ascii grid based on their positions.
    Edges of the board automatically resize based on max width 
    and height of board

    Args:
        tiles (List[Tile]): list of tiles as Tile objects containing information about letter and also position
    """
    positions = [t.position for t in tiles]
    letters = [t.letter for t in tiles]
    
    x_min = min(list(zip(*positions))[0])
    x_max = max(list(zip(*positions))[0])
    y_min = min(list(zip(*positions))[1])
    y_max = max(list(zip(*positions))[1])
    
    # Print the tiles
    print("".join(["_"]*(2*(x_max-(x_min-1))+3)))
    
    for y in range(y_max, y_min-1, -1):
        print("| ", end="")
        for x in range(x_min, x_max+1):
            if (x,y) in positions:
                print(letters[positions.index((x,y))], end=" ")
            else:
                print("  ", end="")
        print("|")
        
    print("|" + "".join(["_"]*(2*(x_max-(x_min-1))+1)) + "|")

    

def choose_letters(n):
    tiles = random.sample(all_tiles, n)
    return tiles

def checkTiles(candidate_tiles: List[Tile], board: List[Tile]) -> bool:
    d = enchant.Dict("en_UK")
    candidate_word = "".join([t.letter for t in candidate_tiles])
    if not d.check(candidate_word):
        return False
    else:
        pass
        # Check placement is correct for surrounding tiles
        
        # Move horizontally and vertically from each tile (in both +ve and -ve directions) until whitespace is encountered

def find_longest_valid_word(tiles: List[Tile], board: List[Tile], num_iterations: int) -> List[Tile]:
    
    candidates: List[List[Tile]] = []
    
    for word_length in range(len(tiles), 1, -1):
        for _ in range(num_iterations):
            candidate_tiles = random.sample(tiles, word_length)
            
            # Set the positions of the tiles
            for i in range(len(tiles)):
                candidate_tiles[i].position = (10,10+i)
            # If one of the tiles already has its position set, this determines the positions of the other tiles
            
            # Check the candidate is valid as a word and with the existing tiles
            if checkTiles(candidate_tiles): 
                candidates.append(candidate_tiles)
        # Stop after at least one word has been found, as 
        # this/these will be the longest word/s possible
        if len(candidates) > 0:
            break
    
    remaining_tiles = copy.deepcopy(tiles)
    
    # If no candidates were found, return an empty tile list and the initial set of tiles
    if len(candidates) == 0:
        return [], remaining_tiles

    # Remove used tiles from list of remaining tiles
    for tile in candidates[0]:
        remaining_tiles.remove(tile)
    
    return candidates[0], remaining_tiles

def attempt_soltuion(tiles: List[str]):
    # Start with a clean board
    board: List[Tile] = []
    remaining_tiles = copy.deepcopy(tiles)
    
    for i in range(10):        
        print(f"--------\nIteration {i}:")
        word, remaining_tiles = find_longest_valid_word(remaining_tiles, 1000)
        
        if word == "":
            print("No viable word found.")
            return board, remaining_tiles
        
        
        
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
    # tiles = choose_letters(21)
    # print("Initial tiles:\n", tiles, "\n-------")
    # solve(tiles, 10)
    
    tiles = placeTiles(choose_letters(21))
    drawTiles(tiles)
        
        
    # Ideas to try
        # [ ] Try to check ahead when choosing "long" words early on that there will be enough useful letters (e.g. vowels) to be able to make a word from them and use up all the letters
        # [ ] Instead of taking the first longest word, choose the one with the highest score based on the letters used
        # [ ] Improve efficiency by using numba
        
    # Features to implement
        # [ ] Allow tiles to be reused if they are part of existing words and can form viable new words with the remaining tiles
        # [ ] Fit words onto a grid and enforce rules like no overlapping & all strings formed by adjacent tiles must be valid words
        # [ ] Multiple AI players competing
        # [ ] "Split" mechanic when one player runs out of letters from their initial set
        
    # Milestones
        # [ ] Place tiles horizontally, setting tile positions correctly
        # [ ] Place tiles vertically as well as horizontally
        # [ ] Place unconnected whole words on a board and check their validity both as words and with respect to the surrounding tiles