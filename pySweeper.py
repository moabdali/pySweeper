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