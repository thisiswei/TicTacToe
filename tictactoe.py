"""
1) Win: If you have two in a row, play the third to get three in a row.  
2) Block: If the opponent has two in a row, play the third to block them.  
3) Fork: Create an opportunity where you can win in two ways.
4) Block Opponent's Fork: 
5) Center: Play the center.  
6) Opposite Corner: If the opponent is in the corner, play the opposite corner.  
7) Empty Corner: Play an empty corner.  
8) Empty Side: Play an empty side.
"""                               
import random
import itertools
import copy as c

R = range(3)
other = {'X':'O', 'O':'X'} 
numstr = ['1 2 3', '4 5 6', '7 8 9'] 
N = map(str.split, numstr)     # [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]

center = [1, 1] 
C = [[0, 0], [2, 2], [0, 2], [2, 0]]    #corners
D = [[C[0], center, C[1]], [C[2], center, C[-1]]]  # diagnals [[0,0],[1,1],[2,2],] [[0,2],[1,1],[2,0]] 
leftover = [[1, 2],[2, 1],[0, 1],[1, 0]]

ocorners = dict((tuple(c1), c2)      #opposite corners
                 for c1, c2 in zip(C, [C[i] for i in [1, 0, 3, 2]]))

ALLPOS = list(itertools.product(R, R))

def aboard():
    return [['_', '_', '_'] for i in R]  

def isempty(sq):
    return sq == '_'

def transpose(board):
    return map(list, zip(*board))

def diags(board):
    ds = [board[i][j] for diag in D for [i, j] in diag]
    return [ds[:3], ds[3:]]

def hvd(board):    #horizontal, vertical, diagonal
    return [board, transpose(board), diags(board)]

def gotwinner(board, role=None, i=None, j=None):
    for b in hvd(board):
        for row in b:
            if any(row.count(sq) == 3 for sq in 'XO'):
                return True
    return False

def show(board):
    print ('\n_________\n'.join(' | '.join([N[i][j] if isempty(sq) else sq 
               for j, sq in enumerate(row)]) 
               for i, row in enumerate(board)))   

def newboard(board, i, j, role): 
    b = c.deepcopy(board)
    b[i][j] = role
    return b

def aiplay(board, role):
    pos = checkboth(board, role) # 1,2) win or block 
    if pos:
        return pos 
    pos = checkboth(board, role, gotfork) 
    if pos:
        return pos                       # 3, 4) place/block @ forkplace( win two way)
    if isempty(board[1][1]): 
        return center                     # 5) 
    corner = checkboth(board, role, gotcorner, C, True)    
    if corner:
        return corner                      # 6, 7) place at opposite corner or just any corner
    for i, j in leftover:
        if isempty(board[i][j]):
            return i, j 

def checkboth(board, role, function=gotwinner, candidates=ALLPOS, oneround=False):
    for i, j in candidates:
        if isempty(board[i][j]):
            b = newboard(board, i, j, role)
            if function(b, role, i, j): 
                return i, j
        if oneround: break

    for i, j in candidates:
        if isempty(board[i][j]):
            b = newboard(board, i, j, other[role])
            if function(b, role, i, j): 
                return i, j 

def gotfork(board, role, i, j): 
    tb = transpose(board)
    if board[i].count(role) == 2 and tb[i].count(role) == 2:
        return (board[i].count(other[role]) == 0 and tb[i].count(other[role]) == 0)

# C = corners = [[0, 0], [2, 2], [0, 2], [2, 0]]    
def gotcorner(board, role, i, j):
    cors = []
    x, y = ocorners[(i, j)]
    if board[x][y] == other[role]:  # if corner opposite is opponent
        return i, j
    else: 
        cors.append((i, j))
    if not cors: return
    return cors[0]
    
def play():
    board = aboard()
    player = 'w'
    while player not in 'XO':
        player = raw_input('choose x or o ? -->     ').upper()
    ai = other[player]
    turn = random.choice('XO')
    if turn == player:
        show(board)
    over = False
    who = {player: 'You', ai: 'AI' }
    placed = 0
    while not over:
        if ai == turn:
            i, j = aiplay(board, ai)
            board[i][j] = ai
            pos = i * 3 + 1 + j    # [0, 0] => 1 [0, 1] => 2   
            print '\n AI place at %s \n' % pos
        else:
            move = 0
            while not isillegal(move, board):
                try:
                    move = int(raw_input('\n enter: to spot(1-9) for %s  -> '% player))  
                except ValueError:
                    continue

            x, y = divmod(move-1, 3)   # 1-> [0, 0], 2 -> [0, 1]
            board[x][y] = player       
        show(board)                       
        over = gotwinner(board)
        if over:
            print who[turn] + ' won'
            break
        placed += 1 
        turn = other[turn]    
        if placed >= 8 and turn==player: 
            print 'Tie'
            break 
        

def isillegal(move, board):
    if not (isinstance(move, int) and move in range(1, 10)):
        return
    i, j = divmod(move-1, 3)   # 1-> [0, 0], 2 -> [0, 1]
    try:
        sq = board[i][j]     
    except IndexError:
        return False
    return isempty(sq)    

     
play()
