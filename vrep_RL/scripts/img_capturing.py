import cv2
import time
import numpy as np
from lib import vrep
from environment import VREPEnv

def main():
	env = VREPEnv()
	print(env.camera_handlers)
	time.sleep(2)
	if(env.conn_handler != -1):
		err, res, img = vrep.simxGetVisionSensorImage(env.conn_handler, env.camera_handlers[0], 0, vrep.simx_opmode_streaming)
		while(vrep.simxGetConnectionId(env.conn_handler) != -1):
			# Set random pos
			pos = []
			for i in range(4):
				pos.append(np.random.randint(0,180))
			pos.append(np.random.randint(2))
			env.step('uarm', pos)
			
			# Get image from vision sensor
			err, res, image = vrep.simxGetVisionSensorImage(env.conn_handler, env.camera_handlers[0], 0, vrep.simx_opmode_buffer)
			if err == vrep.simx_return_ok:
				print('Received image')
				print(res)
				img = np.array(image, dtype=np.uint8)
				img.resize([res[1], res[0], 3])
				cv2.imshow('image', img)
				# Some magic stuff for correct image rendering
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			elif err == vrep.simx_return_novalue_flag:
				print('No image received')
				pass
			else:
				print('Error while receiving image: ', err)
	else:
		print('Failed to connect to remote API server')
		env.finish()

	cv2.destroyAllWindows()

if __name__=="__main__":
	main()
	
