import ffmpeg
import os
import subprocess

class clipGenerator:
    def __init__(self, tempDir=None):
        self._tempDir = tempDir

    def _run(self, stream):
        env = None
        if self._tempDir:
            os.makedirs(self._tempDir, exist_ok=True)
            env = {**os.environ, "TMPDIR": self._tempDir}
        try:
            cmd = ffmpeg.compile(stream, overwrite_output=True)
            completed = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                check=False,
            )
            if completed.returncode != 0:
                stderr = completed.stderr.decode("utf-8", errors="replace").strip() if completed.stderr else "Unknown ffmpeg error"
                raise RuntimeError(f"ffmpeg failed: {stderr}")
        except FileNotFoundError as exc:
            raise RuntimeError("ffmpeg binary not found in PATH") from exc

    def generateClip(self, videoPath, timelines, outputPath):
        """Generates a stitched clip of the specified timelines into one clip."""
        validTimelines = [(float(start), float(end)) for start, end in timelines if end > start]
        if len(validTimelines) == 0:
            return None

        concatInputs = []
        for start, end in validTimelines:
            inputStream = ffmpeg.input(videoPath, ss=start, t=end - start)
            concatInputs.extend([inputStream.video, inputStream.audio])

        joinedStreams = ffmpeg.concat(*concatInputs, v=1, a=1, n=len(validTimelines)).node
        outputStream = ffmpeg.output(
            joinedStreams[0],
            joinedStreams[1],
            outputPath,
            vcodec="libx264",
            acodec="aac",
            preset="veryfast",
            crf=18,
            movflags="+faststart",
        )
        self._run(outputStream)
        return outputPath