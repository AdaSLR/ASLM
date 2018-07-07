import cv2
import numpy as np
import time
from skimage.measure import compare_ssim

class ChangesDetector(object):
    """Class to detect and show changes in empty basket."""
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=5)

    def read_image(self, image, time):
        """Read image from directory with interval.

        Parameters:
        -----------
                image : string, array
                Path or certain image for reading

                time: int, float
                Time for waiting robot's cicle

        """

        time.sleep(time)
        return cv2.imread(path)

    def get_similarity(self, X, Y, method='ssim'):
        """Find measure of similarity betwen two images

        Parameters:
        -----------
                X : array
                Original image

                Y : array
                Changed image

                method : string
                Method for count similarity:
                    - 'ssim'
                    - 'corr'
        """

        if method == 'ssim':

            scores, diff = compare_ssim(X, Y, full=True)
            diff = (diff * 255).astype('uint8')
            return scores, diff
        else if method == 'corr':
            return np.corrcoef(np.asarray(arr_1) + 0.01, np.asarray(arr_2) + 0.01)

    def preprocess_frame(self, frame, _image):
        """Preprocess image for further operations

        Parameters:
        -----------
                frame : array
                Image for preprocessing

                _image : bool
                Determines the processing method
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not _image:
            frame = self.fgbg.apply(frame)

        frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        return frame

    def create_bboxes(self, frame):
        """Show bounding boxes around new detail in basket

        Parameters:
        -----------
                frame : array
                Image for bbox operation
        """
        frame_c = frame[:]
        _, threshold = cv2.threshold(frame_c, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        counturs = cv2.findContours(threshold[:], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counturs = counturs[1]
        for c in counturs:
            [x, y, w, h] = cv2.boundingRect(c)
            cv2.rectangle(frame_c, (x, y), (x + w, y + h), (0, 0, 255), 2)
        return frame_c

    def get_reward(self, sim, treshold=0.675):
        """Placeholder for reward function

        Parameters:
        -----------
                sim : float
                Measure of similarity

                threshold : float
                Threshold for current similarity method

        """
        return 1 if corr < treshold else 0

    def identify_changes_images(self, frame, prev_frame):
        """Final method to identify changes between two frames

        Parameters:
        -----------
                frame : string, array
                Path or certain array-like current frame

                prev_frame : string, array
                Path or certain array-like previous frame
        """
        frame = self.read_image(path, time)
        frame = preprocess_frame(frame)
        prev_frame = self.read_image(path, time=0)
        prev_frame = self.preprocess_frame(prev_frame)
        return get_similarity(frame, prev_frame)

    def read_video_frame(self):
        """Read video-frames"""
        _, frame = self.cap.read()
        return frame

    def identify_changes_video(self, n_of_frame=30, return_reward=False, show=False):
        """Final method to identify changes between two frames

        Parameters:
        -----------
                frame : string, array
                Path or certain array-like current frame

                prev_frame : string, array
                Path or certain array-like previous frame

                n_of_frame : int
                Number of frames before taking a new one

                return_reward : bool
                If true print current get_reward

                show : bool
                If true show video stream
        """
        # take the first frame
        prev_frame = self.read_video_frame()
        prev_frame = self.preprocess_frame(prev_frame)
        k = 0
        while True:
            frame = self.read_video_frame()
            frame = self.preprocess_frame(frame)

            # Caoture and hold the prev frame
            if prev_frame is not None and k % n_of_frame == 0:
                prev_frame = frame
                k = 0
                corr = self.get_similarity(frame, prev_frame)
            k += 1

            corr = np.mean(corr)

            if show:
                cv2.imshow('frame',frame)
                cv2.imshow('prev_frame', prev_frame)

            # Return reward if there are  changes between frames
            if return_reward:
                print(corr)
                print(self.get_reward(corr))

            # Close the windows
            if cv2.waitKey(100) and 0xFF == ord('q'):
                break

if __name__ == '__main__':
    ch = ChangesDetector()
    ch.identify_changes_video(return_reward=True, show=True)

#cv2.destroyWindow()
#cv.release()
