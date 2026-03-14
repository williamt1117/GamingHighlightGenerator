from config import MainConfig
from Detector.audioDetector import audioDetector
from Detector.killDetector import killDetector
from Processing.clipWindowCreator import clipWindowCreator, ClipType
from Processing.timelineMerger import timelineMerger
from Processing.clipGenerator import clipGenerator

import os
import re
from pathlib import Path

if __name__ == "__main__":
    audiodetector = audioDetector()
    killdetector = killDetector()
    windowCreator = clipWindowCreator()
    merger = timelineMerger()
    clipGenerator = clipGenerator()
    config = MainConfig()

    #iterate through all files in the input directory and process them
    for filename in os.listdir(config.inputDirectory):
        if not filename.endswith(".mp4"):
            continue

        inputFile = config.inputDirectory + "/" + filename

        audioSpikeTimes = audiodetector.detect(inputFile)
        print(f"Detected audio spikes at times: {audioSpikeTimes}")
        killTimes = killdetector.detect(inputFile)
        print(f"Detected kills at times: {killTimes}")

        audioClipWindows = [windowCreator.createWindow(t, ClipType.AUDIO) for t in audioSpikeTimes]
        killClipWindows = [windowCreator.createWindow(t, ClipType.KILL) for t in killTimes]
        timelines = audioClipWindows + killClipWindows

        mergedTimeline = merger.mergeTimelines(timelines)

        #extract date from filename of format VALORANT_replay_YYYY.MM.DD-HH.MM.mp4
        date = re.search(config.dateRegex, filename)
        date = date.group(0) if date else "UnknownDate"

        if len(mergedTimeline) == 0:
            print(f"No highlight windows detected for {filename}.")
            continue

        counter = 1
        outputFile = config.outputDirectory + f"/{config.predateFileName}{date}{config.postdateFileName}_{counter:02d}.mp4"
        while Path(outputFile).exists():
            counter += 1
            outputFile = config.outputDirectory + f"/{config.predateFileName}{date}{config.postdateFileName}_{counter:02d}.mp4"

        generatedFile = clipGenerator.generateClip(inputFile, mergedTimeline, outputFile)
        if generatedFile:
            print(f"Generated clip for {filename} at {generatedFile}")