from config import MainConfig
from Detector.audioDetector import audioDetector
from Detector.killDetector import killDetector
from Processing.clipWindowCreator import clipWindowCreator, ClipType
from Processing.timelineMerger import timelineMerger
from Processing.clipGenerator import clipGenerator

if __name__ == "__main__":
    audiodetector = audioDetector()
    killdetector = killDetector()
    windowCreator = clipWindowCreator()
    merger = timelineMerger()
    clipGenerator = clipGenerator()
    config = MainConfig()

    inputFile = config.inputDirectory + "/VALORANT_replay_2026.02.27-14.49.mp4"

    audioSpikeTimes = audiodetector.detect(inputFile)
    print("Detected audio spikes at times (in seconds):", audioSpikeTimes)
    
    killTimes = killdetector.detect(inputFile)
    print("Detected kills at times (in seconds):", killTimes)


    audioClipWindows = [windowCreator.createWindow(t, ClipType.AUDIO) for t in audioSpikeTimes]
    killClipWindows = [windowCreator.createWindow(t, ClipType.KILL) for t in killTimes]
    timelines = audioClipWindows + killClipWindows

    mergedTimeline = merger.mergeTimelines(timelines)
    print("Merged clip windows (start, end) in seconds:", mergedTimeline)

    outputFile = config.outputDirectory + "/temp.mp4"
    clipGenerator.generateClip(inputFile, mergedTimeline, outputFile)