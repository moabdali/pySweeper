import PySimpleGUI as sg
import random
import copy as cp
import string
import os



# for clearing the screen between moves and messages
def clear():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


# reveal the entire map (for when you win/lose - to show that the map wasn't cheating, but also useful for showing the map for debug purposes)
def showBombMap(playBoard):
    spacer = "  "
    print("  ", end="")
    for i in range(len(playingField[0])):
        print(f"{spacer}{i+1:2}", end="")
    print("")
    bombSymbol = " #"
    leftIndex = 1
    for r in range(rows):
        print(f"{leftIndex:2}:", end="")
        leftIndex += 1

        for c in range(columns):

            if playingField[r][c][bombExists] == 1:
                playBoard[r,c].update(image_filename=".\\tileImages\\bomb.png")
                print(f" {bombSymbol:2} ", end="")
                continue
            print(f" {playingField[r][c][surroundingBombs]:2} ", end="")
            number = playingField[r][c][surroundingBombs]
            playBoard[r,c].update(image_filename=(imageAddress(number,"revealed")))
        print("")
    print("")


# cascade function - if you reveal a square with 0, that means all surrounding locations are safe, so automatically show them.  If any of THOSE are zero, keep repeating until
# no further zero squares are encountered
def revealer(playingField):
    change = True
    # technically the first change is a lie, but whatever
    while change:
        rows = len(playingField)
        columns = len(playingField[0])
        change = False
        for r in range(rows):

            for c in range(columns):

                # if the spot is processed already, check another spot

                if playingField[r][c][squareProcessed] == 1:
                    continue

                # if a spot has been revealed and has zero bombs (and hasn't been fully processed yet):
                if (
                    playingField[r][c][bombStatus] == 1
                    and playingField[r][c][surroundingBombs] == 0
                ):
                    # print("marking as processed upper function")
                    playingField[r][c][squareProcessed] = 1  # mark as processed

                    # try top middle:
                    try:
                        if (
                            playingField[r - 1][c][surroundingBombs] == 0
                            and r - 1 >= 0
                            and playingField[r - 1][c][squareProcessed] != 1
                        ):
                            playingField[r - 1][c][bombStatus] = 1
                            # revealedSquares += 1
                            change = True
                        elif playingField[r - 1][c][bombExists] == 0 and r - 1 >= 0:
                            # reveal it
                            playingField[r - 1][c][bombStatus] = 1
                            # revealedSquares += 1
                            # mark it as processed
                            playingField[r - 1][c][squareProcessed] = 1

                    except:
                        pass


                    # try left
                    try:

                        if (
                            playingField[r][c - 1][surroundingBombs] == 0
                            and c - 1 >= 0
                            and playingField[r][c - 1][squareProcessed] != 1
                        ):
                            playingField[r][c - 1][bombStatus] = 1
                            # revealedSquares += 1
                            change = True
                        elif playingField[r][c - 1][bombExists] == 0 and c - 1 >= 0:
                            # reveal it
                            playingField[r][c - 1][bombStatus] = 1
                            # revealedSquares += 1
                            # mark it as processed
                            playingField[r][c - 1][squareProcessed] = 1
                    except:
                        pass

                    # try right
                    try:
                        if (
                            playingField[r][c + 1][surroundingBombs] == 0
                            and playingField[r][c + 1][squareProcessed] != 1
                        ):
                            playingField[r][c + 1][bombStatus] = 1
                            # revealedSquares += 1
                            change = True
                        elif playingField[r][c + 1][bombExists] == 0:
                            # reveal it
                            playingField[r][c + 1][bombStatus] = 1
                            # revealedSquares += 1
                            # mark it as processed
                            playingField[r][c + 1][squareProcessed] = 1
                    except:
                        pass


                    # try bottom
                    try:
                        if (
                            playingField[r + 1][c][surroundingBombs] == 0
                            and playingField[r + 1][c][squareProcessed] != 1
                        ):
                            playingField[r + 1][c][bombStatus] = 1
                            # revealedSquares += 1
                            change = True
                        elif playingField[r + 1][c][bombExists] == 0:
                            # reveal it
                            playingField[r + 1][c][bombStatus] = 1
                            # revealedSquares += 1
                            # mark it as processed
                            playingField[r + 1][c][squareProcessed] = 1
                    except:
                        pass


