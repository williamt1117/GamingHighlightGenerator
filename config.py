class MainConfig:
    def __init__(self):
        self.inputDirectory = "Data/InputClips" # Directory to scan for input videos
        self.outputDirectory = "Data/OutputHighlights" # Directory to save generated highlight clips
        self.tempDirectory = "Data/Temp" # Directory for ffmpeg temporary files (keep on the same drive as input/output)

        self.predateFileName = "VALORANT_" # Prefix for output filenames before the date
        self.postdateFileName = "" # Suffix for output filenames after the date and before the counter for duplicates
        #this can be swapped for any regex that you want added to the filename of the output clips.
        self.dateRegex = "\d{4}\.\d{2}\.\d{2}" # Regex pattern to extract date from filename

class AudioDetectorConfig:
    def __init__(self):
        self.peakDbThreshold = -9.8 # Trigger when frame peak is at or above this dBFS level
        self.crestDbThreshold = 11 # Trigger when peak minus RMS exceeds this many dB
        self.frameLength = 2048 # Analysis frame size in samples
        self.hopLength = 512 # Hop size between analysis frames in samples
        self.sr = 16000 # Sample rate for audio processing

class KillDetectorConfig:
    def __init__(self):
        self.threshold = 0.006 # Ratio of matching pixels to total pixels to consider a kill    detected
        self.sampleFrequency = 2.0 # Frequency for sampling frames for kill detection
        self.lowerHSV = [30, 90, 170] # Lower bound of HSV values for kill feed highlight color
        self.upperHSV = [40, 170, 255] # Upper bound of HSV values for kill feed highlight color

        self.killFeedOriginalWidth = 2560 # Original width of video used for kill feed region calculation
        self.killFeedOriginalHeight = 1440 # Original height of video used for kill feed region calculation
        self.killFeedX1 = 1846 # X1 coordinate of kill feed region in original resolution
        self.killFeedY1 = 118 # Y1 coordinate of kill feed region in original resolution
        self.killFeedX2 = 2257 # X2 coordinate of kill feed region in original resolution
        self.killFeedY2 = 348 # Y2 coordinate of kill feed region in original resolution

class ClipWindowCreatorConfig:
    def __init__(self):
        self.preKillDuration = 4.5 # Amount of seconds to include before a kill event
        self.postKillDuration = 2.5 # Amount of seconds to include after a kill event
        self.preAudioSpikeDuration = 6.0 # Amount of seconds to include before an audio spike
        self.postAudioSpikeDuration = 3.0 # Amount of seconds to include after an audio spike

class TimelineMergerConfig:
    def __init__(self):
        self.mergeThreshold = 5.5 # Maximum gap in seconds between clips to consider for merging