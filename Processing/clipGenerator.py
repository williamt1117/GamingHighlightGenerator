import ffmpeg

class clipGenerator:
    def __init__(self):
        pass

    def _run(self, stream):
        try:
            ffmpeg.run(stream, overwrite_output=True, capture_stdout=True, capture_stderr=True)
        except ffmpeg.Error as exc:
            stderr = exc.stderr.decode("utf-8", errors="replace").strip() if exc.stderr else "Unknown ffmpeg error"
            raise RuntimeError(f"ffmpeg failed: {stderr}") from exc

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