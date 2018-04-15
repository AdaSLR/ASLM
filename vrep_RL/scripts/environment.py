from v-rep.lib import vrep
import numpy as np
import time


class VREPEnv(object):
	"""
	Class that implements all the methods for correct 
	reinforcement learning algorithms research using V-REP.
	"""

	def __init__(self, clientID):
		self.client_id = clientID
		self._low_degrees_bound = 0
		self._low_radians_bound = 0
		self._high_degrees_bound = 180
		self._high_radians_bound = np.pi
		self.camera_handlers = []
		# Get cameras from V-REP
		# vs_0 - global view,
		# vs_1 - details basket,
		# vs_2 - destination basket,
		for i in range(3):
			err, handler = vrep.simxGetObjectHandle(self.client_id, 'vc_' + str(i), vrep.simx_opmode_oneshot_wait)
			if err == vrep.simx_return_ok:
				self.camera_handlers.append(handler)
			else:
				print('Error getting camera handlers, ERR:', err)
				return
