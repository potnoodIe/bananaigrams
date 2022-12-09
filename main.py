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
    utils.displayTiles(player1.board)
    
    solver.nextWord(player1.hand, player1.board)
    print(player1)
    utils.displayTiles(player1.board)
    
    print([f"{t.letter}, nbs: {t.nbs}" for t  in player1.board])
    
    solver.nextWord(player1.hand, player1.board)
    print(player1)
    utils.displayTiles(player1.board)
    
    # tiles = randomPlaceTiles(chooseLetters(21))
    # displayTiles(tiles)