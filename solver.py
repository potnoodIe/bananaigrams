import enchant
import itertools
import random
from typing import List, Dict, Tuple
import copy
# from numba import jit
import numpy as np
from matplotlib import pyplot as plt
import utils

class Tile:
    """Class to represent a tile, including letter and position.
    nbs encodes the connections between 
    different tiles, similar to a directed graph
    """
    
    # For some weird reason, setting nbs below to {"l": None, "r": None, "u": None, "d": None} caused all copies of nbs (i.e. for all tiles) to be the same?!
    nbs = {}
    hand = None
    
    def __init__(self, letter, x=None, y=None) -> None:
        self.letter: str = letter
        self.x: int = x
        self.y: int = y
        self.position = (x, y)
        self.score = utils.SCORES[self.letter]
        self.nbs = {"l": None, "r": None, "u": None, "d": None}
        
    def __str__(self) -> str:
        return self.letter
    
    def __repr__(self) -> str:
        return self.letter
        
    def set_nb(self, direction, tile) -> None:
        if direction not in ["l", "r", "u", "d"]:
            raise KeyError("Please specify a valid direction from: l, r, u, d")
        self.nbs[direction] = tile
        
    def set_nbs(self, nbs: Dict) -> None:
        if list(nbs.keys()) != ["l", "r", "u", "d"]:
            raise KeyError(f"Keys of nbs must be ['l', 'r', 'u', 'd'] but got {list(nbs.keys())}")
        self.nbs = nbs
    
    def nb(self, direction) -> 'Tile':
        if direction not in ["l", "r", "u", "d"]:
            raise KeyError("Please specify a valid direction from: l, r, u, d")
        return self.nbs[direction]
        
class Player:
    hand: List[Tile] = []
    board: List[Tile] = []
    board_positions: List[Tuple[int, int]] = []
    score: int = 0
    
    def __init__(self, initial_letters: List[str] = []) -> None:
        self.hand = [ Tile(l) for l in initial_letters]
        
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

def set_word_nbs(tiles: List[Tile], vertical: bool) -> None:
        #print(f"\nSetting nbs to tiles: {tiles}")
        #print(f"Vertical = {vertical}")
        #print(f"len(tiles) = {len(tiles)}")
        for i in range(len(tiles)-1):
            #print(f"i = {i}")
            if vertical:
                #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])
                #print(f"Setting d nb of {tiles[i]} to {tiles[i+1]}")
                tiles[i].set_nb("d", tiles[i+1])
                #print(f"Setting u nb of {tiles[i+1]} to {tiles[i]}")
                tiles[i+1].set_nb("u", tiles[i])
                #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])
            else:
                # There's something fucky with mutable objects going on...
                #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])
                #print(f"Setting r nb of {tiles[i]} to {tiles[i+1]}")
                #print(tiles)
                tiles[i].set_nb("r", tiles[i+1])
                #print(tiles)
                #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])
                #print(f"Setting l nb of {tiles[i+1]} to {tiles[i]}")
                tiles[i+1].set_nb("l", tiles[i])
                #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])
        #print([f"{t.letter}, nbs: {t.nbs}" for t  in tiles])

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

