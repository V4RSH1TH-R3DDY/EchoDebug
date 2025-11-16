#!/usr/bin/env python3
"""
Simple voice recorder for EchoDebug
Records audio from microphone and sends to API
"""

import sounddevice as sd
import soundfile as sf
import requests
import numpy as np
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Configuration
SAMPLE_RATE = 16000  # Whisper works best with 16kHz
DURATION = 5  # seconds
API_URL = "http://localhost:8000"

def record_audio(duration=5):
    """Record audio from microphone with visual feedback"""
    print(f"\n🎙️  Recording for {duration} seconds...")
    print("   Speak your command now!")
    print("\n   ", end='', flush=True)
    
    # Record audio
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    
    # Show progress bar while recording
    import time
    for i in range(duration):
        print("🔴", end=' ', flush=True)
        time.sleep(1)
    
    sd.wait()  # Wait until recording is finished
    
    print("\n\n   ✓ Recording complete!")
    
    # Show audio level
    max_volume = np.max(np.abs(audio))
    if max_volume < 0.01:
        print("   ⚠️  Warning: Very low audio detected. Speak louder!")
    elif max_volume > 0.8:
        print("   ⚠️  Warning: Audio might be clipping. Speak softer!")
    else:
        print(f"   ✓ Audio level good ({max_volume:.2f})")
    
    return audio

def save_audio(audio, filename="temp_audio.wav"):
    """Save audio to file"""
    # Use absolute path
    abs_filename = os.path.abspath(filename)
    sf.write(abs_filename, audio, SAMPLE_RATE)
    return abs_filename

def transcribe_audio_file(filename):
    """Send audio file to API for transcription"""
    print(f"\n📤 Sending to Whisper API...")
    
    try:
        response = requests.post(
            f"{API_URL}/stt/file",
            json={"file_path": filename}
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('text', '')
        else:
            print(f"   ❌ API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def parse_intent(text):
    """Parse the transcribed text into an intent"""
    print(f"\n🧠 Parsing intent...")
    
    try:
        response = requests.post(
            f"{API_URL}/intent",
            json={"text": text}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ❌ API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def execute_intent(text):
    """Route the intent and execute"""
    print(f"\n⚡ Executing command...")
    
    try:
        response = requests.post(
            f"{API_URL}/intent/route",
            json={"text": text}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ❌ API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_microphone():
    """Test if microphone is working"""
    print("\n🎤 Testing microphone...")
    print("   Recording 2 seconds of audio...")
    
    try:
        # Record short test
        test_audio = sd.rec(
            int(2 * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='float32'
        )
        
        # Show visual feedback
        import time
        print("   ", end='', flush=True)
        for i in range(2):
            print("🔴", end=' ', flush=True)
            time.sleep(1)
        
        sd.wait()
        
        # Check audio level
        max_volume = np.max(np.abs(test_audio))
        
        print(f"\n\n   ✓ Microphone working!")
        print(f"   Audio level: {max_volume:.3f}")
        
        if max_volume < 0.001:
            print("   ⚠️  No sound detected. Check:")
            print("      - Microphone is plugged in")
            print("      - Microphone permissions are granted")
            print("      - Correct input device is selected")
            return False
        else:
            print("   ✓ Sound detected - microphone is working!")
            return True
            
    except Exception as e:
        print(f"\n   ❌ Microphone error: {e}")
        print("   Make sure you have a microphone connected")
        return False

def main():
    """Main voice command loop"""
    print("\n" + "="*60)
    print("  🎙️  EchoDebug Voice Recorder")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code != 200:
            print("\n❌ Server not running!")
            print("   Start with: python backend/main.py")
            return
    except:
        print("\n❌ Cannot connect to server!")
        print("   Start with: python backend/main.py")
        return
    
    print("\n✓ Server is running")
    
    # Test microphone
    if not test_microphone():
        print("\n❌ Microphone test failed!")
        print("   Fix microphone issues and try again")
        return
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  No OpenAI API key detected")
        print("   Voice transcription will use mock data")
        print("   Add OPENAI_API_KEY to backend/.env for real Whisper\n")
    else:
        print("\n✓ OpenAI API key detected - Whisper enabled\n")
    
    while True:
        print("\n" + "-"*60)
        print("Press ENTER to start recording (or 'q' to quit)")
        user_input = input("> ").strip().lower()
        
        if user_input == 'q':
            print("\n👋 Goodbye!")
            break
        
        # Record audio
        audio = record_audio(duration=DURATION)
        
        # Save to file
        filename = save_audio(audio)
        
        # Transcribe (if API key is set, otherwise use mock)
        if api_key and api_key != "your_api_key_here":
            text = transcribe_audio_file(filename)
        else:
            # Mock transcription for testing
            print("\n📝 Mock transcription (add API key for real Whisper)")
            text = input("   Type your command: ").strip()
        
        if not text:
            print("   ❌ No text received")
            continue
        
        # Display transcribed text prominently
        print("\n" + "="*60)
        print("  💬 TRANSCRIPTION")
        print("="*60)
        print(f"\n  \"{text}\"\n")
        print("="*60)
        
        # Parse intent
        intent = parse_intent(text)
        if intent:
            print(f"   Intent: {intent['intent']}")
            print(f"   Confidence: {intent['confidence']}")
        
        # Execute
        result = execute_intent(text)
        if result:
            print(f"\n✅ Result:")
            print(f"   Status: {result.get('status')}")
            if result.get('result'):
                import json
                print(f"   {json.dumps(result['result'][:2] if isinstance(result['result'], list) else result['result'], indent=6)}")
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
