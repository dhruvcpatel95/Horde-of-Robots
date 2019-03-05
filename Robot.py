import random


class Robot:
	"""Robot class"""

	DIRECTION_SYMBOLS_DICT = {'U': '\u25B2', 'R': '\u25B6', 'D': '\u25BC', 'L': '\u25C0'}
	MOVE_DIR_DICT = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}

	def __init__(self, location=[random.randrange(10), random.randrange(10)], pointer_dir_key=random.choice(['U', 'R', 'D', 'L']),
				 shoot_phrases = ['Shot Fired!', 'Exterminate!']):
		self.location = location
		self.pointer_dir_key = pointer_dir_key
		self.pointer_dir_symbol = Robot.DIRECTION_SYMBOLS_DICT[pointer_dir_key]
		self.shoot_phrases = shoot_phrases

	def __str__(self):
		return "Location ({},{}) \nDirection: {}".format(self.location[0], self.location[1], self.pointer_dir_symbol)

	def __repr__(self):
		return " ({},{}), {} ".format(self.location[0], self.location[1], self.pointer_dir_symbol)

	def move(self, move_dir):
		# check if the location after moving is >= (0,0). We have set no upper bounds on location.

		if (self.location[0] + Robot.MOVE_DIR_DICT[move_dir][0] >= 0) and (self.location[1] + Robot.MOVE_DIR_DICT[move_dir][1] >= 0):
			self.location = [self.location[0] + Robot.MOVE_DIR_DICT[move_dir][0],
							 self.location[1] + Robot.MOVE_DIR_DICT[move_dir][1]]
			self.pointer_dir_key = move_dir
			self.pointer_dir_symbol = Robot.DIRECTION_SYMBOLS_DICT[move_dir]

			return True
		return False

	def shoot(self):
		print(self.shoot_phrases[random.randrange(len(self.shoot_phrases))])


