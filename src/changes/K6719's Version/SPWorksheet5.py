# Skeleton Program for the AQA AS Summer 2026 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed using PyCharm Community Edition 2022

# K6719's version -- Worksheet 5 in progress (Startpoint SPWorksheet4.py -- Q1)

# Version number 0.0.1

import random

TILE = "[X]"
NO_TILE = "[ ]"
ALLOWED_DIRECTIONS = [[1,0], [0, 1], [1, 1], [0,0]] # w3q1) needed constant

Width = 4
Height = 4
Board = []

#w3q2) create global field NumPlayers
NumberOfPlayers = 2

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

# w5q1) count the tiles
def CountTilesOnBoard():
    global Board
    Count = 0
    for Row in range(Height):
        for Column in range(Width):
            Count += 1 if Board[Row][Column] == TILE else 0

    return Count

# w4q1) saveGame structure -- note additional feature added for multiple players as extension of
# w3q2
def SaveGame(Moves, ToFile="./default.txt"):
    global Board, NumberOfPlayers
    Metadata = f"{Width},{Height},{NumberOfPlayers}" # w4q1) e.g. 2/5/3

    Body = "\n" # w4q1) main data
    for Move in Moves:
        Body += Move + "\n"

    # write into file
    with open(ToFile, "w+") as writer:
        writer.write(Metadata + Body)
        writer.close()


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
    if FirstRef == SecondRef: # W3) minor edit global, js to allow single letter inputs
        if Board[StartCoords[0]][StartCoords[1]] == TILE:
            Board[StartCoords[0]][StartCoords[1]] = NO_TILE

            SquaresRemoved = 1
        else:
            return False

    print(SquaresRemoved, "squares removed.")
    # edit w2q2) print out toRemove which stores the amount of squares removed

    return True

#w3q2) setNumberOfPlayers subroutine, REMEMBER THE VALIDATION
def SetNumberOfPlayers():
    global NumberOfPlayers

    # w3q2) success flag is NOT returned, no edit
    try:
        TrialValue = int(input("Specify number of players (>=2): "))

        if TrialValue < 2: #w3q2) bound it to >2
            print("Please enter a value above or equal to 2.")
        else:
            NumberOfPlayers = TrialValue
    except:
        print("Please enter a valid integer.")

def SetBoardSize():
    global Width
    global Height

    Validated = False

    while not (2 <= Width <= 9 and 2 <= Height <= 9 and Validated): #w3q4) conditions
        print("Please enter two numbers between 2 and 9.")
        try:
            Width = int(input("Specify board width: "))
            Height = int(input("Specify board height: "))

            Validated = 2 <= Width <= 9 and 2 <= Height <= 9
        except:
            print("Please enter valid integers for both fields.")
            continue # w3q3) continue if non-integer

# w3q3) display statistics subroutine
def DisplayStatistics(Moves):
    SquaresTotal = Width * Height # w3q3) no need to iterate for this
    SquaresActive = 0 # w3q3) count these squares

    for x in range(Width):
        for y in range(Height):
            SquaresActive += 1 if Board[y][x] == TILE else 0

    print(f"Tiles left / Total tiles: {SquaresActive}/{SquaresTotal}")
    print(f"Total moves so far: {Moves}")

def DisplayMenu(RandomOption):
    print("1 - Start game")
    print(f"2 - Set board size (currently {Width} x {Height})")
    print(f"3 - Toggle random option (currently {RandomOption})")
    print("4 - Load test board (4 x 4)")
    # w3q2) add new display option
    print(f"5 - Set number of players (currently {NumberOfPlayers})")
    # w4q1) i dont care aqa 6 is fine
    print(f"6 - Load a game from a file.")
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

# w4q1) stay here because we need alot of these subroutines
def LoadAndPlayGame(RandomOption = True):
    global Board, Width, Height, NumberOfPlayers

    FileName = input("Please give the path to the file that needs to be read from: ")

    try:
        FileOutput = "" # w4q1) store files here.
        with open(FileName, "r") as file:
            FileOutput = file.readlines()
            file.close()
        if isinstance(FileOutput, str):  # w4q1) validate
            print("Failed at reading the file somehow??")

        Metadata = list(map(
            int, FileOutput.pop(0).split(",")
        ))  # w4q1) read metadata

        Width, Height, NumberOfPlayers = Metadata[0], Metadata[1], Metadata[2]  # unpack values
    except IOError: # w4q1) more validations
        print("Errors in reading the actual file. Defaulting to 4x4 2p.")

        Width, Height, NumberOfPlayers = 4, 4, 2

    # w4q1) add validations
    if not (2 <= Width <= 9 and 2 <= Height <= 9) or not (NumberOfPlayers > 1):
        print("This file is invalid. Resetting to default 4x4 2p.")
        Width, Height, NumberOfPlayers = 4, 4, 2

    ResetBoard(RandomOption) # w4q1) utilize preexisting sub to reset the board

    CurrentPlayer = 0

    for Move in range(0, len(FileOutput)):
        ProcessMove(FileOutput[Move]) # w4q1) process each move

        # w4q1) calculate current player with modulus
        CurrentPlayer += 1
        CurrentPlayer %= NumberOfPlayers

    return CurrentPlayer


def PlayGame(NextPlayer="in"):
    print(f"Valid moves are within the range A1-{ConvertCoordsToRef(Height - 1, Width - 1)}")
    GameOver = False

    # w4q1) loop to validate
    if NextPlayer == "in" or not isinstance(NextPlayer, int): # w4q1) check is desired type
        while True:
            NextPlayer = int(input(f"Which player should start (1 to {NumberOfPlayers}): "))
            if 1 <= NextPlayer <= NumberOfPlayers:
                break
            else:
                print(f"Please enter a number between 1 and {NumberOfPlayers}")
    else:
        if not 1 <= NextPlayer <= NumberOfPlayers:
            NextPlayer = 1 # w4q1) default to 1 if invalid

    # w3q3) add move counter
    Moves = 0
    MoveList=[]
    while not GameOver:
        DisplayState(NextPlayer)
        print()
        IsValid = False
        while not IsValid:
            Move = input("Enter move: ").upper() # edit w2q1) uppercase input to allow leniency
            IsValid = ProcessMove(Move)
            if not IsValid:
                print("Not a valid move - try again")
            else:
                MoveList.append(Move) # w4q1) add the log.

        Moves += 1 # w3q3) increment

        DisplayStatistics(Moves) # w3q3) BEFORE wincheck
        NextPlayer = NextPlayer % NumberOfPlayers + 1 # w3q2) simply replace modulus
        if CheckGameOver():
            GameOver = True
            print(f"Game over - player {(NextPlayer - 1) % NumberOfPlayers} wins") #w3q2) same thing
            print()
            DisplayBoard()
            print()
            print("Press enter to continue")
            input()

        # w4q1) add save game option
        # also make sure this is defaulted so u can save after the game ends as well
        SaveOption = input(f"Would you like to save the game in its current state? (y/n): ").lower()

        if SaveOption == "y":
            SaveGame(MoveList, input("Where should I store it? (filename.ext / full path): "))
        elif SaveOption not in ["n" or "y"]:
            print("Do you actually think youre tough bro.")

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
            elif UserInput == 5:
                SetNumberOfPlayers()
            elif UserInput == 6: # w4q1) add new option
                ExitMenu = True
                NextPlayer = LoadAndPlayGame(RandomOption)
                PlayGame(NextPlayer) # w4q1) note the new input
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
