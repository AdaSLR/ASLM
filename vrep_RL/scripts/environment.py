from lib import vrep
from uarm import UARM
import numpy as np
import cv2
import time


class VREPEnv(object):
	"""
	Class that implements all the methods for correct 
	reinforcement learning algorithms research using V-REP.
	"""

	def __init__(self):
		self._low_degrees_bound = 0
		self._low_radians_bound = 0
		self._high_degrees_bound = 180
		self._high_radians_bound = np.pi
		# Get client id from the V-REP server-side
		vrep.simxFinish(-1)
		self.conn_handler = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
		if self.conn_handler == -1:
			print('Failed connecting to the remote API server')
			return -1
		print('Succesfully connected to the remote API server...')

		# Get UARM entity
		# Implemented it in the dict style for future purposes
		# (if there're several robots in the env, call them like 
		# env.robot['uarm'], env.robot['universal_robotics'], etc) 
		uarm = UARM(self.conn_handler)
		self.robot = {'uarm': uarm}	

		# Get cameras from V-REP
		# vs_0 - global view,
		# vs_1 - details basket,
		# vs_2 - destination basket,
		self.camera_handlers = []
		for i in range(3):
			err, handler = vrep.simxGetObjectHandle(self.conn_handler, 'vs_' + str(i), vrep.simx_opmode_oneshot_wait)
			if err == vrep.simx_return_ok:
				self.camera_handlers.append(handler)
			else:
				print('Error getting camera handlers, ERR:', err)
				return


	def state(self, degrees=True):
		_state = []
		# Get motors' positions
		for motor in self.robot['uarm'].motor_handlers:
			err, joint_position = vrep.simxGetJointPosition(self.conn_handler, motor, vrep.simx_opmode_streaming)
			if err == vrep.simx_return_ok or err == vrep.simx_return_novalue_flag:
				joint_position *= 180.0/np.pi 
				_state.append(round(joint_position, 4))
			else:
				print('Error getting joint positions, ERR:', err)
				return -1
		
		# Get gripper state
		err, gripper_state = vrep.simxGetIntegerSignal(self.conn_handler, 
				self.robot['uarm'].gripper_handler, 
				vrep.simx_opmode_streaming)
		if err == vrep.simx_return_ok or err == vrep.simx_return_novalue_flag:
			_state.append(gripper_state)
		else:
			print('Error getting gripper state, ERR:', err)
			_state.append(-1)
		return _state


	def step(self, entity, action):
		# Set action to the given entity
		pos = action[:-1]
		grip = action[-1]
		self.robot[entity].set_motors(position=pos, degrees=True)
		self.robot[entity].grip() if grip else self.robot[entity].ungrip()
		
		# Return reward
		

	def finish(self):
		vrep.simxFinish(self.conn_handler)

