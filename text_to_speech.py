import os
from gtts import gTTS
from datetime import datetime

def text_to_speech(text, language='en'):
    """
    Convert text to speech and save as an audio file.
    
    Args:
        text (str): The text to convert to speech
        language (str): The language code (default: 'en' for English)
    
    Returns:
        str: Path to the generated audio file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')
        
        # Generate unique filename using timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'output/speech_{timestamp}.mp3'
        
        # Create gTTS object and save to file
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_file)
        
        print(f"Audio file saved successfully: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"Error converting text to speech: {str(e)}")
        return None

def main():
    # Example usage
    print("Text to Speech Converter")
    print("-" * 30)
    
    while True:
        # Get text input from user
        text = input("\nEnter text to convert to speech (or 'quit' to exit): ")
        
        if text.lower() == 'quit':
            break
            
        if text.strip():
            # Convert text to speech
            audio_file = text_to_speech(text)
            
            if audio_file:
                print(f"\nYou can find your audio file at: {audio_file}")
        else:
            print("Please enter some text!")

if __name__ == "__main__":
    main() 