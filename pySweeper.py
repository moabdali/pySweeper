import random
import copy as cp
import string
from os import system, name



def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# the square can be changed to a class or dictionary in the future.  The list items below hold the
# corresponding data
# square = 0 = bomb (0 = safe, 1 = bomb), 1= top left, 2= top middle, 3 = top right, 4 = middle left,
#          5 = middle right, 6 = bottom left, 7 = bottom middle, 8 = bottom right,
#          9 = status (0 = unrevealed, 1 = revealed), 10 = number of bombs surrounding spot, 11=clear processed

def showBombMap(playingField):
    spacer = "  "
    print("  ", end="")
    for i in range (len(playingField[0])):
        print(f"{spacer}{i+1:2}",end="")
    print("")
    bombSymbol = " #"
    leftIndex = 1
    firstTime = True
    for r in range(rows):
        
        print(f"{leftIndex:2}:",end="")
        leftIndex+=1
        
        for c in range(columns):
            
            if playingField[r][c][0] == 1:
                print( f" {bombSymbol:2} ",end="")
                continue
            print(f" {playingField[r][c][10]:2} ",end="")
        
        print("")

    print("")


def revealer(playingField):
    
    change = True
    #technically the first change is a lie, but whatever
    while change:
        rows = len(playingField)
        columns = len(playingField[0])
        change = False
        for r in range(rows):
            
            for c in range(columns):
                
                #print(f"Processing ({r},{c})")
                #if the spot is processed already, check another spot
                
                if playingField[r][c][11] == 1:
                    continue
                
                #if a spot has been revealed and has zero bombs (and hasn't been fully processed yet):
                if playingField[r][c][9] == 1 and playingField[r][c][10]==0:
                    #print("marking as processed upper function")
                    playingField[r][c][11] = 1 #mark as processed
                    
                    #try top left
                    try:
                        #if the top left location has no bombs surrounding it and is a legal place to check and the location isn't processed yet
                        if playingField[r-1][c-1][10] == 0 and r-1 >= 0 and c-1 >= 0 and playingField[r-1][c-1][11] != 1:
                            #mark the location as revealed
                            playingField[r-1][c-1][9] = 1
                            #revealedSquares += 1
                            change = True
                            #print("Change in top left")
                            
                        #if it's not a 0 space, but it's also not a bomb:
                        elif playingField[r-1][c-1][0] == 0 and r-1 >= 0 and c-1 >= 0:
                            #reveal it
                            playingField[r-1][c-1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r-1][c-1][11] = 1
                            #print("revealing top left")
                            
                    except:
                        pass
                        
                    #try top middle:
                    try:
                        if playingField[r-1][c][10] == 0 and r-1>=0 and playingField[r-1][c][11] != 1:
                            playingField[r-1][c][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r-1][c][0] == 0 and r-1>=0:
                            #reveal it
                            playingField[r-1][c][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r-1][c][11] = 1
                            
                    except:
                        pass
                        
                    #try top right
                    try:
                        if playingField[r-1][c+1][10] == 0 and r-1 >=0 and playingField[r-1][c+1][11] != 1:
                            playingField[r-1][c+1][9]=1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r-1][c+1][0] == 0 and r-1 >=0:
                            #reveal it
                            playingField[r-1][c+1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r-1][c+1][11] = 1
                    except:
                        pass

                    #try left
                    try:
                        
                        if playingField[r][c-1][10] == 0 and c-1 >= 0 and playingField[r][c-1][11] != 1:
                            playingField[r][c-1][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r][c-1][0] == 0 and c-1 >= 0:
                            #reveal it
                            playingField[r][c-1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r][c-1][11] = 1
                    except:
                        pass

                    #try right
                    try:
                        if playingField[r][c+1][10] == 0 and playingField[r][c+1][11] != 1:
                            playingField[r][c+1][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r][c+1][0] == 0:
                            #reveal it
                            playingField[r][c+1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r][c+1][11] = 1
                    except:
                        pass



                    #try bottom left
                    try:
                        if playingField[r+1][c-1][10] == 0 and c-1 >= 0 and playingField[r+1][c-1][11] != 1:
                            playingField[r+1][c-1][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r+1][c-1][0] == 0 and c-1 >= 0:
                            #reveal it
                            playingField[r+1][c-1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r+1][c-1][11] = 1
                    except:
                        pass

                    #try bottom
                    try:
                        if playingField[r+1][c][10] == 0 and playingField[r+1][c][11] != 1:
                            playingField[r+1][c][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r+1][c][0] == 0:
                            #reveal it
                            playingField[r+1][c][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r+1][c][11] = 1
                    except:
                        pass

                    #try bottom right
                    try:
                        if playingField[r+1][c+1][10] == 0 and playingField[r+1][c+1][11] != 1:
                            playingField[r+1][c+1][9] = 1
                            #revealedSquares += 1
                            change = True
                        elif playingField[r+1][c+1][0] == 0:
                            #reveal it
                            playingField[r+1][c+1][9] = 1
                            #revealedSquares += 1
                            #mark it as processed
                            playingField[r+1][c+1][11] = 1
                    except:
                        pass
            
    
   






