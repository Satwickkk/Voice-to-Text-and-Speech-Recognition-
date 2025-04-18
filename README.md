# Simple Text to Speech Converter

A simple Python-based text-to-speech converter that uses Google's Text-to-Speech (gTTS) service.

## Requirements

- Python 3.6 or higher
- gTTS package

## Installation

1. Make sure you have Python installed on your system
2. Install the required package:
   ```
   pip install gTTS
   ```

## Usage

1. Run the script:
   ```
   python text_to_speech.py
   ```

2. Enter the text you want to convert to speech when prompted
3. The audio file will be saved in the `output` directory
4. Type 'quit' to exit the program

## Features

- Converts text to speech using Google's Text-to-Speech service
- Saves audio files in MP3 format
- Creates unique filenames using timestamps
- Supports multiple languages (default is English)

## Output

All generated audio files are saved in the `output` directory with filenames in the format:
`speech_YYYYMMDD_HHMMSS.mp3`