"""An implementation of the game of hex
Turns the hexagonal grid into a rectangular one with squares being "adjacent" if they are
adjacent in the grid or are diagonally adjacent across the top-left to bottom-right diagonal"""

class Node():
    """Basic node class"""
    def __init__(self):
        self.connections=[]
        self.position=None


class Game():
    """Game class. This class creates the board and runs the game."""
    def __init__(self, size, board=None, values=None,upper_pseudo=None, lower_pseudo=None,\
                  left_pseudo=None, right_pseudo=None, avail_moves=[],player=1):
        self.size=size
        if board is None:
            self.avail_moves=[]
            self.make_board()
        else:
            self.board=board
            self.values=[x[:] for x in values]
            self.upper_pseudo=upper_pseudo
            self.lower_pseudo=lower_pseudo
            self.left_pseudo=left_pseudo
            self.right_pseudo=right_pseudo
            self.avail_moves=avail_moves[:]
        self.player=player #player 1 or 2
        self._compute_hash()

    def make_board(self):
        #Define the pseudo-nodes (edges)
        #Belong to p1:
        self.upper_pseudo=Node()
        self.lower_pseudo=Node()
        #Belong to p2:
        self.left_pseudo=Node()
        self.right_pseudo=Node()
        self.board=[[]]
        self.values=[[0]*(self.size+1) for i in range(self.size+1)]
        for i in range(self.size+1):
            self.board[0].append(Node())
            # print(self.upper_pseudo)
            # print(self.board[0][i])
            self.connect(self.upper_pseudo,self.board[0][i])
            self.values[0][i]=1
            #self.avail_moves.append((0,i))
            if i>0:
                self.connect(self.board[0][i-1],self.board[0][i])
        for i in range(1,self.size+1):
            self.board.append([])
            for j in range(self.size+1):
                self.board[i].append(Node())
                self.avail_moves.append((i,j))
                self.connect(self.board[i][j],self.board[i-1][j])
                if j>0:
                    self.connect(self.board[i][j-1],self.board[i][j])
                if j<self.size:
                    self.connect(self.board[i-1][j+1],self.board[i][j])
        for i in range(self.size+1):
            if self.values[i][0]==0:
                self.avail_moves.remove((i,0))
            self.values[i][0]=2
            self.connect(self.left_pseudo,self.board[i][0])
            if (i,self.size) in self.avail_moves:
                self.avail_moves.remove((i,self.size))
            self.values[i][self.size]=2
            self.connect(self.right_pseudo,self.board[i][self.size])
            if self.values[self.size][i]==0:
                self.avail_moves.remove((self.size,i))
            self.values[self.size][i]=1
            self.connect(self.lower_pseudo,self.board[self.size][i])
            
        for i in range(self.size+1):
            for j in range(self.size+1):
                self.board[i][j].position=(i,j)
    def connect(self,node1,node2):
        node1.connections.append(node2)
        node2.connections.append(node1)

    def is_p1_win(self):
        if self.is_connected(1):
            return True
        return False
    
    def is_p2_win(self):
        if self.is_connected(2):
            return True
        return False

    def payoff(self):
        return 1 if self.is_p1_win() else -1

    def is_connected(self,player):
        #Conduct DFS from one pseudonode to opposite pseudonode
        to_visit=[]
        visited=[[0] * (self.size+1) for i in range(self.size+1)]
        if player==1:
            #Begin with the upper pseudonode and add all adjacents
            for node in self.upper_pseudo.connections:
                if self.values[node.position[0]][node.position[1]]==1:
                    to_visit.append(node)
                    visited[node.position[0]][node.position[1]]=1
        elif player==2:
            for node in self.left_pseudo.connections:
                if self.values[node.position[0]][node.position[1]]==2:
                    to_visit.append(node)
                    visited[node.position[0]][node.position[1]]=1
        else:
            print("Invalid use")
            exit(1)
        while len(to_visit)>0:
            node=to_visit.pop()
            for new_node in node.connections:
                if new_node==(self.lower_pseudo if player==1 else self.right_pseudo):
                    return True
                if new_node.position is None:
                    pass
                elif (self.values[new_node.position[0]][new_node.position[1]]==player) and (visited[new_node.position[0]][new_node.position[1]]==0):
                    to_visit.append(new_node)
                    visited[new_node.position[0]][new_node.position[1]]=1
        return False

    def make_play(self, i, j):
        if self.values[i][j]!=0:
            print((i,j) in self.avail_moves)
            print(self.values[i][j])
            print((i,j))
            print("Error, playing over an already-filled square")
            exit(1)
        self.values[i][j]=self.player
        self.player=2-((self.player+1)%2)
        self.avail_moves.remove((i,j))

    def successor(self,play):
        succ=Game(self.size,self.board,self.values,self.upper_pseudo,\
        self.lower_pseudo,self.left_pseudo,self.right_pseudo,self.avail_moves,self.player)
        succ.make_play(play[0],play[1])
        succ._compute_hash()
        return succ
    
    def actor(self):
        return self.player

    def revert_play(self, i, j):
        self.values[i][j]=0
        self.avail_moves.append((i,j))

    def _compute_hash(self):
        self.hash=hash(tuple(map(tuple,self.values)))

    def __hash__(self):
        return self.hash

    def __eq__(self,other):
        if isinstance(other, Game):
            return self.__hash__()==other.__hash__()
        return NotImplemented

    def get_actions(self):
        return self.avail_moves

    def is_terminal(self):
        if self.is_p1_win() or self.is_p2_win():
            return True
        return False