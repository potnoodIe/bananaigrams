import enchant
import itertools
import random
from typing import List, Dict
import copy
# from numba import jit
import numpy as np
from matplotlib import pyplot as plt
import utils

class Tile:
    """Class to represent a tile, including letter and position.
    nb_ attributes encode the connections between 
    different tiles, similar to a directed graph
    """
    nbs = {"l": None, "r": None, "u": None, "d": None}
    
    def __init__(self, letter, x=None, y=None) -> None:
        self.letter: str = letter
        self.x: int = x
        self.y: int = y
        self.position = (x, y)
        self.score = utils.scores[self.letter]
        
    def __str__(self) -> str:
        return self.letter
    
    def __repr__(self) -> str:
        return self.letter
        
    def set_nb(self, direction, tile):
        if direction not in ["l", "r", "u", "d"]:
            raise KeyError("Please specify a valid direction from: l, r, u, d")
        self.nbs[direction] = tile
    
    def nb(self, direction) -> 'Tile':
        if direction not in ["l", "r", "u", "d"]:
            raise KeyError("Please specify a valid direction from: l, r, u, d")
        return self.nbs[direction]
        
class Player:
    hand: List[Tile] = []
    board: List[Tile] = []
    score: int = 0
    
    def __init__(self, initial_letters: List[str] = []) -> None:
        self.hand = [Tile(l) for l in initial_letters]
        
    def __str__(self):
        return f"Board:\n{self.board.__str__()}\nHand:\n{self.hand.__str__()}"
        
    def updateScore(self):
        self.score = sum([tile.score for tile in self.board])
        
    def solve(self, max_iter):
        for i in range(max_iter):
            print(f"\n////// Solution Trial {i} ///////")
            
            words, remaining_tiles = attempt_soltuion(self.hand)
            
            if len(remaining_tiles) == 0:
                if i == max_iter-1:
                    print("No solution was found :(")
                break
            
        print(f"Final list of words: {words}")
        
class Game:
    players: List[Player]
    
    def play(self):
        pass

def set_nbs(tiles: List[Tile], vertical: bool) -> None:
        for i in range(len(tiles)-1):
            if vertical:
                tiles[i].set_nb("r", tiles[i+1])
                tiles[i+1].set_nb("l", tiles[i])
            else:
                tiles[i].set_nb("d", tiles[i+1])
                tiles[i+1].set_nb("u", tiles[i])

# Deprecated
def find_longest_valid_word(tiles: List[Tile], board: List[Tile], num_iterations: int) -> List[Tile]:
    
    candidates: List[List[Tile]] = []
    board_positions = [t.position for t in board]
    
    max_word_length = 10
    
    for word_length in range(max_word_length, 1, -1):
        for _ in range(num_iterations):
            candidate_letters = random.sample(tiles, word_length)
            candidate_tiles = [Tile(l) for l in candidate_letters]
            
            print("Candidate letters:", candidate_letters)
            # Check the candidate is valid as a word and with the existing tiles
            if not checkTiles(candidate_tiles, board): 
                break
                # candidates.append(candidate_tiles)
            
            # Set the orientation of the group of tiles (randomly for now)
            vertical: bool = random.choice([True, False])
            print("Vertical: ", vertical)
            
            # Set the positions of the tiles
            successful = False
            while not successful:
                starting_position = (random.choice(range(15)), random.choice(range(15)))
                print("Trying with starting position:", starting_position)
                print("len(tiles)=",len(candidate_tiles))
                for i in range(len(candidate_tiles)):
                    print("i=",i)
                    if vertical == True:
                        tile_pos = (starting_position[0],starting_position[1]-i)
                        if tile_pos in board_positions:
                            print("Unsuccessful")
                            break
                        else:
                            candidate_tiles[i].position = tile_pos
                            if i == len(candidate_tiles)-1:
                                print("Successful")
                                successful = True
                    else:
                        tile_pos = (starting_position[0]+i,starting_position[1])
                        if tile_pos in board_positions:
                            print("Unsuccessful")
                            break
                        else:
                            candidate_tiles[i].position = tile_pos
                            if i == len(candidate_tiles)-1:
                                print("Successful")
                                successful = True
                print("Successful: ", successful)
            
            # If one of the tiles already has its position set, this determines the positions of the other tiles (future)
            
            # Set the neighbours of the tiles in the group
            for i in range (len(candidate_tiles)-1):
                if vertical == True:
                    candidate_tiles[i].nb_down = candidate_tiles[i+1]
                    candidate_tiles[i+1].nb_up = candidate_tiles[i]
                else:
                    candidate_tiles[i].nb_right = candidate_tiles[i+1]
                    candidate_tiles[i+1].nb_left = candidate_tiles[i]        
                
            candidates.append(candidate_tiles)
            
        # Stop after at least one word has been found, as 
        # this/these will be the longest word/s possible
        if len(candidates) > 0:
            break
    
    # If no candidates were found, return an empty tile list and the initial set of tiles
    if len(candidates) == 0:
        return [], tiles

    remaining_tiles = copy.deepcopy(tiles)
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
        candidate_tiles, remaining_tiles = find_longest_valid_word(remaining_tiles, board, 100)
        
        if candidate_tiles == []:
            print("No viable word found.")
            return board, remaining_tiles
        
        board.append(candidate_tiles)
        print(f"Chosen word: {''.join([t.letter for t in candidate_tiles])}")
        print(f"Remaining tiles: {[t.letter for t  in remaining_tiles]}")
        utils.displayTiles(board)
        
        if len(remaining_tiles) == 0:
            print("All letters used up!")
            return board, []

