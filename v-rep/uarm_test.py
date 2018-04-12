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
		self.client_id = client_id
		self.motors_number = 4
		self.motor_handlers = []
		for i in range(0, self.motors_number):
			error, vrep_motor_handler = vrep.simxGetObjectHandle(self.client_id, 'uarm_motor' + str(i+1), vrep.simx_opmode_oneshot_wait)
			if error == vrep.simx_return_ok:
				self.motor_handlers.append(vrep_motor_handler)
			else:
				print('Error getting motor handlers, ERR: ' + str(error))
				return

	
	def set_motors(self, position, degrees=False):
		"""
		Set values of the UARM's motors.
		
		Arguments: 	positions - list containing angular positions for all motors: 
					positions = [joint_val_1, ..., joint_val_4] 
					degrees - if given positions are in degress (True) or radians (False)
		"""
		# Recalculate into radians if positions are in degrees
		if degrees:
			coeff = np.pi/180
			position = [pos * coeff for pos in position]
		vrep.simxPauseCommunication(self.client_id, True)
		errors = []
		for i in range(0, self.motors_number):
			code = vrep.simxSetJointTargetPosition(self.client_id, self.motor_handlers[i], position[i], vrep.simx_opmode_oneshot)
			errors.append(code)
		vrep.simxPauseCommunication(self.client_id, False)
		

def main():
	vrep.simxFinish(-1) 
	# Connect to V-REP via sockets
	clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
	if clientID == -1:
		print ('Failed connecting to remote API server')
		return -1	
	print ('Connected to remote API server')

	#vrep.simxAddStatusbarMessage(clientID,'Python training script have been connected.',vrep.simx_opmode_oneshot)
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
