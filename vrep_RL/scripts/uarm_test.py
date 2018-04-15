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
import numpy as np

def main():
	vrep.simxFinish(-1) 
	# Connect to V-REP via sockets
	clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
	if clientID == -1:
		print ('Failed connecting to remote API server')
		return -1	
	print ('Connected to remote API server')

	uarm = UARM(clientID)
	print(uarm.motor_handlers)
	uarm.set_motors(position=[0,34,15,0], degrees=True)
	# Before closing the connection to V-REP, make sure that the last command 
	# sent out had time to arrive
	vrep.simxGetPingTime(clientID)

	# Close the connection to V-REP:
	vrep.simxFinish(clientID)
	return 1


if __name__=='__main__':
	main()
