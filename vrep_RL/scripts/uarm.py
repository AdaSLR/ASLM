from lib import vrep
import numpy as np

class UARM(object):
	def __init__(self, connection_handler):
		""" Get all V-REP handlers for the UARM manipulator
		
		Arguments:
			connection_handler -- handler containing connection identificator with server-side V-REP
		"""		

		self.conn_handler = connection_handler
		self.motors_number = 4
		self.motor_handlers = []
		self.gripper_handler = None
		for i in range(0, self.motors_number):
			error, vrep_motor_handler = vrep.simxGetObjectHandle(self.conn_handler, 'uarm_motor' + str(i+1), vrep.simx_opmode_oneshot_wait)
			if error == vrep.simx_return_ok:
				self.motor_handlers.append(vrep_motor_handler)
			else:
				print('Error getting motor handlers, ERR: ' + str(error))
				return
		self.gripper_handler = 'uarm_suctionCup'
	

	def grip(self):
		""" Enables UARM's gripper
		"""

		err = vrep.simxSetIntegerSignal(self.conn_handler, self.gripper_handler, 1, vrep.simx_opmode_oneshot)
		if err != vrep.simx_return_ok: #or err != vrep.simx_return_novalue_flag:
			print('Error while gripping, ERR: ', err)


	def ungrip(self):
		""" Disables UARM's gripper
		"""
		err = vrep.simxSetIntegerSignal(self.conn_handler, self.gripper_handler, 0, vrep.simx_opmode_oneshot)
		if err != vrep.simx_return_ok:
			print('Error while gripping, ERR: ', err)


	def set_motors(self, position, degrees=False):
		""" Set values of the UARM\'s motors.
        
		Arguments:  
			positions - list containing angular positions for all motors: 
						positions = [joint_val_1, ..., joint_val_4] 
			degrees -- if given positions are in degress (True) or radians (False)
		"""

		# Recalculate into radians if positions are in degrees
		if degrees:
			coeff = np.pi/180
			position = [pos * coeff for pos in position]
		vrep.simxPauseCommunication(self.conn_handler, True)
		errors = []
		for i in range(0, self.motors_number):
			code = vrep.simxSetJointTargetPosition(self.conn_handler, self.motor_handlers[i], position[i], vrep.simx_opmode_oneshot)
			errors.append(code)
		vrep.simxPauseCommunication(self.conn_handler, False)
