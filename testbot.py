#Team number 56
import sys
import random
import signal
from copy import deepcopy

class Player13:
    def __init__(self):
        self.totalmoves=0
        self.first_move = [(5,5),(5,3),(3,3),(3,5)]
        self.ply = 4
        self.max_child = 0
        pass

    def determine_blocks_allowedd(self,old_move, block_stat):
        
        blocks_allowed = []
        if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
            blocks_allowed = [1,3]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
            blocks_allowed = [1,5]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
            blocks_allowed = [3,7]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
            blocks_allowed = [5,7]
        elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
            blocks_allowed = [0,2]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
            blocks_allowed = [0,6]
        elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
            blocks_allowed = [6,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
            blocks_allowed = [2,8]
        elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
            blocks_allowed = [4]
        else:
            sys.exit(1)

        final_blocks_allowed = []
        for i in blocks_allowed:
            if block_stat[i] == '-':
                final_blocks_allowed.append(i)
        return final_blocks_allowed

    def get_empty_out_off(self,gameb, blal,block_stat):
        cells = []  
        for idb in blal:
            id1 = idb/3
            id2 = idb%3
            for i in range(id1*3,id1*3+3):
                for j in range(id2*3,id2*3+3):
                    if gameb[i][j] == '-':
                        cells.append((i,j))

        if cells == []:
            new_blal = []
            all_blal = [0,1,2,3,4,5,6,7,8]
            for i in all_blal:
                if block_stat[i]=='-':
                    new_blal.append(i)

            for idb in new_blal:
                id1 = idb/3
                id2 = idb%3
                for i in range(id1*3,id1*3+3):
                    for j in range(id2*3,id2*3+3):
                        if gameb[i][j] == '-':
                            cells.append((i,j))
        return cells
    
    def give_block_no(self,x,y):
        if ((0<=y) and (2>=y) and (0<=x) and (2>=x)):
            return 0
        elif ((3<=y) and (5>=y) and (0<=x) and (2>=x)):
            return 1
        elif ((6<=y) and (8>=y) and (0<=x) and (2>=x)):
            return 2
        elif ((0<=y) and (2>=y) and (3<=x) and (5>=x)):
            return 3
        elif ((3<=y) and (5>=y) and (3<=x) and (5>=x)):
            return 4
        elif ((6<=y) and (8>=y) and (3<=x) and (5>=x)):
            return 5
        elif ((0<=y) and (2>=y) and (6<=x) and (8>=x)):
            return 6
        elif ((3<=y) and (5>=y) and (6<=x) and (8>=x)):
            return 7
        elif ((6<=y) and (8>=y) and (6<=x) and (8>=x)):
            return 8

    def checkwin(self,board,cell,flag_player):
        x = cell[0]
        y = cell[1]

        if flag_player == 1:
            board[x][y] = 'x'
        else:
            board[x][y] = 'o'

        idb = self.give_block_no(x,y)

        id1 = idb/3 #0
        id2 = idb%3 #1


        id1 = id1*3;
        id2 = id2*3
        
        x = cell[0]%3 #2
        y = cell[1]%3 #2
        
        if board[id1+0][id2+y] == 'x' and board[id1+1][id2+y] == 'x' and board[id1+2][id2+y] == 'x':
            return True
        if board[id1+0][id2+y] == 'o' and board[id1+1][id2+y] =='o' and board[id1+2][id2+y] == 'o':
            return True

        #check if previous move was on horizontal line and caused a win
        if board[id1+x][id2+0] == 'x' and board[id1+x][id2+1] == 'x' and board[id1+x][id2+2] == 'x':
            return True
        if board[id1+x][id2+0] == 'o' and board[id1+x][id2+1] == 'o' and board[id1+x][id2+2] == 'o':
            return True

        #check if previous move was on the main diagonal and caused a win
        if board[id1+0][id2+0] == 'x' and board[id1+1][id2+1] == 'x' and board[id1+2][id2+2] == 'x':
            return True
        if board[id1+0][id2+0] == 'o' and board[id1+1][id2+1] == 'o' and board[id1+2][id2+2] == 'o':
            return True
        #check if previous move was on the secondary diagonal and caused a win
        if board[id1+0][id2+2] == 'x' and board[id1+1][id2+1] == 'x' and board[id1+2][id2+0] == 'x':
            return True
        if board[id1+0][id2+2] == 'o' and board[id1+1][id2+1] == 'o' and board[id1+2][id2+0] == 'o':
            return True

        return False

    def virtual_move(self,temp_board,temp_block,old_move):
        blocks_allowed  = self.determine_blocks_allowedd(old_move, temp_block)
        return blocks_allowed

    def check_board_win(self,temp_board,temp_block,cell,flag_player):
        
        if self.checkwin(temp_board,cell,flag_player):
            x = cell[0]
            y = cell[1]

            idb = self.give_block_no(x,y)

            if flag_player == 1:
                if temp_block[idb] == '-' or temp_block[idb] == 'x':
                    temp_block[idb] = 'x'
            else:
                if temp_block[idb] == '-' or temp_block[idb] == 'o':
                    temp_block[idb] = 'o'

            if temp_block[0] == 'x' and temp_block[1] == 'x' and temp_block[2] == 'x':
                return True
            if temp_block[0] == 'o' and temp_block[1] == 'o' and temp_block[2] == 'o':
                return True
            
            if temp_block[3] == 'x' and temp_block[4] == 'x' and temp_block[5] == 'x':
                return True
            if temp_block[3] == 'o' and temp_block[4] == 'o' and temp_block[5] == 'o':
                return True
            
            if temp_block[6] == 'x' and temp_block[7] == 'x' and temp_block[8] == 'x':
                return True
            if temp_block[6] == 'o' and temp_block[7] == 'o' and temp_block[8] == 'o':
                return True
            
            if temp_block[0] == 'x' and temp_block[3] == 'x' and temp_block[6] == 'x':
                return True
            if temp_block[0] == 'o' and temp_block[3] == 'o' and temp_block[6] == 'o':
                return True

            if temp_block[1] == 'x' and temp_block[4] == 'x' and temp_block[7] == 'x':
                return True
            if temp_block[1] == 'o' and temp_block[4] == 'o' and temp_block[7] == 'o':
                return True
            
            if temp_block[2] == 'x' and temp_block[5] == 'x' and temp_block[8] == 'x':
                return True
            if temp_block[2] == 'o' and temp_block[5] == 'o' and temp_block[8] == 'o':
                return True
            
            if temp_block[0] == 'x' and temp_block[4] == 'x' and temp_block[8] == 'x':
                return True
            if temp_block[0] == 'o' and temp_block[4] == 'o' and temp_block[8] == 'o':
                return True
            
            if temp_block[2] == 'x' and temp_block[4] == 'x' and temp_block[6] == 'x':
                return True
            if temp_block[2] == 'o' and temp_block[4] == 'o' and temp_block[6] == 'o':
                return True

    def AI(self,temp_board, blocks_allowed, temp_block,player_no,level,alpha,beta):

        if level > self.ply:
            return
        

        center_cells = [(1,1),(1,4),(1,7),(4,1),(4,4),(4,7),(7,1),(7,4),(7,7)]
        
        corner_cells = [(0,0),(0,2),(0,3),(0,5),(0,6),(0,8),
                        (2,0),(2,2),(2,3),(2,5),(2,6),(2,8),
                        (3,0),(3,2),(3,3),(3,5),(3,6),(3,8),
                        (5,0),(5,2),(5,3),(5,5),(5,6),(5,8),
                        (6,0),(6,2),(6,3),(6,5),(6,6),(6,8),
                        (8,0),(8,2),(8,3),(8,5),(8,6),(8,8)]    
        
        total_blocks = deepcopy(blocks_allowed)

        for i in range(len(total_blocks)):
            if temp_block[total_blocks[i]] != '-':
                blocks_allowed.remove(total_blocks[i])

        cells = self.get_empty_out_off(temp_board, blocks_allowed,temp_block)
        heuristic = -100


        if self.totalmoves ==1 and player_no==1:
            return self.first_move[random.randrange(len(self.first_move))]
        
        elif self.totalmoves ==1 and player_no==2:
            for each_cell in cells:
                if each_cell in corner_cells:
                    return each_cell
        
        if level == 1: 
            heuristic_dict = {}
            if len(cells) == 1: #if only one block is free
                return cells[0]


        self.max_child = self.max_child + len(cells)

        if self.max_child < 6000:
            self.ply = 6

        elif self.max_child > 6000 and level < 5:
            self.ply =4
        # if self.totalmoves > 24:
            # self.ply = 6

        # if self.totalmoves > 18:
            # self.ply = 8

        for each_cell in cells: # Min-Max
            another_board = deepcopy(temp_board)   
            another_block = deepcopy(temp_block)
            temp_player_no = player_no

            if temp_player_no == 1:
                temp_player_no = 2
            else:
                temp_player_no = 1

            if self.totalmoves > 8 and  self.check_board_win(another_board,another_block,each_cell,player_no):
                temp_heuristic = 100
                if level == 1:
                    return each_cell
            
            elif self.totalmoves > 8 and  self.check_board_win(another_board,another_block,each_cell,temp_player_no):
                temp_heuristic = 90
            
            else:        
                another_board = deepcopy(temp_board)
                if self.checkwin(another_board,each_cell,player_no):
                        temp_heuristic = 60
                else: 
                    another_board = deepcopy(temp_board)
                    if player_no == 1:
                        player_no = 2
                    else:
                        player_no = 1
                    # Opponent Blocking
                    if self.checkwin(another_board,each_cell,player_no):
                        temp_heuristic = 40
                    else:
                        if each_cell in center_cells:
                            temp_heuristic = 5
                        if each_cell in corner_cells:
                            temp_heuristic = 15
                        if each_cell not in center_cells and each_cell not in corner_cells:
                            temp_heuristic = 10

            if level < self.ply:
                another_board = deepcopy(temp_board)
                another_block = deepcopy(temp_block)
                next_blocks_allowed = self.virtual_move(another_board,another_block,each_cell)
                if self.checkwin(another_board,each_cell,player_no):
                    x = each_cell[0]
                    y = each_cell[1]

                    idb = self.give_block_no(x,y)

                    if player_no == 1:
                        another_block[idb] = 'x'
                    else:
                        another_block[idb] = 'o'
                
                if player_no ==1:
                    next_player =2
                    another_board[each_cell[0]][each_cell[1]] = 'x'

                elif player_no ==2:
                    next_player=1
                    another_board[each_cell[0]][each_cell[1]] = 'o'
                
                next_heuristic = self.AI(another_board, next_blocks_allowed, another_block, next_player,level+1,alpha,beta)
                final_heuristic = temp_heuristic - next_heuristic
                
                #Alpha-Beta Pruning
                if next_heuristic > alpha and level%2==1:
                    alpha = next_heuristic
                
                elif next_heuristic < beta and level%2==0:
                    beta = next_heuristic
            
            if alpha > beta: #Alpha-Beta Pruning
                break

            if level < self.ply:
                if level ==1:    
                    if final_heuristic not in heuristic_dict.keys():
                        heuristic_dict[final_heuristic] = [each_cell]
                    else:
                        heuristic_dict[final_heuristic].append(each_cell)

                if final_heuristic > heuristic:
                    heuristic = final_heuristic 

            else:
                if temp_heuristic > heuristic:
                    heuristic = temp_heuristic


        if level ==1:
            final_list = heuristic_dict[heuristic]            
            return final_list[random.randrange(len(final_list))]
        else:
            return heuristic


    def move(self,temp_board,temp_block,old_move,flag):
        self.totalmoves = self.totalmoves+1
        blocks_allowed  = self.determine_blocks_allowedd(old_move, temp_block)
        
        print "Number of children " , self.max_child
        print self.totalmoves
        self.max_child = 0

        if flag == 'x':
            player_no = 1
        else:
            player_no =  2
        
        return self.AI(temp_board,blocks_allowed,temp_block,player_no,1,-99999999,99999999)


"""
Player 2 made the move: (8, 1) with o
=========== Game Board ===========
- - -  x - -  - - -
o - o  - - -  - - o
- - x  x - o  - x -

o - -  - - -  - - o
- - -  - - -  - - -
- - o  x x -  - - x
    #
- x -  - o -  - x -
- - o  - - -  - o x
- o -  - o x  - x -#
==================================
=========== Block Status =========
- - -
- - -
- - -
==================================

13
Player 1 made the move: (8, 8) with x
=========== Game Board ===========
- - -  x - -  - - -
o - o  - - -  - - o
- - x  x - o  - x -

o - -  - - -  - - o
- - -  - - -  - - -
- - o  x x -  - - x

- x -  - o -  - x -
- - o  - - -  - o x
- o -  - o x  - x x
==================================
=========== Block Status =========
"""