#columns = input("Columns? ")
#rows = input("Rows? ")

columns = 10
rows = 10

playingField = []

# the square can be changed to a class or dictionary in the future.  The list items below hold the
# corresponding data
# square = 0 = bomb (0 = safe, 1 = bomb), 1= top left, 2= top middle, 3 = top right, 4 = middle left,
#          5 = middle right, 6 = bottom left, 7 = bottom middle, 8 = bottom right,
#          9 = status (0 = unrevealed, 1 = revealed), 10 = number of bombs surrounding spot, 11=clear processed
square = [0,0,0,0,0,0,0,0,0,0,0,0]
mineRow = []

for i in range(columns):
    mineRow.append(cp.deepcopy(square))
    
for i in range(rows):
    playingField.append(cp.deepcopy(mineRow))


# how many mines there are; can be a user toggle option in the future
bombCount = 10
totalBombs = bombCount
#the generator below creates bombs, making sure to not duplicate them
while bombCount > 0:
    bombRow = random.randint(0,rows-1)
    bombColumn = random.randint(0,columns-1)
    
    if playingField[bombRow][bombColumn][0] == 1:
        #print("already bombed")
        continue

    elif playingField[bombRow][bombColumn][0] == 0:
        #print("laying mine")
        bombCount -= 1
        playingField[bombRow][bombColumn][0] = 1
        continue
    
    else:
        print("dire error!")
        quit


for r in range(rows):
    
    for c in range(columns):
        surrBombs = 0
        if playingField[r][c][0] == 1:
            #print("You're standing on a bomb.")
            continue
        #print(f"searching for bombs around ({r},{c})")
        #try top left
        try:
            if playingField[r-1][c-1][0] == 1 and r-1 >= 0 and c-1 >= 0:
                #print("I found a bomb top left")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        #try top middle:
        try:
            if playingField[r-1][c][0] == 1 and r-1>=0:
                #print("I found a bomb above")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        #try top right
        try:
            if playingField[r-1][c+1][0] == 1 and r-1 >=0:
                #print("I found a bomb top right")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try left
        try:
            if playingField[r][c-1][0] == 1 and c-1 >= 0:
                #print("I found a bomb left")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try right
        try:
            if playingField[r][c+1][0] == 1:
                #print("I found a bomb right")
                surrBombs += 1
        except:
            surrBombs = surrBombs



        #try bottom left
        try:
            if playingField[r+1][c-1][0] == 1 and c-1 >= 0:
                #print("I found a bomb bottom left")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try bottom
        try:
            if playingField[r+1][c][0] == 1:
                #print("I found a bomb bottom")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try bottom right
        try:
            if playingField[r+1][c+1][0] == 1:
                #print("I found a bomb bottom right")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        #print(f"I found {surrBombs} bombs")
        playingField[r][c][10]=surrBombs





dead = False
while True:
    clear()
    revealedSquares = 0
    if dead == True:
        showBombMap(playingField)
        input("Hit enter to quit")
        break

    




    

    
    spacer = "  "
    print("  ", end="")
    for i in range (len(playingField[0])):
        print(f"{spacer}{i+1:2}",end="")
    print("")
    bombSymbol = " #"
    leftIndex = 1
    firstTime = True


    unrevealedString = " ?"
    
    for r in range(rows):
        
        print(f"{leftIndex:2}:",end="")
        leftIndex+=1
        
        for c in range(columns):
            
            if playingField[r][c][9] == 1:
                revealedSquares+=1
                #print(f"revealedSquares is {revealedSquares}")
                print(f" {playingField[r][c][10]:2} ",end="")
                continue
            else:
                    print(f" {unrevealedString:2} ",end="")
        
        print("")
    print("")

    print(f"Uncovered squares: {revealedSquares}")
    print(f"Total spaces needing to be uncovered: {len(playingField)*len(playingField[0])-totalBombs}")
    print(f"Bombs: {totalBombs}")


    if revealedSquares == len(playingField)*len(playingField[0])-totalBombs:
        print("")
        print("You win.  Good job.")
        showBombMap(playingField)
        input("Hit enter to quit")
        break

    getInput = input("Type in your location doing row then column. For example, you can type 3 4. ")
    
    try:
        myList = getInput.split(" ")
        r = int(myList[0])-1
        c = int(myList[1])-1
    except:
        print("bad input")
        input("Press enter to continue")
        continue

    if r < 0 or r > rows-1 or c < 0 or c > columns -1:
        print("Out of bounds")
        continue
    
    if playingField[r][c][0] == 1:
        print("You dead!")
        input("Press enter to continue")
        dead = True
    else:
        if playingField[r][c][9]==1:
            print("You already revealed this spot.")
            input("Press enter to continue")
            continue
        else:
            playingField[r][c][9]=1



    revealer(playingField)


    
