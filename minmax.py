import random

other = dict(X='O', O='X') 

pick_your_move = 'pick your spot for %s (0-8)->  '
not_valid = 'not valid try again ->  %s'

horizontal = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
vertical   = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
diagonal   = [[0, 4, 8], [2, 4, 6]]
hvd  = horizontal + vertical + diagonal

def same_element(lst):
    return not lst or len(set(lst)) == 1

class Board:
    def __init__(self):
        self.element = ['_' for i in range(9)]

    def show(self):
        print ('\n'.join(
                   ' |'.join([str(i+j) if e == '_' else e 
                             for i, e in enumerate(self.element[j:j+3])])
                             for j in [0, 3, 6])) 
    def gotwinner(self):
        for seq in hvd:
            if self.element[seq[0]] != '_' and same_element([self.element[i] for i in seq]):
                return self.element[seq[0]]

    def emptyspots(self):
        return [pos for pos in range(9) if self.element[pos] == '_']

    def gameover(self):
        return self.gotwinner() or not self.emptyspots()

    def makemove(self, move, player):
        self.element[move] = player

    def undomove(self, move):
        self.makemove(move, '_')

def aiplay(board, player):
    board.show() 

    def score(winner):
        return 1 if winner == player else 0 if not winner else -1

    def move_score(move, turn=player):
        try:
            board.makemove(move, turn)
            if board.gameover():
                return score(board.gotwinner())
            possibie_scores = (move_score(nextmove, other[turn]) 
                                         for nextmove in board.emptyspots())
            if turn == player:
                minelement = 1
                for p in possibie_scores:
                    if p == -1:
                        return p
                    minelement = min(p, minelement)
                return minelement
            else:
                maxelement = -1
                for p in possibie_scores:
                    if p == 1:
                        return p
                    maxelement = max(p, maxelement)
                return maxelement
        finally:
            board.undomove(move)
    moves = [(move_score(move), move) for move in board.emptyspots()]
    topscore_move = sorted(moves)[-1][1]
    board.makemove(topscore_move, player)
    print "\nAI placed at %s" % topscore_move

def game(): 
    b = Board()
    human = raw_input('pick x or o ->    ').upper()
    playnext = random.choice('XO')
    movefirst = 'Your' if playnext == human else 'AI' 
    print '\n %s move first' % movefirst
    if movefirst == 'AI':
        print 'Calculating......\n'
    while True:
        if playnext == human:
            humanplay(b, human)
        else:
            aiplay(b, other[human])
        if b.gameover():
            break
        playnext = other[playnext]
    b.show()
    if b.gotwinner():
        print '\n you lost'
    else:
        print '\n tie'

def humanplay(board, player):
    board.show()
    move = int(raw_input(pick_your_move % player))
    while move not in board.emptyspots():
        move = int(raw_input(not_valid % player))
    board.makemove(move, player)    
    print '\n you placed at %s' % move


if __name__ == "__main__":
    game()






