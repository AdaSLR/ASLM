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
	uarm = UARM(env.conn_handler)
	
	while True:
		pos = input('Enter 4 positions: ').split(' ')
		pos = [int(p) for p in pos]	

		uarm.set_motors(position=pos, degrees=True)
		# Make sure that the last command 
		# sent out had time to arrive
		vrep.simxGetPingTime(env.conn_handler)

	# Close the connection to V-REP:
	env.finish()
	
	return 1


if __name__=='__main__':
	main()
