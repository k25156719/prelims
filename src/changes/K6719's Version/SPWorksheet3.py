# Skeleton Program for the AQA AS Summer 2026 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed using PyCharm Community Edition 2022

# K6719's version -- Worksheet 3 in progress (Startpoint SPWorksheet2.py)

# Version number 0.0.1

import random

TILE = "[X]"
NO_TILE = "[ ]"
ALLOWED_DIRECTIONS = [[1,0], [0, 1], [1, 1]] # w3q1) needed constant

Width = 4
Height = 4
Board = []

def ResetBoard(RandomOption):
    global Board
    Board = []
    for Row in range(Height):
        Board.append([])
        for Column in range(Width):
            if RandomOption:
                Board[Row].append(GetRandomTile())
            else:
                Board[Row].append(TILE)

def GetRandomTile():
    Rand = random.randint(1, 10)
    if Rand < 10:
        return TILE
    else:
        return NO_TILE

def DisplayState(PlayerNumber):
    print("-------------------------")
    print(f"Player {PlayerNumber}'s turn")
    print()
    DisplayBoard()

def DisplayBoard():
    print("  ", end='')
    for Column in range(Width):
        Header = chr(Column + 65)
        print(f"  {Header} ", end='')
    print()
    for Row in range(Height):
        print(Row + 1, end=" ")        
        for Column in range(Width):
            print(f" {Board[Row][Column]}", end='')
        print()

def ConvertRefToCoords(Ref):
    Column = ord(Ref[0]) - 65
    Row = int(Ref[1]) - 1

    # w2q5) explanation then code
    # Task 1
    # Column can easily be negative if a character under the character A is given
    # Row is only negative where Ref[1] is the character 0 (as this would lead to a value of -1)
    # The bounding is set by the dimensions above (global variables Width and Height)
    if (Column < 0 or Column >= Width) or (Row == -1 or Row >= Height):
        print("Out of bounds (or negative values calculated).")
        return [] # return an empty list and appropriate message printed
    # Task 1 end [coding end]

    if Row < Height and Column < Width:
        Coords = [Row, Column]
    else:
        Coords = []
    return Coords

def ConvertCoordsToRef(Row, Column):
    Ref = ""
    if Row < Height and Column < Width:        
        Letter = chr(Column + 65)
        Number = Row + 1
        Ref = Letter + str(Number)
    return Ref

def ProcessMove(Move):
    # w2q6) allow an option for X, do this at the start
    # scan from top to bottom then along rows for the first tile, remove it
    if Move == "X":
        tilesFound = 0

        for column in range(Width):
            for row in range(Height):
                # loop from TOP to BOTTOM
                if Board[row][column] == TILE:
                    Board[row][column] = NO_TILE
                    tilesFound += 1
                    break

            if tilesFound: # if a tile is found break out
                break

        print(f"{tilesFound} square(s) removed.")

        return True # break out of function

    # w3q1) diagonal movement notes
    # only allow southeast direction, and utilize the existing move check to actually
    # do this efficiently with less code
    # an idea is to actually generalize the move check with an integer direction

    if "-" in Move:
        DashPos = Move.index("-")
        FirstRef = Move[0:DashPos]
        SecondRef = Move[DashPos + 1:]
    else:
        FirstRef = Move
        SecondRef = Move
    StartCoords = ConvertRefToCoords(FirstRef)

    if StartCoords != []: # w2q5) QoL fix, prevents multiple prints of the same error.
        EndCoords = ConvertRefToCoords(SecondRef)
    else:
        return False # w2q5) may make the following code redundant?

    # w3q1) calculate directional movement
    DirectionVector = [EndCoords[0] - StartCoords[0], EndCoords[1] - StartCoords[1]]
    DirectionY = 1 if DirectionVector[0] > 0 else 0 if DirectionVector[0] == 0 else -1 # this has to be flipped
    DirectionX = 1 if DirectionVector[1] > 0 else 0 if DirectionVector[1] == 0 else -1
    DirectionVector = [DirectionX, DirectionY]

    # only allow Direction Vectors of [1,0], [0, -1] and [1, -1] as of w3q1

    SquaresRemoved = 0 # w2q2) variable set
    if len(StartCoords) == 0 or len(EndCoords) == 0:
        return False

    # w3q1) fix this selection to allow validation for diagonal directions.
    if DirectionVector not in ALLOWED_DIRECTIONS:
        return False

    if DirectionVector == ALLOWED_DIRECTIONS[0]: # w3q1) add our directions, and [0] is horizontal movement
        ToRemove = SquaresRemoved = EndCoords[1] - StartCoords[1] + 1
        # edit w2q2) set SquaresRemoved to same thing
        for Cell in range(StartCoords[1], EndCoords[1] + 1):
            if Board[StartCoords[0]][Cell] == TILE:
                ToRemove -= 1
        if ToRemove == 0:
            for Cell in range(StartCoords[1], EndCoords[1] + 1):
                Board[StartCoords[0]][Cell] = NO_TILE
        else:
            return False
    elif DirectionVector == ALLOWED_DIRECTIONS[1]: # w3q1) add directions, [1] is vertical downwards movement
        ToRemove = SquaresRemoved = EndCoords[0] - StartCoords[0] + 1
        # edit w2q2) set squaresRemoved to toRemove's old value to preserve it
        # .. as ToRemove becomes 0 over runtime

        for Cell in range(StartCoords[0], EndCoords[0] + 1):
            if Board[Cell][StartCoords[1]] == TILE:
                ToRemove -= 1
        if ToRemove == 0:
            for Cell in range(StartCoords[0], EndCoords[0] + 1):
                Board[Cell][StartCoords[1]] = NO_TILE
        else:
            return False
    elif DirectionVector == ALLOWED_DIRECTIONS[2]: # w3q1) add directions [2] allowing DIAGONAL SOUTHEAST movement
        # w3q1) preserve this, row difference is still the diagonal distance (squares needed to be removed)
        ToRemove = SquaresRemoved = EndCoords[0] - StartCoords[0] + 1

        # edit w2q2) set squaresRemoved to toRemove's old value to preserve it
        # .. as ToRemove becomes 0 over runtime

        # w3q1) this is a 1dim loop
        # Note: use squares removed to offset otherwise it will bug out
        for offset in range(0, SquaresRemoved):
            # w3q1) offset beginning coordinates)
            if Board[StartCoords[0] + offset][StartCoords[1] + offset] == TILE:
                ToRemove -= 1 # follow sameish algorithm for w3q1

        if ToRemove == 0:
            # w3q1) transition to this 1dim iteration to actually allow the diagonal iteration.
            for offset in range(0, SquaresRemoved):
                Board[StartCoords[0] + offset][StartCoords[1] + offset] = NO_TILE
        else:
            return False

    print(SquaresRemoved, "squares removed.")
    # edit w2q2) print out toRemove which stores the amount of squares removed

    return True

