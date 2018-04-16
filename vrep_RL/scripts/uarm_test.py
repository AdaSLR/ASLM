# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

from lib import vrep
from uarm import UARM
from environment import VREPEnv
import numpy as np

def main():
	env = VREPEnv()
	
	while True:
		pos = input('Enter 4 positions and grip flag: ').split(' ')
		pos = [int(p) for p in pos]	

		env.robot['uarm'].set_motors(position=pos[:-1], degrees=True)
		env.robot['uarm'].grip() if pos[-1] else env.robot['uarm'].ungrip()
		print(env.state())
		# Make sure that the last command 
		# sent out had time to arrive
		vrep.simxGetPingTime(env.conn_handler)

	# Close the connection to V-REP:
	env.finish()
	
	return 1


if __name__=='__main__':
	main()
