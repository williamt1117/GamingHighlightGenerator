# Gaming Highlight Generator by Pixel and Audio Detection

This project aims to serve as a one-pass storage space reduction for generic gaming recordings by filtering out dead space in the recordings.

## Description

This application works by scanning MP4 recordings for specific video and audio cues and creating a condensed highlight reel. Two detectors run in parallel on each input file:

- **Audio Detector** — extracts mono 16 kHz audio with ffmpeg, then uses librosa to compute per-frame peak dBFS and crest factor. Frames exceeding both thresholds are flagged as significant audio events like loud speech, laughs, or heavy gunfire.
- **Kill Detector** — samples frames via OpenCV and checks the kill feed region for the characteristic highlight color using HSV masking.

Detected event timestamps are expanded into clip windows with configurable pre/post padding, overlapping or nearby windows are merged, and ffmpeg stitches the final highlight using a concat filter.

### Dependencies

- Python 3.10+
- ffmpeg (must be on system PATH)
- ffmpeg-python
- librosa
- numpy
- opencv-python

### Installing

1. Install ffmpeg system-wide (e.g. `sudo apt install ffmpeg` on Ubuntu).
2. Install python dependencies: `pip3 install ffmpeg-python librosa numpy opencv-python`.
3. Adjust detection and I/O parameters in `config.py` as needed.

### Executing

1. Place `.mp4` recordings in specified input directory (default `Data/InputClips`).
2. Run: `python3 main.py`.
3. Highlight clips will be written to specified output directory (default `Data/OutputHighlights`).

## Future Work

* Expand kill detection to more games (Currently tuned for VALORANT recordings).
