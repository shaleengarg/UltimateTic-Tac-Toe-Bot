from operator import itemgetter
import copy
import time

temp = 0
cccc = 0
class IntelligentPlayer:
	def __init__(self):
		pass
	def move(self, temp_board, temp_block, old_move, flag):
                cccc = 0
                if(flag=='x'):
                 temp=1
                else:   
                    temp=0
                if(flag=='x' and old_move[0]==-1 and old_move[1]==-1):
                    # print "Arabin"
                    return (3,3)
                blocks_allowed = determine_allowed_blocks(old_move, temp_block)
		cells  = get_empty_cells(temp_block,temp_board, blocks_allowed,0)
                # print cells
                best_cell = findbestcell(temp_board,cells,old_move,3,temp,temp_block,-10e6,10e6)
                # print "best_cell",best_cell
                # print "cccc",cccc
              #  time.sleep(3)
                return f(best_cell)
def f(t):
    return (t[0],t[1])
def update(game_board, block_stat, move_ret, fl):
	game_board[move_ret[0]][move_ret[1]] = fl
        block_no = (move_ret[0]/3)*3 + move_ret[1]/3	
	id1 = block_no/3
	id2 = block_no%3
	mflg = 0
        flag = 0
	for i in range(id1*3,id1*3+3):
		for j in range(id2*3,id2*3+3):
			if game_board[i][j] == '-':
				flag = 1
        if block_stat[block_no] == '-':
		if game_board[id1*3][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3+2][id2*3+2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if game_board[id1*3+2][id2*3] == game_board[id1*3+1][id2*3+1] and game_board[id1*3+1][id2*3+1] == game_board[id1*3][id2*3 + 2] and game_board[id1*3+1][id2*3+1] != '-' and game_board[id1*3+1][id2*3+1] != 'D':
			mflg=1
		if mflg != 1:
                    for i in range(id2*3,id2*3+3):
                        if game_board[id1*3][i]==game_board[id1*3+1][i] and game_board[id1*3+1][i] == game_board[id1*3+2][i] and game_board[id1*3][i] != '-' and game_board[id1*3][i] != 'D':
                                mflg = 1
                                break
		if mflg != 1:
                    for i in range(id1*3,id1*3+3):
                        if game_board[i][id2*3]==game_board[i][id2*3+1] and game_board[i][id2*3+1] == game_board[i][id2*3+2] and game_board[i][id2*3] != '-' and game_board[i][id2*3] != 'D':
                                mflg = 1
                                break
	if flag == 0:
		block_stat[block_no] = 'D'
	if mflg == 1:
		block_stat[block_no] = fl
	return block_stat

def printboard(gb):
	print '=========== Game Board ==========='
	for i in range(9):
		if i > 0 and i % 3 == 0:
			print
		for j in range(9):
			if j > 0 and j % 3 == 0:
				print " " + gb[i][j],
			else:
				print gb[i][j],

		print
	print "=================================="

def findbestcell(temp_board,cells,old_move,level,player,temp_block,alpha,beta):
     #   global temp
    	if level == 0:
                
                v = (0,0,-10e9)
		for i in range(len(cells)):
                        temp2_board=copy.deepcopy(temp_board)
                        if player == 1:
                                temp2_board[cells[i][0]][cells[i][1]]='x'
                        else:
				temp2_board[cells[i][0]][cells[i][1]]='o'
                        x=calculate_heuristic(temp2_board,player)
                        y=calculate_heuristic(temp2_board,1-player)
                        c=(x-y,)
                        cells[i]=cells[i]+c
                        if c[0] > v[2]:
                            v=cells[i]+c
                        if v[2] > alpha:
                            alpha = v[2]
                        if alpha >= beta:
                            break
                return v                    

	else:
                
                new=[]

                if level %2 ==0:
                        v = (0,0,-10e9)
                else:
                        v = (0,0,10e9)
                for cell in cells:


			temp2_board=copy.deepcopy(temp_board)
                        temp2_block=copy.deepcopy(temp_block)
			if player == 1:
                                temp2_board[cell[0]][cell[1]]='x'
			else:
				temp2_board[cell[0]][cell[1]]='o'
                        if(player==1):
                            x='x'
                            y='o'
                        else:
                            x='o'
                            y='x'
                     
                        temp2_block=update(temp2_board,temp2_block,cell,x)

                        blocks_all = determine_allowed_blocks(cell,temp2_block)
                        
			cell2  = get_empty_cells(temp2_block,temp2_board, blocks_all,0)

                        if(cell2==[]):

                          #  print "abc"
                          #  print temp2_block
                          #  p = [[0 for x in range(3)] for x in range(3)] 
                          #  for i in range(0,9):
                           #     p[i/3][i%3]=temp2_block[i]

                       #     print"p", p


                                
                         
                         #   print find_heuristic(temp2_block,x,y,0,0)
                            c=cell +(calculate_heuristic(temp2_board,player),)
                        #    print c,

                     #       c=(-2,-2,10)
                        else:
                            t=findbestcell(temp2_board,cell2,cell,level-1,1-player,temp2_block,alpha,beta)
                            c=cell+ (t[2],)
                          #  print c, 
                          
                        if level % 2 == 0:  
                            if c[2] > v[2]:
                                v = c
                            if v[2] > alpha:
                                alpha = v[2]
                            if alpha >= beta:
                                 break
                        else:
                            if v[2] > c[2]:
                                v=c
                            if beta > v[2]:
                                beta = v[2]
                            if alpha >= beta:
                                 break
                        
                        new.append(c)
                
                if(old_move==(3,3)):
                        # print new 
                    pass
                      #  sys.exit(1)
                return  v



                        
def calculate_heuristic(temp_board,player):
        global cccc
        cccc += 1
#	print "bbbb"
	heuristic=[]
 #       heuristic1=[]

        for i in range(0,9):
       # for i in range(1):
			
		#	print (calculate_heuristic_block(temp_board,i,player))
	        heuristic.append(calculate_heuristic_block(temp_board,i,player))
#                heuristic1.append(calculate_heuristic_block(temp_board,i,1-player))
#	print temp_board
#        sys.exit(1)
        h = 0
        '''p = [[0 for x in range(3)] for x in range(3)] 
        if(player==1):
            player='x'
            opponent='o'
        else:
            player='o'
            opponent='x'
        for i in range(0,9):
            if(heuristic1[i]>heuristic[i]):
                p[i/3][i%3]=opponent
            elif heuristic[i]>heuristic1[i]:
                p[i/3][i%3]=player
            else:
                p[i/3][i%3]=player
#        return find_heuristic(p,player,opponent,0,0)
        '''


	
        h += (convert_heuristic(heuristic,0,1,2) + convert_heuristic(heuristic,3,4,5) +convert_heuristic(heuristic,6,7,8))
        h += (convert_heuristic(heuristic,0,3,6) + convert_heuristic(heuristic,1,4,7) +convert_heuristic(heuristic,2,5,8))
	
        h += (convert_heuristic(heuristic,0,4,8) + convert_heuristic(heuristic,2,4,6))
        
     #   if temp_board[0][3]=='x'):
      #      sys.exit(0)
        return h



	
def convert_heuristic(heuristic,i,j,k):
    
        h=0
	temp = heuristic[i] + heuristic[j] + heuristic[k]
        if temp < 1:
		h += temp
	elif temp > 1 and temp < 2:
		h += ( (temp-1) * 9 ) + 1
	elif temp > 2 and temp < 3:
		h = (temp-2) * 90 + 10
	else:
		h += 1000
        return h



def calculate_heuristic_block(temp_board,block_no,player):
        if block_no ==0:
		row = 0  
                column = 0
	if block_no == 1:
		row = 0 
                column = 3
	if block_no == 2:
		row = 0
                column = 6
	if block_no == 3:
		row = 3 
                column = 0
	if block_no == 4:
		row = 3 
                column = 3
	if block_no == 5:
		row = 3
                column = 6
	if block_no == 6:
		row = 6 
                column = 0
	if block_no == 7:
		row = 6 
                column = 3
	if block_no == 8:
		row = 6 
                column = 6
	if player == 1:
            player = 'x'
	    opponent = 'o'
        else:
	    player = 'o'
	    opponent = 'x'
        return find_heuristic(temp_board,player,opponent,row,column)

def find_heuristic(temp_board,player,opponent,row,column):
	heuristic_value = 0


        for i in range(row,row+3):
		countr = 0
		countc = 0
		for j in range(column,column+3):
			
                        if temp_board[i][j] == player:                  #for row
				countr += 1
			
                        if temp_board[i][j] == opponent:
				countr = -10
                        
                        if temp_board[j-column+row][i-row+column] == player:                  # for column
				countc += 1

			
                        if temp_board[j-column+row][i-row+column] == opponent:
				countc = -10
                
                if countr == 1:
			heuristic_value += 1
		elif countr == 2:
			heuristic_value += 10
		elif countr == 3:
			heuristic_value += 100
                if countc == 1:
			heuristic_value += 1
		elif countc == 2:
			heuristic_value += 10
		elif countc == 3:
			heuristic_value += 100
        count=0
	for i in range (3):                                             # first diagonal
		if temp_board[row+i][column+i] == player:
			count += 1
		if temp_board[row+i][column+i] == opponent:
			count -= 10
        if count == 1:
		heuristic_value += 1
	elif count == 2:
		heuristic_value += 10
	elif count == 3:
		heuristic_value += 100


	count=0
	for i in range (3):                                             # second diagonal
		if temp_board[row+i][column+2-i] == player:
			count += 1
		if temp_board[row+i][column+2-i] == opponent:
			count -= 10


        if count == 1:
		heuristic_value += 1
	elif count == 2:
		heuristic_value += 10
	elif count == 3:
		heuristic_value += 100
        if heuristic_value > 100:   
		heuristic_value = 100

        
#       print heuristic_value*1.0/100
	return  (heuristic_value*1.0)/100


def determine_allowed_blocks(old_move, block_stat):
	blocks_allowed = []
        if old_move[0]%3==0:
            if old_move[1]%3==0:
		blocks_allowed.append(1)
                blocks_allowed.append(3)
            elif old_move[1]%3==2:
                blocks_allowed.append(1)
                blocks_allowed.append(5)
            else:
                blocks_allowed.append(0)
                blocks_allowed.append(2)
        elif old_move[0]%3==1:
            if old_move[1]%3==0:
		blocks_allowed.append(0)
                blocks_allowed.append(6)
            elif old_move[1]%3==2:
                blocks_allowed.append(2)
                blocks_allowed.append(8)
            else:
                blocks_allowed.append(4)
        elif old_move[0]%3==2:
            if old_move[1]%3==0:
		blocks_allowed.append(3)
                blocks_allowed.append(7)
            elif old_move[1]%3==2:
                blocks_allowed.append(5)
                blocks_allowed.append(7)
            else:
                blocks_allowed.append(6)
                blocks_allowed.append(8)
        else:
            sys.exit(1)
        final_blocks_allowed = []
	for i in blocks_allowed:
		if block_stat[i] == '-':
			final_blocks_allowed.append(i)
	return final_blocks_allowed

def get_empty_cells(block_stat,game_board, a_b,count):
        empty_cells = []  # it will be list of tuples
	#Iterate over possible blocks and get empty cells
	for idb in a_b:
		id1 = idb/3
		id2 = idb%3
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if game_board[i][j] == '-':
					empty_cells.append((i,j))
    
        #    print "z"
         #   print empty_cells
    
	# If all the possible blocks are full, you can move anywhere
	if empty_cells == [] and count==0:
            new=[]

            for i in range(0,9):
                if(block_stat[i]=='-'):
                    new.append(i)
            
            return get_empty_cells(block_stat,game_board,new,1)
                
	'''	for idb in new_blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))'''
	return empty_cells
