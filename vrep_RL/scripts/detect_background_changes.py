import cv2
import numpy as np

cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2(history=5)

def get_frame():
    #Preprocess frames
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = fgbg.apply(frame)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    return frame

def reward_placeholder(corr, treshold=0.675):
    return 1 if corr < treshold else 0

def identify_changes(n_of_frame=30, return_reward=False, show=False):
    #take the first frame
    prev_frame = get_frame()
    k = 0
    while True:
        frame = get_frame()

        # Caoture and hold the prev frame
        if prev_frame is not None and k % n_of_frame == 0:
            prev_frame = frame
            k = 0
            corr = np.corrcoef(np.asarray(frame) + 0.01, np.asarray(prev_frame) + 0.01)
        k += 1

        corr = np.mean(corr)

        if show:
            cv2.imshow('frame',frame)
            cv2.imshow('prev_frame', prev_frame)

        # Return reward if there are  changes between frames
        if return_reward:
            print(corr)
            print(reward_placeholder(corr))

        # Close the windows
        if cv2.waitKey(100) and 0xFF == ord('q'):
            break

if __name__ == '__main__':
    identify_changes(return_reward=True, show=True)

#cv2.destroyWindow()
#cv.release()
