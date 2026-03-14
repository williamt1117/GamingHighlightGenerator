import ffmpeg
import librosa
import tempfile
import numpy as np
from config import AudioDetectorConfig

class audioDetector:
    def __init__(self):
        self.config = AudioDetectorConfig()

    def extractAudio(self, videoPath):
        """Extracts audio from the given video file and saves it as a temporary WAV file."""
        tempFile = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        audioPath = tempFile.name

        inputStream = ffmpeg.input(videoPath)
        outputStream = ffmpeg.output(inputStream.audio, audioPath, ac=1, ar=self.config.sr, format='wav')
        outputStream = ffmpeg.overwrite_output(outputStream)
        ffmpeg.run(outputStream, overwrite_output=True, quiet=True)

        return audioPath
    
    def computeLevels(self, audioPath):
        """Computes and returns per-frame peak and RMS levels."""
        y, sr = librosa.load(audioPath, sr=None)

        padded = np.pad(y, self.config.frameLength // 2, mode="constant")
        frames = librosa.util.frame(padded, frame_length=self.config.frameLength, hop_length=self.config.hopLength)

        rms = np.sqrt(np.mean(frames ** 2, axis=0))
        peaks = np.max(np.abs(frames), axis=0)

        eps = 1e-12
        rmsDb = 20 * np.log10(np.maximum(rms, eps))
        peakDb = 20 * np.log10(np.maximum(peaks, eps))
        return peakDb, rmsDb, sr

    def findSpikes(self, peakDb, rmsDb, sr):
        """Finds spikes by peaks and crest factor and return corresponding timestamps."""
        crestDb = peakDb - rmsDb
        spikeFrames = np.where(
            (peakDb >= self.config.peakDbThreshold) &
            (crestDb >= self.config.crestDbThreshold)
        )[0]

        spikeTimes = librosa.frames_to_time(spikeFrames, sr=sr, hop_length=self.config.hopLength)
        return spikeTimes.tolist()

    def detect(self, videoPath):
        """Detects audio spikes in the given video file."""
        audioPath = self.extractAudio(videoPath)
        peakDb, rmsDb, sr = self.computeLevels(audioPath)
        spikeTimes = self.findSpikes(peakDb, rmsDb, sr)
        return spikeTimes