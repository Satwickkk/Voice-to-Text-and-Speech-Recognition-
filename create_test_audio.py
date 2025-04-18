from gtts import gTTS
import os

def create_test_audio(text, output_file="test_audio.mp3", language="en-US", rate=150, volume=0.9):
    """
    Create an audio file from text using Google Text-to-Speech.
    
    Args:
        text (str): The text to convert to speech
        output_file (str): Path to save the audio file (default: "test_audio.mp3")
        language (str): Language code (e.g., "en-US", "es-ES") (default: "en-US")
        rate (int): Speech rate in words per minute (default: 150)
        volume (float): Volume level between 0.0 and 1.0 (default: 0.9)
    
    Returns:
        str: Path to the created audio file
    """
    try:
        # Extract the language code (e.g., "en" from "en-US")
        lang_code = language.split('-')[0]
        
        # Create the gTTS object
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
        
        # Save the audio file
        tts.save(output_file)
        
        return output_file
        
    except Exception as e:
        raise Exception(f"Error creating audio file: {str(e)}")

if __name__ == "__main__":
    # Test the function with sample text
    sample_text = "This is a test of the text to speech functionality. If you can hear this, it's working correctly!"
    result = create_test_audio(sample_text)
    print(f"Audio file created successfully: {result}") 