def SetBoardSize():
    global Width
    global Height
    Width = int(input("Specify board width: "))
    Height = int(input("Specify board height: "))

def DisplayMenu(RandomOption):
    print("1 - Start game")
    print(f"2 - Set board size (currently {Width} x {Height})")
    print(f"3 - Toggle random option (currently {RandomOption})")
    print("4 - Load test board (4 x 4)")
    print("9 - Quit")

def LoadTestBoard():
    global Width
    global Height
    Width = 4
    Height = 4
    ResetBoard(False)
    ProcessMove("A1-A4")
    ProcessMove("B1-B4")
    ProcessMove("C1-C4")
    ProcessMove("D1-D2")

def CheckGameOver():
    Remaining = 0
    for Row in range(Height):
        for Column in range(Width):
            if Board[Row][Column] == TILE:
                Remaining += 1
    if Remaining == 1:
        return True
    else:
        return False

def PlayGame():
    print(f"Valid moves are within the range A1-{ConvertCoordsToRef(Height - 1, Width - 1)}")
    GameOver = False
    NextPlayer = 1
    while not GameOver:
        DisplayState(NextPlayer)
        print()
        IsValid = False
        while not IsValid:
            Move = input("Enter move: ").upper() # edit w2q1) uppercase input to allow leniency
            IsValid = ProcessMove(Move)
            if not IsValid:
                print("Not a valid move - try again")
        NextPlayer = NextPlayer % 2 + 1
        if CheckGameOver():
            GameOver = True
            print(f"Game over - player {NextPlayer % 2 + 1} wins")
            print()
            DisplayBoard()
            print()
            print("Press enter to continue")
            input()

def Main():
    Playing = True
    RandomOption = True # w2q3) set randomOption to True on default
    while Playing:
        ExitMenu = False
        while not ExitMenu:
            print()
            DisplayMenu(RandomOption)

            # w2q4) encapsulate in try except
            try:
                UserInput = int(input("Enter a choice: "))
            except ValueError: # NOTE: int returns a ValueError upon not working properly.
                print("Invalid choice.")
                continue # continue to avoid the if statements (performance, not necessary)
            # w2q4 end

            if UserInput == 1:
                ExitMenu = True
                ResetBoard(RandomOption)
            elif UserInput == 2:
                SetBoardSize()
            elif UserInput == 3:
                RandomOption = not RandomOption
            elif UserInput == 4:
                ExitMenu = True
                LoadTestBoard()
            elif UserInput == 9:
                print("Thank you for playing")
                ExitMenu = True
                Playing = False
            else:
                print("Invalid choice.")
        if Playing:
            PlayGame()
    print("Press enter to continue")
    input()

if __name__ == "__main__":
    Main()
