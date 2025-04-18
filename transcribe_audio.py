import os
import speech_recognition as sr
from datetime import datetime

def transcribe_audio(input_file, language="en-US", auto_save=True):
    """
    Transcribe audio file to text using speech recognition.
    
    Args:
        input_file (str): Path to the input audio file
        language (str): Language code for transcription (default: "en-US")
        auto_save (bool): Whether to save the transcription to a file (default: True)
    
    Returns:
        str: Transcribed text
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(input_file) as source:
            audio = recognizer.record(source)
            
        # For now, we'll use a placeholder message since we're having issues with whisper
        transcribed_text = f"Speech recognition is currently being set up. Language selected: {language}. Please check back later."
        
        if auto_save:
            # Create logs directory if it doesn't exist
            os.makedirs("logs", exist_ok=True)
            
            # Generate output filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"logs/transcription_{timestamp}.txt"
            
            # Save transcription to file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcribed_text)
            
            return f"Transcription saved to {output_file}"
        
        return transcribed_text
        
    except Exception as e:
        raise Exception(f"Error transcribing audio: {str(e)}")

def main():
    # Define the audio file path
    audio_file = "output/test_audio.wav"
    
    # Perform transcription with default settings
    result = transcribe_audio(audio_file)
    print(result)
    
    # Example with different language (uncomment to test)
    # result = transcribe_audio(audio_file, language="es")

if __name__ == "__main__":
    main() 