def imageAddress(number,status):
    if number == 0 and status == "revealed":
        return ".\\tileImages\\safe.png"
    elif number >0 and number <9 and status == "revealed":
        return f".\\tileImages\\{number}.png"
    elif status == "unrevealed":
        return f".\\tileImages\\unrevealed.png"



# execution begins here
columns = 10
rows = 10

playingField = []


# The square is essentially like an object to represent each square on the field.  Each of the four entries in the list corresponds, in order, to whether the bommb
# exists, whether the square has been revealed, how many bombs there are, and whether the square was processed for the automatic cascade function that will reveal
# all the squares around an empty square (and also continue this each time a new zero square is encountered during that reveal cycle)
square = [0, 0, 0, 0]
mineRow = []

# keys for square
bombExists = 0
bombStatus = 1
surroundingBombs = 2
squareProcessed = 3


# Python doesn't actually duplicate lists, so I'm doing a deep copy, which creates a real copy of the list instead of passing its address.  If you don't
# do a deepcopy, any changes to one list will affect all copies of the list.  We want the lists to be independent.  The first loop creates a single
# mine field lane.  The second one duplicates the empty lane to create the required number of rows.
for i in range(columns):
    mineRow.append(cp.deepcopy(square))
for i in range(rows):
    playingField.append(cp.deepcopy(mineRow))


# how many mines there are; can be a user toggle option in the future
bombCount = 10
totalBombs = bombCount
# the generator below creates bombs, making sure to not duplicate them
while bombCount > 0:
    bombRow = random.randint(0, rows - 1)
    bombColumn = random.randint(0, columns - 1)

    # if there's a bomb here already, try a new location
    if playingField[bombRow][bombColumn][bombExists] == 1:
        continue

    # if there isn't a bomb here, go ahead and drop one
    elif playingField[bombRow][bombColumn][bombExists] == 0:
        bombCount -= 1
        playingField[bombRow][bombColumn][bombExists] = 1
        continue
    # this shouldn't ever show, but just to be safe in case it does happen, we'll exit the game instead of letting it loop forever
    else:
        print("dire error!  This should never show.")
        quit


# determines how many bombs surround a location and appends it to the respective square entry
for r in range(rows):

    for c in range(columns):

        surrBombs = 0

        # if there's a bomb on the current location, then we know not to reveal the location, nor do we put a number here so we're just going to skip it
        if playingField[r][c][bombExists] == 1:
            continue

        # try top left
        try:
            if (
                playingField[r - 1][c - 1][bombExists] == 1
                and r - 1 >= 0
                and c - 1 >= 0
            ):
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try top middle:
        try:
            if playingField[r - 1][c][bombExists] == 1 and r - 1 >= 0:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try top right
        try:
            if playingField[r - 1][c + 1][bombExists] == 1 and r - 1 >= 0:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try left
        try:
            if playingField[r][c - 1][bombExists] == 1 and c - 1 >= 0:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try right
        try:
            if playingField[r][c + 1][bombExists] == 1:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try bottom left
        try:
            if playingField[r + 1][c - 1][bombExists] == 1 and c - 1 >= 0:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try bottom
        try:
            if playingField[r + 1][c][bombExists] == 1:
                surrBombs += 1
        except:
            surrBombs = surrBombs

        # try bottom right
        try:
            if playingField[r + 1][c + 1][bombExists] == 1:
                surrBombs += 1
        except:
            surrBombs = surrBombs
        playingField[r][c][surroundingBombs] = surrBombs
        
# create the window

image = ".\\tileImages\\blank.png"
layout = [ [sg.T("pySweeper!",font = "Calibri 30")] ]
layout += [ [sg.Radio("Normal Mode","flagMode",default = True)],[sg.Radio("Flag Mode","flagMode")],[sg.Radio("Remove Flag Mode","flagMode")]]
layout += [ [sg.Button( "Help" ), sg.Button( "Stats" )] ]
layout += [ [sg.Button( image_filename=image,key = (i,j),pad=(1,1),border_width=2,size=(4,2),) for j in range (rows)] for i in range (columns) ]
playBoard = sg.Window("Connect X",layout,keep_on_top=True).Finalize()



# assume the player isn't dead
dead = False

