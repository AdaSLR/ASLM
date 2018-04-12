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

import vrep
import numpy as np


class UARM(object):
	def __init__(self, client_id):
		self.motor_handlers = []
		for i in range(0,4):
			error, vrep_motor_handler = vrep.simxGetObjectHandle(client_id, 'uarm_motor' + str(i+1), vrep.simx_opmode_oneshot_wait)
			if error == vrep.simx_return_ok:
				self.motor_handlers.append(vrep_motor_handler)
			else:
				print('Error getting motor handlers, ERR: ' + str(error))
				return


def main():
	vrep.simxFinish(-1) 
	# Connect to V-REP via sockets
	clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
	if clientID == -1:
		print ('Failed connecting to remote API server')
		return -1	
	print ('Connected to remote API server')

	# Now try to retrieve data in a blocking fashion (i.e. a service call):
	res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking)

	# Now retrieve streaming data (i.e. in a non-blocking fashion):
	vrep.simxGetIntegerParameter(clientID, vrep.get_joint_state, vrep.simx_opmode_streaming) # Initialize streaming

	# Now send some data to V-REP in a non-blocking fashion:
	vrep.simxAddStatusbarMessage(clientID,'Python training script have been connected.',vrep.simx_opmode_oneshot)

	# Before closing the connection to V-REP, make sure that the last command sent out had time to arrive. You can guarantee this with (for example):
	vrep.simxGetPingTime(clientID)

	# Now close the connection to V-REP:
	vrep.simxFinish(clientID)
	return 1
