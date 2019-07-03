# gregarious-wolf

## Quickstart
1. `Python 3.6` recommended but tbd, pyaudio and some other stuff might not work.
2. The VSCode linter doesn't seem to like `opencv-python` or `cv2` (just a heads up).

## Speech to text
- `cd <project>`
- `python youtube-extraction.py`

## Smile detection
- `python smile-detection.py`

## Demofile parsing instructions 
- Download an test .demo file from https://www.hltv.org/matches
- Extract dem file from download
- `cd demofile-parsing`
- run `npm install`
- Edit `parse_demo.js` to point to path of downloaded .dem
- run `node parse_demo.js`