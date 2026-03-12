from config import ClipWindowCreatorConfig
from enum import Enum

class ClipType(Enum):
    KILL = 1
    AUDIO = 2

class clipWindowCreator:
    def __init__(self):
        self.config = ClipWindowCreatorConfig()

    def createWindow(self, timestamp, clipType):
        """Creates a clip window around the given timestamp based on the clip type."""
        if clipType == ClipType.KILL:
            start = max(0, timestamp - self.config.preKillDuration)
            end = timestamp + self.config.postKillDuration
            return [start, end]
        elif clipType == ClipType.AUDIO:
            start = max(0, timestamp - self.config.preAudioSpikeDuration)
            end = timestamp + self.config.postAudioSpikeDuration
            return [start, end]
        else:
            raise ValueError("Invalid clip type specified.")