import numpy as np
from Robot import Robot

class Simulation:
	def __init__(self, robot_dict, rows=10, cols=10, empty_symbol=' '):
		self.rows = rows
		self.cols = cols
		self.empty_symbol = empty_symbol
		self.robot_dict = self._filer_list(robot_dict)
		self.board = np.empty((self.rows, self.cols), dtype=Robot)

	def _filer_list(self, robot_dict):
		# Filter robot_dict to contain robots with distinct locations

		# dictionary containing the robot key as key and robot location as value
		robot_loc_dict = {key: val.location for key, val in robot_dict.items()}
		unique_loc_dict = {}
		for key, val in robot_loc_dict.items():
			if val not in unique_loc_dict.values():
				unique_loc_dict[key] = val
			else:
				print("Robot with key {} has been eliminated because location is occupied.".format(key))

		unique_robot_dict = {key: val for key, val in robot_dict.items() if key in unique_loc_dict.keys()}

		return unique_robot_dict

	def set_board(self):
		print("These robots have made it into the simulation: ", self.robot_dict)
		self.board[:] = None
		for robot in self.robot_dict.values():
			self.board[robot.location[0], robot.location[1]] = robot

	def draw_board(self):
		# add padding to the board for printing purposes
		padded_board = np.pad(self.board, ((1, 1), (1, 1)), 'constant', constant_values=(('-', '-'), ('|', '|')))
		padded_board[0, 0] = '+'
		padded_board[0, self.cols + 1] = '+'
		padded_board[self.rows + 1, self.cols + 1] = '+'
		padded_board[self.rows + 1, 0] = '+'

		for index, element in np.ndenumerate(padded_board):
			if (index[1] % (self.cols + 2)) == 0: print()
			if element is None: print(self.empty_symbol, end="")
			elif isinstance(element, Robot ): print(element.pointer_dir_symbol, end="")
			else: print(element, end="")
		print()
		print("Robots on the board: ", self.robot_dict)

	def is_move_valid(self, robot_key, move_dir):
		robot_loc = self.robot_dict[robot_key].location
		change_by = Robot.MOVE_DIR_DICT[move_dir]

		if ((robot_loc[0] + change_by[0] >= 0) and (robot_loc[0] + change_by[0] < self.rows)) and (
				(robot_loc[1] + change_by[1] >= + 0) and (robot_loc[1] + change_by[1] < self.cols)):
			if self.board[robot_loc[0] + change_by[0], robot_loc[1] + change_by[1]] is None:
				return True
			else:
				print("Invalid Move: Position is occupied")
				return False
		else:
			print("Invalid Move: Position out of bounds")
			return False

	def move(self, robot_key, move_dir):
		robot_loc = self.robot_dict[robot_key].location
		change_by = Robot.MOVE_DIR_DICT[move_dir]
		# check if the move is possible
		print("New Call")
		if self.is_move_valid(robot_key, move_dir):
			self.robot_dict[robot_key].move(move_dir) #calls move method of the robot object. Just here for no Reason right now!
			self.board[robot_loc[0] + change_by[0],
					   robot_loc[1] + change_by[1]] = self.robot_dict[robot_key]
			self.board[robot_loc[0], robot_loc[1]] = None
			print("Location after move {}: {}".format(move_dir, self.robot_dict[robot_key].location))

			self.draw_board()

			return True
		self.draw_board()
		return False

	def shoot(self, robot_key):
		self.robot_dict[robot_key].shoot() #Calls the shoot method of the robot object. Just prints one of robots 'shoot_phrases'.
		search_dir = self.robot_dict[robot_key].pointer_dir_key
		loc = self.robot_dict[robot_key].location
		search_vals = []
		if search_dir == 'U': search_vals = self.board[:loc[0], loc[1]]
		if search_dir == 'R': search_vals = self.board[loc[0], loc[1]+1:]
		if search_dir == 'D': search_vals = self.board[loc[0]+1:, loc[1]]
		if search_dir == 'L': search_vals = self.board[loc[0], :loc[1]]
		#print(self.board)
		print("Search Vals: ", search_vals)

		for element in search_vals:
			if isinstance(element, Robot):
				robot_to_kill_loc = element.location
				robot_to_kill = [key for key in self.robot_dict if element == self.robot_dict[key]][0]
				print("Killing Robot:", robot_to_kill)
				self.board[robot_to_kill_loc[0], robot_to_kill_loc[1]] = None
				del self.robot_dict[robot_to_kill]
				print("Robot {} has been Exterminated. Here are the remaining Robots: {}".format(robot_to_kill, self.robot_dict))
				self.draw_board()

				return True
		print("Nothing to kill. Ran into a wall.")
		self.draw_board()
		return False

	def take_turn(self):
		while True:
			if len(self.robot_dict) == 1:
				print("You are alone in this world :( ")
			for key in tuple(self.robot_dict):
				if key in self.robot_dict:
					move = input("Robot {}'s turn. Enter 'U', 'R', 'D', 'L' to move and 'Q' to shoot. Enter anything else to skip turn.: ".format(key))
					if move in Robot.MOVE_DIR_DICT:
						self.move(key, move)
					elif move == 'Q':
						self.shoot(key)
					else:
						print("Your turn has been skipped.")
