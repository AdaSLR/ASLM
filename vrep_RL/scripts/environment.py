from lib import vrep
import numpy as np
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
		self.conn_handler = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)
		if self.conn_handler == -1:
			print('Failed connecting to the remote API server')
			return -1
		print('Succesfully connected to the renote API server...')

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
