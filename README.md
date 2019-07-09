# gregarious-wolf

## Misc. notes
1. `Python 3.6` recommended but tbd, pyaudio and some other stuff might not work.
2. The VSCode linter doesn't seem to like `opencv-python` or `cv2` (just a heads up).

## Speech to text
- `$cd audio-analysis`
### Input a youtube url - outputs the speech to text with timestamps
- `python youtube-extraction.py`
### Input an audio file - outputs the amplitude analysis
- `python amplitude-analysis.py`

## Frame detection
- `$cd frame-detection`
- `python smile-detection.py`

## Demofile parsing instructions 
- Download an test .demo file from https://www.hltv.org/matches
- Extract dem file from download
- `cd demofile-parsing`
- run `npm install`
- Edit `parse_demo.js` to point to path of downloaded .dem
- run `node parse_demo.js`