def checkTiles(candidateTiles: List[Tile], vertical=None) -> bool:
    if not checkWord(candidateTiles):
        return False
    else:
        # If orientation isn't specified (i.e. for checking the first word) then skip checking surrounding tiles
        if vertical == None: return True
        
        d = enchant.Dict("en_UK")
        # Check placement is correct wrt surrounding tiles i.e. that any auxiliary words formed (auxWord) are valid
        for tile in candidateTiles:
            ind = ["l", "r"] if vertical else ["u", "d"]
            auxTiles = [fetchNeighbours(tile, ind[0]), tile, fetchNeighbours(tile, ind[1])]
            auxWord = "".join([t.letter for t in auxTiles])
            if not d.check(auxWord):
                return False
        return True
 
def checkWord(candidateTiles: List[Tile]) -> bool:
    d = enchant.Dict("en_UK")
    candidateWord = "".join([t.letter for t in candidateTiles])
    if not d.check(candidateWord):
        return False
    else:
        return True

def fetchNeighbours(tile: Tile, direction: str) -> List[Tile]:
    """Recursively find all neighbours of a tile along a particular direction"""
    if tile.nb(direction) is None:
        return []
    else:
        return [tile.nb(direction), fetchNeighbours(tile, direction)]

def chooseFirstWord(hand: List[Tile], board: List[Tile], maxWordLength: int = 5, numIterations: int = 1000) -> List[Tile]:
    d = enchant.Dict("en_UK")
    candidate_words: List[List[str]] = []
    candidate_indices_lists: List[List[int]] = []

    for word_length in range(maxWordLength, 1, -1):
        for _ in range(numIterations):
            sample = [(t.letter, hand.index(t)) for t in random.sample(hand, word_length)]
            candidate_word = "".join(tup[0] for tup in sample)
            candidate_indices = [tup[1] for tup in sample]
            print("Candidate letters:", candidate_word)
            
            # Check the candidate is valid as a word
            if not d.check(candidate_word): 
                # print(f"Candidate word {''.join([t.letter for t in candidateTiles])} not viable")
                continue
            
            candidate_words.append(candidate_word)
            candidate_indices_lists.append(candidate_indices) 
            
        # Stop after at least one word has been found, as 
        # this/these will be the longest word/s possible
        if len(candidate_words) > 0:
            break
        
    # If no candidates were found for any word length attempted, return an empty tile list and the initial set of tiles
    if len(candidate_words) == 0:
        print("No viable word found.")
        return [], hand
            
    # Create tiles for candidate words
    candidate_tiles_lists: List[List[Tile]] = [[hand[i] for i in ci] for ci in candidate_indices_lists]
        
    # Choose the set of candidate tiles with the highest Scrabble score to go forward
    scores = [sum([t.score for t in ts]) for ts in candidate_tiles_lists]  
    chosen_tiles = candidate_tiles_lists[scores.index(max(scores))]
    
    print(candidate_tiles_lists)
    print(scores)
    print("Chosen word:", chosen_tiles, "with score =", max(scores))

    # Set the orientation of the group of tiles (randomly, for now)
    vertical: bool = random.choice([True, False])
    print("Vertical: ", vertical)
    
    # Remove used tiles from list of remaining tiles
    # remaining_tiles = copy.deepcopy(tiles)
    for tile in chosen_tiles:
        hand.remove(tile)
        
    # Set the positions of the tiles, starting with the first tile on (0,0)
    for i in range(len(chosen_tiles)):
        chosen_tiles[i].position = (0,-i) if vertical else (i,0)
    
    # Set the neighbours of the tiles in the group
    set_nbs(chosen_tiles, vertical)
    
    # Modify the board passed in
    board += chosen_tiles
    
    # Return the updated hand and board passed in
    return hand, board


def nextWord(hand: List[Tile], board: List[Tile], maxWordLength: int = 10, numIterations: int = 1000) -> List[Tile]:
    candidates: List[List[Tile]] = []

    for word_length in range(maxWordLength, 1, -1):
        for _ in range(3): # numIterations):
             # choose one viable letter from the board and the rest from the hand
            candidateTiles = random.shuffle( random.sample(hand, word_length-1) + random.sample(board, 1) )
            print(candidateTiles)
    
def attempt_solution_new(hand: List[Tile]):
    pass
    
    
# Ideas to try
    # [ ] Try to check ahead when choosing "long" words early on that there will be enough useful letters (e.g. vowels) to be able to make a word from them and use up all the letters
    # [ ] Instead of taking the first longest word, choose the one with the highest score based on the letters used
    # [ ] Improve efficiency by using numba
    # [ ] Implement a "Tiles" class which can replace List[Tile] and also perform operations on collections of tiles (e.g. the set_nbs function)
    
# Features to implement
    # [ ] Allow tiles to be reused if they are part of existing words and can form viable new words with the remaining tiles
    # [ ] Fit words onto a grid and enforce rules like no overlapping & all strings formed by adjacent tiles must be valid words
    # [ ] Multiple AI players competing
    # [ ] "Split" mechanic when one player runs out of letters from their initial set
    
# Milestones
    # [ ] Place tiles horizontally, setting tile positions correctly
    # [ ] Place tiles vertically as well as horizontally
    # [ ] Place unconnected whole words on a board and check their validity both as words and with respect to the surrounding tiles