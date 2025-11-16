#!/usr/bin/env python3
"""
Advanced voice recorder with real-time audio visualization
Shows you exactly when and how loud you're speaking
"""

import sounddevice as sd
import soundfile as sf
import requests
import numpy as np
import sys
import os
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')

# Configuration
SAMPLE_RATE = 16000
DURATION = 5
API_URL = "http://localhost:8000"

# Global flag for recording status
is_recording = False
audio_buffer = []

def audio_callback(indata, frames, time_info, status):
    """Callback for real-time audio processing"""
    global audio_buffer
    if status:
        print(f"Status: {status}", file=sys.stderr)
    
    # Store audio data
    audio_buffer.append(indata.copy())
    
    # Calculate volume level
    volume = np.linalg.norm(indata) * 10
    
    # Visual feedback based on volume
    if volume < 1:
        indicator = "░"  # Very quiet
    elif volume < 3:
        indicator = "▒"  # Quiet
    elif volume < 6:
        indicator = "▓"  # Medium
    else:
        indicator = "█"  # Loud
    
    # Print volume bar
    bar_length = int(min(volume, 20))
    bar = indicator * bar_length
    print(f"\r   🎤 {bar:<20} {volume:.1f}", end='', flush=True)

def record_with_visualization(duration=5):
    """Record audio with real-time visualization"""
    global is_recording, audio_buffer
    
    print(f"\n🎙️  Recording for {duration} seconds...")
    print("   Watch the bars - they show your voice level!")
    print("   Speak clearly into your microphone...\n")
    
    is_recording = True
    audio_buffer = []
    
    # Start recording with callback
    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=audio_callback,
        dtype='float32'
    ):
        # Show countdown
        for i in range(duration, 0, -1):
            print(f"\n   ⏱️  {i} seconds remaining...", end='', flush=True)
            time.sleep(1)
    
    is_recording = False
    
    print("\n\n   ✓ Recording complete!")
    
    # Combine audio chunks
    if audio_buffer:
        audio = np.concatenate(audio_buffer, axis=0)
        
        # Show statistics
        max_volume = np.max(np.abs(audio))
        avg_volume = np.mean(np.abs(audio))
        
        print(f"\n   📊 Audio Statistics:")
        print(f"      Max volume: {max_volume:.3f}")
        print(f"      Avg volume: {avg_volume:.3f}")
        
        if max_volume < 0.01:
            print("      ⚠️  Very low audio! Speak louder or check microphone")
        elif max_volume > 0.9:
            print("      ⚠️  Audio clipping! Speak softer or reduce mic gain")
        else:
            print("      ✓ Audio level is good!")
        
        return audio
    else:
        print("   ❌ No audio captured!")
        return None

def save_audio(audio, filename="temp_audio.wav"):
    """Save audio to file"""
    sf.write(filename, audio, SAMPLE_RATE)
    print(f"\n   💾 Saved to {filename}")
    return filename

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

def execute_command(text):
    """Execute the voice command"""
    print(f"\n⚡ Executing: '{text}'")
    
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
                        print(f"   First: {json.dumps(res[0], indent=6)}")
                else:
                    print(f"   {json.dumps(res, indent=6)}")
            
            return result
        else:
            print(f"   ❌ API error: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_microphone():
    """Test microphone with visual feedback"""
    print("\n🎤 Testing microphone...")
    print("   Say something for 3 seconds...")
    print("   Watch the bars to see if your voice is detected!\n")
    
    try:
        global audio_buffer
        audio_buffer = []
        
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            callback=audio_callback,
            dtype='float32'
        ):
            time.sleep(3)
        
        print("\n\n   ✓ Microphone test complete!")
        
        if audio_buffer:
            audio = np.concatenate(audio_buffer, axis=0)
            max_volume = np.max(np.abs(audio))
            
            if max_volume < 0.001:
                print("   ❌ No sound detected!")
                print("      Check:")
                print("      • Microphone is connected")
                print("      • Microphone permissions granted")
                print("      • Correct input device selected")
                return False
            else:
                print(f"   ✓ Sound detected! (level: {max_volume:.3f})")
                return True
        else:
            print("   ❌ No audio captured!")
            return False
            
    except Exception as e:
        print(f"\n   ❌ Error: {e}")
        return False

def list_audio_devices():
    """List available audio input devices"""
    print("\n🔊 Available Audio Devices:")
    devices = sd.query_devices()
    
    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:
            default = " (DEFAULT)" if i == sd.default.device[0] else ""
            print(f"   [{i}] {device['name']}{default}")
            print(f"       Channels: {device['max_input_channels']}")

def main():
    """Main voice command loop"""
    print("\n" + "="*60)
    print("  🎙️  EchoDebug Advanced Voice Recorder")
    print("  Real-time audio visualization")
    print("="*60)
    
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
    
    # List audio devices
    list_audio_devices()
    
    # Test microphone
    if not test_microphone():
        print("\n❌ Microphone test failed!")
        return
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("\n⚠️  No OpenAI API key - using mock transcription")
        print("   Add OPENAI_API_KEY to backend/.env for Whisper\n")
    else:
        print("\n✓ OpenAI API key detected - Whisper enabled\n")
    
    # Main loop
    while True:
        print("\n" + "-"*60)
        print("Commands:")
        print("  [ENTER] - Record voice command")
        print("  [t]     - Test microphone again")
        print("  [d]     - List audio devices")
        print("  [q]     - Quit")
        
        choice = input("\n> ").strip().lower()
        
        if choice == 'q':
            print("\n👋 Goodbye!")
            break
        elif choice == 't':
            test_microphone()
            continue
        elif choice == 'd':
            list_audio_devices()
            continue
        
        # Record audio
        audio = record_with_visualization(duration=DURATION)
        
        if audio is None:
            continue
        
        # Save audio
        filename = save_audio(audio)
        
        # Transcribe
        if api_key and api_key != "your_api_key_here":
            text = transcribe_audio_file(filename)
        else:
            print("\n📝 Mock mode - type your command:")
            text = input("   > ").strip()
        
        if not text:
            print("   ❌ No text received")
            continue
        
        # Display transcribed text prominently
        print("\n" + "="*60)
        print("  💬 TRANSCRIPTION")
        print("="*60)
        print(f"\n  \"{text}\"\n")
        print("="*60)
        
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