def checkPlacement(candidateTiles: List[Tile], board: List[Tile], vertical: bool) -> bool:
    d = enchant.Dict("en_UK")
    
    board_positions = [t.position for t in board]
    auxTiles = []
    potential_nbs: Dict[Tile: Dict[str: Tile]] = {}
    
    ind = ['u', 'd'] if vertical else ['l', 'r']
    
    print(f"Vertical in placement check: {vertical}")
    
    for tile in candidateTiles:
        
        if tile.hand == False:
            continue
        
        print(f"Checking tile: {tile}")
        print(f"Position: {tile.position}")
        potential_nbs[tile] = {"l": None, "r": None, "u": None, "d": None}
        
        # Check left, right directions
        print("Checking left/right")
        all_left_tiles = []
        all_right_tiles = []
        
        # Is there a neighbouring tile to the left?
        pos_l = (tile.position[0]-1, tile.position[1])
        if pos_l in board_positions:
            # Fetch all contiguous tiles to the left
            left_nb = board[board_positions.index(pos_l)]
            all_left_tiles = fetchNeighbours(left_nb, "l")
            print("All left tiles:", all_left_tiles)
            
            if len(all_left_tiles) == 0:
                continue
            
            potential_nbs[tile]['l'] = left_nb
        
        # Is there a neighbouring tile to the right?
        pos_r = (tile.position[0]+1, tile.position[1])
        if pos_r in board_positions:
            # Fetch all contiguous tiles to the right
            right_nb = board[board_positions.index(pos_r)]
            all_right_tiles = fetchNeighbours(right_nb, "r")
            print("All right tiles:", all_left_tiles)
            
            if len(all_right_tiles) == 0:
                continue
            
            potential_nbs[tile]['r'] = right_nb
        
        # Do the left and/or right neighbouring tiles form a valid word with the current tile?
        trial_word = "".join([t.letter for t in all_left_tiles + [tile] + all_right_tiles])
        
        if len(trial_word) == 1:
            pass
        else:
            # Check trial word against dictionary
            print(f"Checking horizontal trial word: {trial_word}")
            
            if not d.check(trial_word):
                return False
        
        # Check up, down directions
        print("Checking up/down")
        all_up_tiles = []
        all_down_tiles = []
        
        # Is there a neighbouring tile upwards?
        pos_u = (tile.position[0], tile.position[1]+1)
        if pos_u in board_positions:
            # Fetch all contiguous tiles upwards
            up_nb = board[board_positions.index(pos_u)]
            all_up_tiles = fetchNeighbours(up_nb, "u")
            print("All upward tiles:", all_up_tiles)
            
            if len(all_up_tiles) == 0:
                continue
            
            potential_nbs[tile]['u'] = up_nb
        
        # Is there a neighbouring tile downwards?
        pos_d = (tile.position[0], tile.position[1]-1)
        if pos_d in board_positions:
            # Fetch all contiguous tiles downwards
            down_nb = board[board_positions.index(pos_d)]
            all_down_tiles = fetchNeighbours(down_nb, "d")
            
            if len(all_down_tiles) == 0:
                continue
            
            print("All downward tiles:", all_down_tiles)
            potential_nbs[tile]['d'] = down_nb
        
        
        # Do the upward and/or downward neighbouring tiles form a valid word with the current tile?
        trial_word = "".join([t.letter for t in all_up_tiles + [tile] + all_down_tiles])
        
        print(f"Checking vertical trial word: {trial_word}")
        
        if len(trial_word) == 1:
            continue
        if not d.check(trial_word):
            return False
        
    for tile in candidateTiles:
        if tile.hand == False:
            continue
        tile.set_nbs(potential_nbs[tile])
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
        nb_list = [tile.nb(direction)] if tile.nb(direction) is not None else []
        return nb_list + fetchNeighbours(tile.nb(direction), direction)

def chooseFirstWord(hand: List[Tile], board: List[Tile], maxWordLength: int = 5, numIterations: int = 1000) -> List[Tile]:
    d = enchant.Dict("en_UK")
    candidate_words: List[List[str]] = []
    candidate_indices_lists: List[List[int]] = []

    for word_length in range(maxWordLength, 1, -1):
        for _ in range(numIterations):
            sample = [(t.letter, hand.index(t)) for t in random.sample(hand, word_length)]
            candidate_word = "".join(tup[0] for tup in sample)
            candidate_indices = [tup[1] for tup in sample]
            #print("Candidate letters:", candidate_word)
            
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
    print("Vertical (first word): ", vertical)
    
    # Remove used tiles from list of remaining tiles
    # remaining_tiles = copy.deepcopy(tiles)
    for tile in chosen_tiles:
        hand.remove(tile)
        
    # Set the positions of the tiles, starting with the first tile on (0,0)
    for i in range(len(chosen_tiles)):
        chosen_tiles[i].position = (0,-i) if vertical else (i,0)
    
    print("\n".join([f"{t.letter}, nbs: {t.nbs}" for t  in chosen_tiles]))
    # Set the neighbours of the tiles in the group
    set_word_nbs(chosen_tiles, vertical)
    print("\n".join([f"{t.letter}, nbs: {t.nbs}" for t  in chosen_tiles]))
    
    # Modify the board passed in
    board += chosen_tiles
    
    for tile in board:
        tile.hand = False
        
    for tile in hand:
        tile.hand = True
    
    # Return the updated hand and board passed in
    return hand, board


