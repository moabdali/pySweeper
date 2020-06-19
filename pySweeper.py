import random
import copy as cp

#columns = input("Columns? ")
#rows = input("Rows? ")

columns = 10
rows = 9

playingField = []

# the square can be changed to a class or dictionary in the future.  The list items below hold the
# corresponding data
# square = 0 = bomb (0 = safe, 1 = bomb), 1= top left, 2= top middle, 3 = top right, 4 = middle left,
#          5 = middle right, 6 = bottom left, 7 = bottom middle, 8 = bottom right,
#          9 = status (0 = unrevealed, 1 = revealed), 10 = number of bombs surrounding spot
square = [0,0,0,0,0,0,0,0,0,0,0,0]
mineRow = []

for i in range(columns):
    mineRow.append(cp.deepcopy(square))
    
for i in range(rows):
    playingField.append(cp.deepcopy(mineRow))

# debug: test minefield generation
for rrows in playingField:
    for ccolumns in rrows:
        print(f"{ccolumns[10]} ",end="")
    print("")
# end debug

# how many mines there are; can be a user toggle option in the future
bombCount = 10

#the generator below creates bombs, making sure to not duplicate them
while bombCount > 0:
    bombRow = random.randint(0,rows-1)
    bombColumn = random.randint(0,columns-1)
    print(bombRow,bombColumn)
    if playingField[bombRow][bombColumn][0] == 1:
        print("already bombed")
        continue

    elif playingField[bombRow][bombColumn][0] == 0:
        print("laying mine")
        bombCount -= 1
        playingField[bombRow][bombColumn][0] = 1
        continue
    
    else:
        print("dire error!")
        quit


#debug:  shows the developer the status of the bombs
for rrows in playingField:
    for ccolumns in rrows:
        if ccolumns[0] == 1:
            print(f" # ",end="")
        else:
            print(f" ? ",end="")
    print("")

# square = 0 = bomb (0 = safe, 1 = bomb), 1= top left, 2= top middle, 3 = top right, 4 = middle left,
#          5 = middle right, 6 = bottom left, 7 = bottom middle, 8 = bottom right,
#          9 = status (0 = unrevealed, 1 = revealed), 10 = number of bombs surrounding spot


for r in range(rows):
    
    for c in range(columns):
        surrBombs = 0
        if playingField[r][c][0] == 1:
            print("You're standing on a bomb.")
            continue
        print(f"searching for bombs around ({r},{c})")
        #try top left
        try:
            if playingField[r-1][c-1][0] == 1:
                print("I found a bomb top left")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        #try top middle:
        try:
            if playingField[r-1][c][0] == 1:
                print("I found a bomb above")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        #try top right
        try:
            if playingField[r-1][c+1][0] == 1:
                print("I found a bomb top right")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try left
        try:
            if playingField[r][c-1][0] == 1:
                print("I found a bomb left")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try right
        try:
            if playingField[r][c+1][0] == 1:
                print("I found a bomb right")
                surrBombs += 1
        except:
            surrBombs = surrBombs



        #try bottom left
        try:
            if playingField[r+1][c-1][0] == 1:
                print("I found a bomb bottom left")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try bottom
        try:
            if playingField[r+1][c][0] == 1:
                print("I found a bomb bottom")
                surrBombs += 1
        except:
            surrBombs = surrBombs

        #try bottom right
        try:
            if playingField[r+1][c+1][0] == 1:
                print("I found a bomb bottom right")
                surrBombs += 1
        except:
            surrBombs = surrBombs
            
        print(f"I found {surrBombs} bombs")
        playingField[r][c][10]=surrBombs





for r in range(rows):
   
    for c in range(columns):
        if playingField[r][c][0] == 1:
            print( " # ",end="")
            continue
        print(f" {playingField[r][c][10]} ",end="")
    print("")
