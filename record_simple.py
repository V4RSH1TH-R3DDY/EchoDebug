#!/usr/bin/env python3
"""
Simple voice recorder - just press ENTER and speak!
"""

import sounddevice as sd
import soundfile as sf
import requests
import numpy as np
import os
from dotenv import load_dotenv

# Load environment
load_dotenv('backend/.env')

# Config
SAMPLE_RATE = 16000
DURATION = 5
API_URL = "http://localhost:8000"

def record_audio():
    """Record audio from microphone"""
    print("\n🎙️  GET READY...")
    print("   Recording will start in 3 seconds...")
    
    import time
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🔴 RECORDING NOW - SPEAK!")
    print("   (Recording for 5 seconds)")
    
    # Record
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    
    # Show countdown
    for i in range(DURATION, 0, -1):
        print(f"   {i} seconds left...", end='\r', flush=True)
        time.sleep(1)
    
    sd.wait()
    
    print("\n\n✅ Recording complete!")
    
    # Check audio level
    max_vol = np.max(np.abs(audio))
    print(f"   Audio level: {max_vol:.3f}")
    
    if max_vol < 0.01:
        print("   ⚠️  Very quiet! Speak louder next time")
    
    return audio

def save_and_transcribe(audio):
    """Save audio and send to Whisper"""
    # Save with absolute path
    filename = os.path.abspath("temp_audio.wav")
    sf.write(filename, audio, SAMPLE_RATE)
    print(f"\n💾 Saved audio file")
    
    # Check if we have API credits
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Try Whisper first
    print("📤 Sending to Whisper API...")
    
    try:
        response = requests.post(
            f"{API_URL}/stt/file",
            json={"file_path": filename}
        )
        
        if response.status_code == 200:
            text = response.json().get('text', '')
            
            # Display transcription
            print("\n" + "="*60)
            print("  💬 WHISPER TRANSCRIPTION:")
            print("="*60)
            print(f"\n  \"{text}\"\n")
            print("="*60)
            
            return text
        elif response.status_code == 500 and "insufficient_quota" in response.text:
            # No credits - fall back to manual input
            print("   ⚠️  No OpenAI credits remaining")
            print("   💡 Falling back to manual input...")
            
            print("\n" + "="*60)
            print("  💬 TYPE WHAT YOU SAID:")
            print("="*60)
            text = input("\n  > ").strip()
            print("="*60)
            
            return text
        else:
            print(f"   ❌ Error {response.status_code}")
            print("   💡 Type what you said instead:")
            text = input("   > ").strip()
            return text
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   💡 Type what you said instead:")
        text = input("   > ").strip()
        return text
    finally:
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)

def execute_command(text):
    """Execute the command"""
    if not text:
        return
    
    print("\n⚡ Executing command...")
    
    try:
        response = requests.post(
            f"{API_URL}/intent/route",
            json={"text": text}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Done!")
            print(f"   Intent: {result.get('intent')}")
            print(f"   Status: {result.get('status')}")
            
            if result.get('result'):
                res = result['result']
                if isinstance(res, list) and res:
                    print(f"   Found {len(res)} result(s)")
                    print(f"   First: {res[0].get('file')}:{res[0].get('line')}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    print("\n" + "="*60)
    print("  🎙️  EchoDebug Simple Voice Recorder")
    print("="*60)
    
    # Check server
    try:
        r = requests.get(f"{API_URL}/")
        if r.status_code != 200:
            print("\n❌ Server not running!")
            print("   Start with: python backend/main.py")
            return
    except:
        print("\n❌ Cannot connect to server!")
        return
    
    print("\n✅ Server is running")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✅ Whisper enabled")
    else:
        print("⚠️  No API key - Whisper disabled")
    
    print("\n" + "="*60)
    print("\nInstructions:")
    print("  1. Type 'r' and press ENTER to record")
    print("  2. Type 'q' and press ENTER to quit")
    print("="*60)
    
    while True:
        print("\n> ", end='', flush=True)
        choice = input().strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            break
        elif choice == 'r' or choice == '':
            # Record
            audio = record_audio()
            
            # Transcribe
            text = save_and_transcribe(audio)
            
            # Execute
            if text:
                execute_command(text)
        else:
            print("   Type 'r' to record or 'q' to quit")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
