from Robot import Robot
from Simulation import Simulation


R1 = Robot([0, 0], 'U')
R2 = Robot([1, 3], 'R')
R3 = Robot([7, 9], 'D')

r_dict = {1: R1, 2: R2, 3: R3}
Sim = Simulation(r_dict, 10, 15)
Sim.set_board()
Sim.draw_board()
Sim.take_turn()