# while the player hasn't died or won
while True:
    
    playBoard.refresh()
    # clear the screen
    clear()
    # assume no squares were revealed yet (there's a function that prefers this value stays at zero since it needs to recheck every turn)
    revealedSquares = 0

    # if you died
    if dead == True:
        showBombMap(playBoard)
        sg.popup("Hit ok to continue",keep_on_top=True, grab_anywhere=True)
        os.execv("pysweeper.py",("","./pysweeper.py"))
        break

    # spacer is used to align the playing field display
    spacer = "  "
    print("  ", end="")
    for i in range(len(playingField[0])):
        print(f"{spacer}{i+1:2}", end="")
    print("")
    
    #show window
    playBoard.refresh()
    # bombflag is the symbol we're using to show flag; it can be changed to whatever you want to use
    bombFlag = " B"
    # left index used to label the rows on the playing field display
    leftIndex = 1

    # unrevealed string is what you want unknown squares to look like
    unrevealedString = " ?"

    # print the playing field
    for r in range(rows):

        print(f"{leftIndex:2}:", end="")
        leftIndex += 1

        for c in range(columns):
            # if the location has been revealed, show it.  Overrides bomb flag
            if playingField[r][c][bombStatus] == 1:
                revealedSquares += 1
                print(f" {playingField[r][c][surroundingBombs]:2} ", end="")

                #send number and safety
                playBoard[r,c].Update(image_filename=imageAddress( playingField[r][c][surroundingBombs], "revealed"  ))
                
                continue
            else:
                # if you put a flag down and it hasn't been revealed, show a flag
                if playingField[r][c][squareProcessed] == 1:

                    
                    
                    print(f" {bombFlag:2} ", end="")
                # if there's no flag, then show the unrevealed square character
                else:
                    playBoard[r,c].Update(image_filename=imageAddress( playingField[r][c][surroundingBombs], "unrevealed"  ))
                    print(f" {unrevealedString:2} ", end="")

        print("")
    print("")

    # reset the "attempting to put a flag down" /"attempting to remove flag" variable
    flagAttempt = False
    flagRemoveAttempt = False

    # if you win, good job
    if revealedSquares == len(playingField) * len(playingField[0]) - totalBombs:
        print("")
        print("You win.  Good job.")
        showBombMap(playingField)
        sg.popup("Click ok to restart",keep_on_top=True)
        os.execv("pysweeper.py",("","./pysweeper.py"))
        break

    playBoard[0].update(True)
    event, values = playBoard.read()
    print(event, values)

    if event == "Help":
        sg.popup("""  Click a square to set up a mine detector in that
If there is a mine on that spot, you will instantly explode. That's bad.

If there is no mine there, you will be told how many mines touch that square
in any 8 of the surrounding spots touching that box. For example, revealing
an 8 means there's a bomb on all 8 surrounding squares.  A 3 would mean there's
three mines in total.
        
You also have the option to place down lightweight flags that help you keep track
of where you think a mine might be. These flags serve only as a visual tool for
yourself; they have no effect on anything else (and will automatically be removed
if the game determines that the spot was supposed to be revealed.  You can add a
flag by choosing Flag Mode, and then clicking the unchecked tile you want to place
it on.

To remove a flag that you placed down, chose the remove flag mode option, and then
click on the flag you want to remove.
        
Finally, you can click STATS to see how many bombs there are, how many spaces you've
safely uncovered, and how many more spaces you need to uncover to win.""",keep_on_top=True)
        continue
    if event == "Stats":
        sg.popup( f"Uncovered squares: {revealedSquares}\nRemaining squares to be uncovered: {len(playingField)*len(playingField[0])-totalBombs-revealedSquares}\nBombs: {totalBombs}",keep_on_top = True)
        continue
    
    if values[1] == True:
        flagAttempt = True
        string = "b"
        print("adding flag")
    elif values[2] == True:
        flagRemoveAttempt = True
        string = "c"
        print("removing Flag")
    else:
        string = None
    r = event[0]+1
    c = event[1]+1
    print(r,c)
    # get the user input; main interactive part of the game
    #getInput = input("Enter your row and column.  Type ? for more detailed help.\n>> ")
    if string == None:
        getInput = (str(r)+" "+str(c))
    else:
        getInput = (str(r)+" "+str(c)+" "+string)
    # if the user asks for help, explain the game
    if getInput == "?":
        print(
            """            Enter a row followed by a column, then hit enter to set up a mine
            detector in that location. For example, 3 4 will set up a detector
            on the third row from the top, fourth column from the left. If there
            is a mine on that spot, you will instantly explode.  If there is no
            mine there, you will be told how many mines touch that square in any
            8 of the surrounding spots touching that box. For example, revealing
            an 8 means there's a bomb on all 8 surrounding squares.  A 3 would
            mean there's three mines in total.

            You also have the option to place down lightweight flags that help
            you keep track of where you think a mine might be.  These flags
            serve only as a visual tool for yourself; they have no effect
            on anything else (and will automatically be removed if the game
            determines that the spot was supposed to be revealed.  You can add a
            flag by adding the letter b after your coordinates to designate you
            want to place a bomb flag there.  For example, to set a bomb flag on
            the top left, just type 1 1 b and then hit enter.  To remove a flag
            that you placed down, type the location and then follow it with
            a c to show you want to remove it.  For example, 1 1 c

            Finally, you can type the word STATS and then hit enter to see how
            many bombs there are, how many spaces you've safely uncovered, and
            how many more spaces you need to uncover to win."""
        )
        input("Hit enter to continue")
        clear()
        continue

    # show the stats if they type STATS or stats
    if getInput == "STATS" or getInput == "stats":
        print(f"Uncovered squares: {revealedSquares}")
        print(
            f"Remaining squares to be uncovered: {len(playingField)*len(playingField[0])-totalBombs-revealedSquares}"
        )
        print(f"Bombs: {totalBombs}")
        input("Hit enter to continue")
        continue

    # attempt to read the player's input
    try:

        # attempt to save the input as a row and column
        print(getInput)
        myList = getInput.split(" ")
        # converts the string to a number that is one less than what they typed.  This makes it to where they don't have to deal with
        # using 0 for row 1 and makes it more user friendly.  The rest of the program can be written in "programmer" language without
        # any hassle.
        r = int(myList[0]) - 1
        c = int(myList[1]) - 1
        try:
            # see if they attempted to give a third argument
            b = myList[2]
            # set flags for "bomb flag" if they typed b or B; same corresponding logic for c below
            if b == "b" or b == "B":
                flagAttempt = True
                # the line below is necessary to avoid keeping the flag variable in emory for all future attempts
                # if you don't have this here, it'll store the b in the list and will only place down flags instead
                # of attempting to reveal the square
                myList[2] = False
            elif b == "c" or b == "C":
                flagRemoveAttempt = True
                myList[2] = False
            # catch all for a third value not being b or c
            else:
                print("Your third value must be either b for bomb or c for clear")
                input("Hit enter to continue")
                continue
        # if they didn't give a third value, that's fine.  It's not an actual error
        except:
            pass
    # if you didn't feed two or three arguments, then that's bad.  Try again
    except:
        
        print("bad input")
        continue
    # you can't have values that don't fit within the number or rows or columns
    if r < 0 or r > rows - 1 or c < 0 or c > columns - 1:
        print("Out of bounds")
        continue
    
    if flagAttempt == True:
        # if you haven't revealed it yet
        if playingField[r][c][bombStatus] != 1:
            # place a bomb flag to note there may be a bomb
            playingField[r][c][squareProcessed] = 1
            playBoard[r,c].update(image_filename=".\\tileImages\\flag.png")
            print(
                "Placed a flag down.  Marked potential bomb with a B.  You may remove the flag by typing the location followed by c"
            )
            
            continue
        else:
            sg.popup("You can't place a flag in a revealed location.",keep_on_top=True)
            continue
    if flagRemoveAttempt == True:
        if playingField[r][c][squareProcessed] == 1:
            # remove bomb flag
            playingField[r][c][squareProcessed] = 0
            sg.popup("Removed the bomb marker",keep_on_top=True)
            
            continue
        else:
            sg.popup("There's no flag there.",keep_on_top=True)
            
            continue
    
        
    if playingField[r][c][bombExists] == 1:
        sg.popup("You dead!",keep_on_top=True)
        dead = True
    # kind of a pointless message, but there might be a confused person that keeps trying to reveal a spot for whatever reason. Can also act as a
    # debug message in a cinch in case a spot says it's been revealed, but hasn't (luckily this hasn't happened in testing yet)
    else:
        if playingField[r][c][bombStatus] == 1:
            sg.popup("You already revealed this spot.",keep_on_top=True)
            #input("Press enter to continue")
            continue
        elif playingField[r][c][squareProcessed] == 1:
            sg.popup("There's a flag there.  Remove it first.",keep_on_top=True)
            continue
        else:
            playingField[r][c][bombStatus] = 1

    revealer(playingField)