def nextWord(hand: List[Tile], board: List[Tile], maxWordLength: int = 5, numIterations: int = 1000) -> List[Tile]:
    d = enchant.Dict("en_UK")
    candidates: List[Dict[ str: List[Tile],bool]] = []

    for word_length in range(maxWordLength, 1, -1):
        for _ in range(numIterations):
            # choose one viable letter from the board and the rest from the hand
            # candidateTiles = random.shuffle( random.sample(hand, word_length-1) + random.sample(board, 1) )
            # print(candidateTiles)
            
            hand_sample = [(t.letter, hand.index(t), 'h') for t in random.sample(hand, min(len(hand), word_length-1))]
            board_sample = [(t.letter, board.index(t), 'b') for t in random.sample(board, 1)]
            sample = hand_sample + board_sample
            random.shuffle(sample)
            #print(f"\nHand sample: {hand_sample}\nboard sample: {board_sample} with nbs {[board[t[1]].nbs for t in board_sample]}")
        
            candidate_word = "".join(tup[0] for tup in sample)
            candidate_indices = [tup[1] for tup in sample]
            hand_or_board = [tup[2] for tup in sample]
            print("Candidate word:", candidate_word)
            
            # Check the candidate is valid as a word
            if not d.check(candidate_word): 
                # print(f"Candidate word {''.join([t.letter for t in candidateTiles])} not viable")
                # print("Failed dictionary test")
                continue
            
            candidate_tiles = [hand[candidate_indices[i]] if hand_or_board[i] == 'h' else board[candidate_indices[i]] for i in range(len(candidate_indices))]
            
            print("\n".join([f"{t.letter}: {t.nbs}" for t in candidate_tiles]))
            
            # Set vertical bool based on orientation of word containing letter from board
            if board[board_sample[0][1]].nbs['l'] or board[board_sample[0][1]].nbs['r']:
                if board[board_sample[0][1]].nbs['u'] or board[board_sample[0][1]].nbs['d']:
                    print("Can't place candidate word because board letter is used both vertically and horizontally already")
                    continue
                vertical = True
            else:
                vertical = False
        
            # Set the positions of the tiles temporarily to check placement
            board_tile_ind: int = [i for i in range(len(candidate_tiles)) if candidate_tiles[i].hand == False][0]
            board_tile = candidate_tiles[board_tile_ind]
            for i in range(len(candidate_tiles)):
                dist_from_board_tile = i - board_tile_ind
                candidate_tiles[i].position = (board_tile.position[0], board_tile.position[1] - dist_from_board_tile) if vertical else (board_tile.position[0] + dist_from_board_tile, board_tile.position[1])
            
            print(f"Vertical before placement check: {vertical}")
            if not checkPlacement(candidate_tiles, board, vertical):
                print("Failed placement test\n")
                continue
            print("Passed placement test")
            
            candidates.append({"tiles": candidate_tiles, "vertical": vertical})
            
        # Stop after at least one word has been found, as 
        # this/these will be the longest word/s possible
        if len(candidates) > 0:
            break
        
    # If no candidates were found for any word length attempted, return an empty tile list and the initial set of tiles
    if len(candidates) == 0:
        print("No viable word found.")
        return [], hand
        
    # Choose the set of candidate tiles with the highest Scrabble score to go forward
    scores = [sum([tile.score for tile in d["tiles"]]) for d in candidates]  
    chosen_tiles = candidates[scores.index(max(scores))]["tiles"]
    # Recall vertical value for chosen tiles
    vertical = candidates[scores.index(max(scores))]["vertical"]
    
    # Make sure the positions of the tiles are set to those of the chosen word, rather than the last word found
    board_tile_ind: int = [i for i in range(len(chosen_tiles)) if chosen_tiles[i].hand == False][0]
    board_tile = chosen_tiles[board_tile_ind]
    print(f"Vertical after placement check : {vertical}")
    print(f"Board tile position: ({board_tile.position[0], board_tile.position[1]}")
    for i in range(len(chosen_tiles)):
        dist_from_board_tile = i - board_tile_ind
        print(f"i={i}")
        print(f"Distance: {dist_from_board_tile}")
        chosen_tiles[i].position = (board_tile.position[0], board_tile.position[1] - dist_from_board_tile) if vertical else (board_tile.position[0] + dist_from_board_tile, board_tile.position[1])
    
    print(f"---------------\nCandidates: {candidates}")
    print(f"with scores: {scores}")
    print("Chosen word:", chosen_tiles, "with score =", max(scores))
    
    print([t.position for t in chosen_tiles])
    
    # Remove used tiles from list of remaining tiles
    # remaining_tiles = copy.deepcopy(tiles)
    for tile in chosen_tiles:
        # Need to check if tile is in hand before removal since one of the tiles will be in board instead
        if tile in hand:
            hand.remove(tile)
    
    # Set the neighbours of the tiles in the group
    set_word_nbs(chosen_tiles, vertical)
    
    # Modify the board
    board += [t for t in chosen_tiles if t.hand == True]
    
    # Update hand attribute to show that chosen tiles are on the board
    for tile in chosen_tiles:
        tile.hand = False
    
    # Return the updated hand and board passed in
    return hand, board
    
def attempt_solution_new(hand: List[Tile]):
    pass
    
    
# Ideas to try
    # [ ] Try to check ahead when choosing "long" words early on that there will be enough useful letters (e.g. vowels) to be able to make a word from them and use up all the letters
    # [ ] Instead of taking the first longest word, choose the one with the highest score based on the letters used
    # [ ] Improve efficiency by using numba
    # [ ] Implement a "Tiles" class which can replace List[Tile] and also perform operations on collections of tiles (e.g. the set_word_nbs function)
    
# Features to implement
    # [ ] Allow tiles to be reused if they are part of existing words and can form viable new words with the remaining tiles
    # [ ] Fit words onto a grid and enforce rules like no overlapping & all strings formed by adjacent tiles must be valid words
    # [ ] Multiple AI players competing
    # [ ] "Split" mechanic when one player runs out of letters from their initial set
    
# Milestones
    # [ ] Place tiles horizontally, setting tile positions correctly
    # [ ] Place tiles vertically as well as horizontally
    # [ ] Place unconnected whole words on a board and check their validity both as words and with respect to the surrounding tiles