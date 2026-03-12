import ffmpeg
import tempfile
from pathlib import Path

class clipGenerator:
    def __init__(self):
        pass

    def generateClip(self, videoPath, timelines, outputPath):
        """Generates a stitched clip of the specified timelines into one clip."""
        subclips = []
        for start, end in timelines:
            subclip = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name

            inputStream = ffmpeg.input(videoPath, ss=start, to=end)
            outputStream = ffmpeg.output(inputStream, subclip, c="copy")
            outputStream = ffmpeg.overwrite_output(outputStream)
            ffmpeg.run(outputStream, quiet=True)

            subclips.append(subclip)

        if len(subclips) == 0:
            return None
        
        concatFile = tempfile.NamedTemporaryFile(mode="w", delete=False)

        for subclip in subclips:
            concatFile.write(f"file '{subclip}'\n")
        concatFile.close()

        inputStream = ffmpeg.input(concatFile.name, format='concat', safe=0)
        outputStream = ffmpeg.output(inputStream, outputPath, c="copy")
        outputStream = ffmpeg.overwrite_output(outputStream)
        ffmpeg.run(outputStream, quiet=True)