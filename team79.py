#Team number 79
import sys
import random
import signal
from operator import itemgetter

class Player79:
	def __init__(self):
		self.marker = ""
		self.no_of_moves = 0
		self.force_move = [(3,3),(3,5),(5,3),(5,5)] # 4 corners of the centre block
		self.depth_level = 3
		pass

	def move(self,temp_board,temp_block_stat,old_move,flag):
		self.marker = flag
		if self.marker == 'x':
			self.oppmarker = 'o'
		else :
			self.oppmarker = 'x'
			
		if self.no_of_moves >= 10 :
			self.depth_level = 4

		if self.no_of_moves >= 18 :
			self.depth_level = 5

		if self.no_of_moves >= 33 :
			self.depth_level = 7
			
		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block_stat)
		cells = self.get_empty_out_of(temp_board, blocks_allowed,temp_block_stat)

		if self.no_of_moves == 0 and self.marker == 'x' :
			get_move = self.force_move[random.randrange(4)]
		else :
			get_val,get_move = self.minimax(temp_board,temp_block_stat,old_move,0,-99999999,99999999)
			print get_val
			
		print get_move
		print self.depth_level
		
		self.no_of_moves += 1
		return get_move

	#def hardcode():
		
	def determine_blocks_allowed(self,old_move, block_stat):
		blocks_allowed = []
		#print "here"
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

	def get_empty_out_of(self,gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
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

	def CRCalculation(self,pcount,ocount):
		net_value = 0

		if ocount == 0 :
			if pcount == 1 :
				net_value += 1
			elif pcount == 2 :
				net_value += 10
			elif pcount == 3 :
				net_value += 100

		if pcount == 0 :
			if ocount == 1 :
				net_value -= 1
			elif ocount == 2 :
				net_value -= 10
			elif ocount == 3 :
				net_value -= 100

		return net_value

	def bstat_CRCalculation(self,pcount,ocount,dcount):
		net_value = 0

		if ocount == 0 and dcount == 0 :
			if pcount == 1 :
				net_value += 200
			elif pcount == 2 :
				net_value += 500
			elif pcount == 3 :
				net_value += 1000

		if pcount == 0 and dcount == 0:
			if ocount == 1 :
				net_value -= 200
			elif ocount == 2 :
				net_value -= 500
			elif ocount == 3 :
				net_value -= 1000

		return net_value
		
	def block_stat_calculation(self,block_stat):
		net_value = 0
		for row in range(0,8,3):
			pcount=0
			ocount=0
			dcount=0
			for col in range(row,row+3):
				if block_stat[col] == self.marker:
					pcount += 1
				elif block_stat[col] == self.oppmarker:
					ocount += 1
				elif block_stat[col] == 'D':
					dcount += 1
			net_value += self.bstat_CRCalculation(pcount,ocount,dcount)
					
				
		for col in range(0,3):
			pcount=0
			ocount=0
			dcount=0
			for row in range(col,8,3):
				if block_stat[row] == self.marker:
					pcount += 1
				elif block_stat[row] == self.oppmarker:
					ocount += 1
				elif block_stat[row] == 'D':
					dcount += 1
			net_value += self.bstat_CRCalculation(pcount,ocount,dcount)

		dcount=0
		ocount=0
		pcount=0
		for block in range(0,9,4):
			if block_stat[block] == self.marker:
				pcount += 1
			elif block_stat[block] == self.oppmarker:
				ocount += 1
			elif block_stat[block] == 'D':
				dcount += 1
		net_value += self.bstat_CRCalculation(pcount,ocount,dcount)

		ocount=0
		pcount=0
		dcount=0
		for block in range(2,8,2):
			if block_stat[block] == self.marker:
				pcount += 1
			elif block_stat[block] == self.oppmarker:
				ocount += 1
			elif block_stat[block] == self.oppmarker:
				dcount += 1
		net_value += self.bstat_CRCalculation(pcount,ocount,dcount)
							
		return net_value
	
	def utility_value(self,cur_move,temp_board,temp_block_stat):
		net_value = 0

		net_value += self.block_stat_calculation(temp_block_stat) #Inter block heuristic calculation
		
		if 0<= cur_move[0] <=2 :
			x=0
		elif 3<= cur_move[0] <=5 :
			x=3
		elif 6<= cur_move[0] <=8 :
			x=6

		if 0<= cur_move[1] <=2 :
			y=0
		elif 3<= cur_move[1] <=5 :
			y=3
		elif 6<= cur_move[1] <=8 :
			y=6

		for row in range(x,x+3):
			pcount=0
			ocount=0
			for col in range(y,y+3):
				if temp_board[row][col] == self.marker :
					pcount+=1
				elif temp_board[row][col] == self.oppmarker :
					ocount+=1
			net_value += self.CRCalculation(pcount,ocount)

		for col in range(y,y+3):
			pcount=0
			ocount=0
			for row in range(x,x+3):
				if temp_board[row][col] == self.marker :
					pcount+=1
				elif temp_board[row][col] == self.oppmarker :
					ocount+=1
			net_value += self.CRCalculation(pcount,ocount)

		pcount=0
		ocount=0
		for row,col in zip(range(x,x+3),range(y,y+3)):
			if temp_board[row][col] == self.marker :
				pcount+=1
			elif temp_board[row][col] == self.oppmarker :
				ocount+=1
		net_value += self.CRCalculation(pcount,ocount)

		pcount=0
		ocount=0
		for col,row in zip(range(y+2,y-1,-1),range(x,x+3)):
			if temp_board[row][col] == self.marker :
				pcount+=1
			elif temp_board[row][col] == self.oppmarker :
				ocount+=1
		net_value += self.CRCalculation(pcount,ocount)
			
		return net_value
	
	def minimax(self,temp_board,temp_block_stat,cur_move,depth,alpha,beta) :
				
		if depth <= self.depth_level :
			blocks_allowed = self.determine_blocks_allowed(cur_move, temp_block_stat)
			cells = self.get_empty_out_of(temp_board, blocks_allowed,temp_block_stat)
			
			child_ret_list = []
			for choice in cells :
				if depth%2 == 0 :
					bblock_flag,bblock_pos = self.update_lists(temp_board, temp_block_stat, choice, self.marker) #even my move
				else :
					bblock_flag,bblock_pos = self.update_lists(temp_board, temp_block_stat, choice, self.oppmarker) #odd opponent move

				val,best_move = self.minimax(temp_board,temp_block_stat,choice,depth + 1,alpha,beta) #recursion
							
				child_ret_list.append((val,choice))

				if val>alpha and depth%2==0 :
					alpha = val
				elif val<beta and depth%2==1 :
					beta = val
					
				#Reverting temporary move made
				temp_board[choice[0]][choice[1]] = '-'
				if(bblock_flag == 1):
					temp_block_stat[bblock_pos] = '-'

				if alpha > beta : #alpha-beta pruning
					break
					
			if len(cells) == 0 :
				return (self.utility_value(cur_move,temp_board,temp_block_stat),cur_move) #Calculate utility if reached depth
			elif depth%2 == 0 :
				return max(child_ret_list,key=itemgetter(0))
			else :
				return min(child_ret_list,key=itemgetter(0))
		else :
			return (self.utility_value(cur_move,temp_board,temp_block_stat),cur_move)
		
	def update_lists(self,game_board, block_stat, move_ret, fl):

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

		if mflg == 1:
			block_stat[block_no] = fl
			
		if flag == 0 and mflg == 0:
			block_stat[block_no] = 'D'
			mflg = 1
		
		return mflg , block_no