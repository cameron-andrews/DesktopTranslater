# DesktopTranslater - Screen Capture App with PyQt6
This Python application, developed using PyQt6, allows users to capture a specified area of the screen, which is then displayed in a transparent window.
## Original Intent

The primary goal of this application was to facilitate the translation of videos with Mandarin subtitles that lacked corresponding English and Pinyin subtitles. The envisioned workflow included translating the content and exporting the newly acquired language data to Anki or reviewing it in the history.
## Current Features

As it stands, the application enables users to select and translate a specific area of the screen. Additionally, there is a "Start" button that initiates continuous translation for the selected screen area, suitable for video playback.
## Project Evolution

During testing, particularly with live video content, it became evident that achieving accurate live translation would necessitate predicting the next subtitle to maintain precision. Given this limitation, the project has been put on hold. A more viable approach might involve exploring integration with browser/video translation features or utilizing translation APIs if not directly embedded.

Feel free to explore and adapt the application based on your specific needs!

## Dependencies

- PyQt6
- Pillow (PIL)
- NumPy
- OpenCV
- Googletrans
- Pytesseract(needs a local path set currently)
