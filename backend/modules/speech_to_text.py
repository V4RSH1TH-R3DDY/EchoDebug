import base64
import os
import tempfile
from typing import Optional
from openai import OpenAI

def transcribe_audio(audio_data: str, format: str = "wav") -> str:
    """
    Convert audio to text using OpenAI Whisper API.
    
    Args:
        audio_data: Base64 encoded audio
        format: Audio format (wav, flac, mp3, etc.)
    
    Returns:
        Transcribed text
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        # Fallback to mock for testing
        return "find all syntax errors in main.py"
    
    try:
        # Decode audio data
        audio_bytes = base64.b64decode(audio_data)
        
        # Create temporary file for Whisper API
        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = temp_file.name
        
        try:
            # Call OpenAI Whisper API
            client = OpenAI(api_key=api_key)
            
            with open(temp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"  # Can be auto-detected by omitting this
                )
            
            return transcript.text.strip()
        
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        raise Exception(f"STT error: {str(e)}")

def transcribe_audio_file(file_path: str) -> str:
    """
    Transcribe audio from file path.
    
    Args:
        file_path: Path to audio file
    
    Returns:
        Transcribed text
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        return "find all syntax errors in main.py"
    
    try:
        client = OpenAI(api_key=api_key)
        
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
        
        return transcript.text.strip()
    
    except Exception as e:
        raise Exception(f"STT error: {str(e)}")
