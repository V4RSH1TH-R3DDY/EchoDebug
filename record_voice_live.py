#!/usr/bin/env python3
"""
Live voice recorder with real-time transcription display
Shows text appearing as you speak (simulated)
"""

import sounddevice as sd
import soundfile as sf
import requests
import numpy as np
import sys
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Configuration
SAMPLE_RATE = 16000
DURATION = 5
API_URL = "http://localhost:8000"

def typing_effect(text, delay=0.03):
    """Print text with typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def record_with_visualization(duration=5):
    """Record audio with real-time visualization"""
    print(f"\n🎙️  Recording for {duration} seconds...")
    print("   Speak clearly into your microphone...\n")
    
    audio_buffer = []
    
    def callback(indata, frames, time_info, status):
        audio_buffer.append(indata.copy())
        volume = np.linalg.norm(indata) * 10
        
        if volume < 1:
            indicator = "░"
        elif volume < 3:
            indicator = "▒"
        elif volume < 6:
            indicator = "▓"
        else:
            indicator = "█"
        
        bar_length = int(min(volume, 20))
        bar = indicator * bar_length
        print(f"\r   🎤 {bar:<20} {volume:.1f}", end='', flush=True)
    
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback,
        dtype='float32'
    ):
        for i in range(duration, 0, -1):
            print(f"\n   ⏱️  {i} seconds remaining...", end='', flush=True)
            time.sleep(1)
    
    print("\n\n   ✓ Recording complete!")
    
    if audio_buffer:
        audio = np.concatenate(audio_buffer, axis=0)
        max_volume = np.max(np.abs(audio))
        
        if max_volume < 0.01:
            print("      ⚠️  Very low audio! Speak louder")
        elif max_volume > 0.9:
            print("      ⚠️  Audio clipping! Speak softer")
        else:
            print(f"      ✓ Audio level good ({max_volume:.3f})")
        
        return audio
    return None

def save_audio(audio, filename="temp_audio.wav"):
    """Save audio to file"""
    # Use absolute path
    abs_filename = os.path.abspath(filename)
    sf.write(abs_filename, audio, SAMPLE_RATE)
    return abs_filename

def transcribe_audio_file(filename):
    """Send audio file to API for transcription"""
    print(f"\n📤 Sending to Whisper API...")
    print("   Processing audio...")
    
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

def display_transcription(text):
    """Display transcription with nice formatting"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*20 + "💬 TRANSCRIPTION" + " "*22 + "║")
    print("╠" + "="*58 + "╣")
    print("║" + " "*58 + "║")
    
    # Word wrap the text
    words = text.split()
    line = "  "
    
    for word in words:
        if len(line) + len(word) + 1 <= 54:
            line += word + " "
        else:
            print("║ " + line.ljust(56) + " ║")
            line = "  " + word + " "
    
    if line.strip():
        print("║ " + line.ljust(56) + " ║")
    
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

def display_transcription_typing(text):
    """Display transcription with typing effect"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*20 + "💬 TRANSCRIPTION" + " "*22 + "║")
    print("╠" + "="*58 + "╣")
    print("║" + " "*58 + "║")
    
    # Print with typing effect
    print("║  ", end='', flush=True)
    
    words = text.split()
    line_length = 0
    
    for i, word in enumerate(words):
        if line_length + len(word) + 1 > 54:
            # New line
            print(" " * (54 - line_length) + " ║")
            print("║  ", end='', flush=True)
            line_length = 0
        
        # Type out word
        for char in word:
            print(char, end='', flush=True)
            time.sleep(0.02)
        
        if i < len(words) - 1:
            print(" ", end='', flush=True)
            time.sleep(0.05)
        
        line_length += len(word) + 1
    
    # Fill rest of line
    print(" " * (54 - line_length) + " ║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

def execute_command(text):
    """Execute the voice command"""
    print(f"\n⚡ Executing command...")
    
    try:
        response = requests.post(
            f"{API_URL}/intent/route",
            json={"text": text}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Result:")
            print(f"   Status: {result.get('status')}")
            print(f"   Intent: {result.get('intent')}")
            
            if result.get('result'):
                import json
                res = result['result']
                if isinstance(res, list):
                    print(f"   Found {len(res)} result(s)")
                    if res:
                        first = res[0]
                        print(f"\n   First result:")
                        print(f"   • File: {first.get('file', 'N/A')}")
                        print(f"   • Line: {first.get('line', 'N/A')}")
                        print(f"   • Kind: {first.get('kind', 'N/A')}")
                else:
                    print(f"   {json.dumps(res, indent=6)}")
            
            return result
        else:
            print(f"   ❌ API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def main():
    """Main voice command loop"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*10 + "🎙️  EchoDebug Live Voice Recorder" + " "*13 + "║")
    print("║" + " "*15 + "Real-time Transcription" + " "*19 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check server
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
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  No OpenAI API key - using mock transcription")
        use_whisper = False
    else:
        print("\n✓ OpenAI API key detected - Whisper enabled")
        use_whisper = True
    
    # Main loop
    while True:
        print("\n" + "-"*60)
        print("Press ENTER to start recording (or 'q' to quit)")
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            break
        
        # Record audio
        audio = record_with_visualization(duration=DURATION)
        
        if audio is None:
            continue
        
        # Save audio
        filename = save_audio(audio)
        
        # Transcribe
        if use_whisper:
            text = transcribe_audio_file(filename)
        else:
            print("\n📝 Mock mode - type your command:")
            text = input("   > ").strip()
        
        if not text:
            print("   ❌ No text received")
            continue
        
        # Display with typing effect
        display_transcription_typing(text)
        
        # Execute
        execute_command(text)
        
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
