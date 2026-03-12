import cv2
import numpy as np
from config import KillDetectorConfig

class killDetector:
    def __init__(self):
        self.config = KillDetectorConfig()
        self.lowerHSV = np.array(self.config.lowerHSV, dtype=np.uint8)
        self.upperHSV = np.array(self.config.upperHSV, dtype=np.uint8)

    def calculateKillFeedWindow(self, cap):
        """Calculates the kill feed window based on the first frame of the video."""

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        x1 = int((self.config.killFeedX1 / self.config.killFeedOriginalWidth) * width)
        y1 = int((self.config.killFeedY1 / self.config.killFeedOriginalHeight) * height)
        x2 = int((self.config.killFeedX2 / self.config.killFeedOriginalWidth) * width)
        y2 = int((self.config.killFeedY2 / self.config.killFeedOriginalHeight) * height)
        return (x1, y1, x2, y2)
            

    def detect(self, videoPath):
        """Detects kills in the given video file by pattern matching and returns timestamps."""

        cap = cv2.VideoCapture(videoPath)
        fps = cap.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            raise ValueError("Could not determine FPS of the video.")

        x1, y1, x2, y2 = self.calculateKillFeedWindow(cap)

        frameSkip = max(1, int(fps / self.config.sampleFrequency))

        timestamps = []
        for frameNum in range(0, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), frameSkip):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frameNum)
            ret, frame = cap.read()

            if not ret:
                break

            region = frame[y1:y2, x1:x2]
            hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, self.lowerHSV, self.upperHSV)
            matchingPixels = np.count_nonzero(mask)
            totalPixels = mask.size

            if matchingPixels / totalPixels > self.config.threshold:
                timestamp = frameNum / fps
                timestamps.append(timestamp)

        cap.release()
        return timestamps