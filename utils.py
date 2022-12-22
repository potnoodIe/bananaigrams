import random
from typing import List
from solver import Tile
    
ALL_TILES = ( ["a"] * 13
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

SCORES ={"a": 1,
         "b": 3,
         "c": 3,
         "d": 2,
         "e": 1,
         "f": 4,
         "g": 2,
         "h": 4,
         "i": 1,
         "j": 8,
         "k": 5,
         "l": 1,
         "m": 3,
         "n": 1,
         "o": 1,
         "p": 3,
         "q": 10,
         "r": 1,
         "s": 1,
         "t": 1,
         "u": 1,
         "v": 4,
         "w": 4,
         "x": 8,
         "y": 4,
         "z": 10
}
    
def chooseLetters(n):
    tiles = random.sample(ALL_TILES, n)
    return tiles

def displayTiles(tiles: List[Tile]) -> None:
    """Function to print tiles as an ascii grid based on their positions.
    Edges of the board automatically resize based on max width 
    and height of board

    Args:
        tiles (List[Tile]): list of tiles as Tile objects containing information about letter and also position
    """
    positions = [t.position for t in tiles]
    letters = [t.letter for t in tiles]
    print("-------------------")
    print(letters)
    print(positions)
    
    x_min = min(list(zip(*positions))[0])
    x_max = max(list(zip(*positions))[0])
    y_min = min(list(zip(*positions))[1])
    y_max = max(list(zip(*positions))[1])
    
    print(f"x_min: {x_min}")
    print(f"x_max: {x_max}")
    print(f"y_min: {y_min}")
    print(f"y_max: {y_max}")
    
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
    
def displayConnectivity(tiles: List[Tile]) -> None:
    """Function to print tiles as an ascii grid, showing both their positions and connections with neighbouring tiles.
    Edges of the board automatically resize based on max width and height

    Args:
        tiles (List[Tile]): list of tiles as Tile objects containing information about letter and also position
    """
    positions = [t.position for t in tiles]
    letters = [t.letter for t in tiles]
    print("-------------------")
    print(letters)
    print(positions)
    
    x_min = min(list(zip(*positions))[0])
    x_max = max(list(zip(*positions))[0])
    y_min = min(list(zip(*positions))[1])
    y_max = max(list(zip(*positions))[1])
    
    # Print the tiles
    # print(" ".join([str(i) for i in range(2*(x_max-(x_min-1))+3)]))
    print("  ","".join(["_"]*(2*(x_max-(x_min-1))+3)))
    
    for y in range(y_max, y_min-1, -1):
        print(f"{y} " if y<10 else y,"| ", end="")
        for x in range(x_min, x_max+1):
            if (x,y) in positions:
                tile = tiles[positions.index((x,y))]
                print(tile, end=" ")
            else:
                print("  ", end="")
        print("|")
        
    print("   |" + "".join(["_"]*(2*(x_max-(x_min-1))+1)) + "|")

def randomPlaceTiles(letters: List[str]) -> List[Tile]:
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
                tiles.append(Tile(letters[i], x, y))
                successful = True
    # plt.scatter(list(zip(*positions))[0], list(zip(*positions))[1])
    # plt.show()
    # print(positions)
    # print(list(zip(*positions))[0])
    return tiles