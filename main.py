import random
import utils
import solver

if __name__ == "__main__":
    random.seed(1)
    
    initial_letters = utils.chooseLetters(21)
    print("Initial letters:\n", initial_letters, "\n-------")
    
    player1 = solver.Player(initial_letters)    
    print(f"Player 1: {player1}")
    
    solver.chooseFirstWord(player1.hand, player1.board)
    
    print(player1)
    
    # tiles = randomPlaceTiles(chooseLetters(21))
    # displayTiles(tiles)