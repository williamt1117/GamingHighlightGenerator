import ffmpeg
import librosa
import tempfile
import numpy as np
from config import AudioDetectorConfig

class audioDetector:
    def __init__(self):
        self.config = AudioDetectorConfig()
        self.threshold = self.config.threshold
        self.sr = self.config.sr

    def extractAudio(self, videoPath):
        """Extracts audio from the given video file and saves it as a temporary WAV file."""
        tempFile = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audioPath = tempFile.name

        inputStream = ffmpeg.input(videoPath)
        outputStream = ffmpeg.output(inputStream.audio, audioPath, ac=1, ar=self.sr, format='wav')
        outputStream = ffmpeg.overwrite_output(outputStream)
        ffmpeg.run(outputStream, overwrite_output=True, quiet=True)

        return audioPath
    
    def computeRms(self, audioPath):
        """Computes root mean square for the audio file and returns alongside sample rate"""
        y, sr = librosa.load(audioPath, sr=None)
        rms = librosa.feature.rms(y=y)[0]
        return rms, sr
    
    def findSpikes(self, rms, sr):
        """Finds audio spikes based on RMS values and sample rate."""
        mean = np.mean(rms)
        std = np.std(rms)
        
        threshold = mean + self.threshold * std
        spikeFrames = np.where(rms > threshold)[0]
        spikeTimes = librosa.frames_to_time(spikeFrames, sr=sr)
        return spikeTimes.tolist()

    def detect(self, videoPath):
        """Detects audio spikes in the given video file."""
        audioPath = self.extractAudio(videoPath)
        rms, sr = self.computeRms(audioPath)
        spikeTimes = self.findSpikes(rms, sr)
        return spikeTimes