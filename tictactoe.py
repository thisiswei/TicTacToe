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
import copy 


"""
(0, 0)  |(0, 1)  |(0, 2)
_______________________
(1, 0)  |(1, 1)  |(1, 2)
_______________________
(2, 0)  |(2, 1)  |(2, 2)
"""

OTHER = {'X':'O', 'O':'X'} 
N = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
C = CORNERS = [(0, 0), (0, 2), (2, 0), (2, 2)]
OPPOSITE_CORNERS = dict((c1, c2) for c1, c2 in zip(C, C[::-1]))   
D = diagnals = [[[0, 0], [1, 1], [2, 2]], 
                [[0, 2], [1, 1], [2, 0]]]

SIDE = [(1, 2),(2, 1),(0, 1),(1, 0)] 

ALLPOS = list(itertools.product(range(3), range(3)))

def aboard():
    return [['_', '_', '_'] for i in range(3)]  

def isempty(sq):
    return sq == '_'

def transpose(board):
    return map(list, zip(*board))

def diags(board):
    ds = [board[i][j] for diag in D for i, j in diag]
    return [ds[:3], ds[3:]]

def hvd(board):    #horizontal, vertical, diagonal
    return [board, transpose(board), diags(board)]


def show(board):
    print ('\n_________\n'.join('  |'.join([N[i][j] if isempty(sq) else sq 
               for j, sq in enumerate(row)]) 
               for i, row in enumerate(board)))   

def newboard(board, i, j, role): 
    b = copy.deepcopy(board)
    b[i][j] = role
    return b

def checkboth(board, role, function=gotwinner, candidates=ALLPOS):
    position = find_spot(board, candidates, role, function)
    if position:
        return position
    # check if OTHER[role] have spots for winning, or two way.wining potential
    position = find_spot(board, candidates, OTHER[role], function)
    if position:
        return position

def find_spot(board, candidates, role, function):
    for i, j in candidates:
        if isempty(board[i][j]):
            b = newboard(board, i, j, role)
            if function(b, role, i, j): 
                return i, j

def gotwinner(board, role=None, i=None, j=None):
    for b in hvd(board):
        for row in b:
            if any(row.count(sq) == 3 for sq in 'XO'):
                return True
    return False

def gotfork(board, role, i, j): 
    tb = transpose(board)
    if board[i].count(role) == 2 and tb[i].count(role) == 2:
        return (board[i].count(OTHER[role]) == 0 and tb[i].count(OTHER[role]) == 0)

#) Opposite Corner: If the opponent is in the corner, play the opposite corner.  
#) Empty Corner: Play an empty corner.  
def gotcorner(board, role):
    empty_corners = []
    for i,j in CORNERS:
        if isempty(board[i][j]):
            x, y = OPPOSITE_CORNERS[(i, j)]
            if board[x][y] == OTHER[role]:  
                return i, j
            else:
                empty_corners.append((i, j))
    if not empty_corners:
        return 
    return empty_corners[0]

def aiplay(board, role):
    pos = checkboth(board, role) # 1) Win: If you have two in a row, play the third to get three in a row.  
    if pos:                      # 2) Block: If the opponent has two in a row, play the third to block them.  
        return pos
    pos = checkboth(board, role, gotfork) # 3, 4) place/block @ forkplace( win two way)
    if pos:
        return pos
    if isempty(board[1][1]): # 5) play at center if it's empty
        return 1, 1
    corner = gotcorner(board, role)  # 6, 7) place at opposite corner or just any corner
    if corner:
        return corner
    for i, j in SIDE:
        if isempty(board[i][j]):
            return i, j

def play():
    board, player, ai, turn, who = initial_setup()
    placed = 0
    show(board)
    while True:
        if ai == turn:
            i, j = aiplay(board, ai)
            board[i][j] = ai
                                         # [0, 0] => 1 [0, 1] => 2
            print '\n AI place at %s \n' % (i * 3 + 1 + j) 
        else:
            playerplay(board, player)
        show(board) 
        if gotwinner(board):
            print who[turn] + ' won'
            break
        placed += 1
        turn = OTHER[turn]
        if placed >= 8 and turn == player:
            print 'Tie'
            break

def initial_setup():
    player = 'w'
    while player not in 'XO':
        player = raw_input('choose x or o ? -->     ').upper()
    ai = OTHER[player]
    turn = random.choice('XO')
    who = {player: 'You', ai: 'AI' }
    board = aboard()
    return board, player, ai, turn, who

def playerplay(board, player):
    move = 0
    while not isillegal(move, board):
        try:
            move = int(raw_input('\n enter: spot(1-9) for %s  -> '% player))  
        except ValueError:
            continue 
    x, y = divmod(move-1, 3)   # 1-> [0, 0], 2 -> [0, 1]
    board[x][y] = player

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
