import os
import numpy as np
from scipy.io import wavfile
import pygame

# Create sounds directory if it doesn't exist
os.makedirs("sounds", exist_ok=True)

def create_jump_sound():
    """Create a simple jump sound effect"""
    sample_rate = 44100
    duration = 0.3  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a tone that goes up in pitch
    freq_start = 300
    freq_end = 1200
    freq = np.linspace(freq_start, freq_end, int(sample_rate * duration))
    note = np.sin(2 * np.pi * freq * t)
    
    # Apply a volume envelope
    envelope = np.exp(-5 * t)
    note = note * envelope
    
    # Normalize
    note = note * 32767 / np.max(np.abs(note))
    note = note.astype(np.int16)
    
    # Save as WAV file
    wavfile.write("sounds/jump.wav", sample_rate, note)
    print("Created jump sound")

def create_collision_sound():
    """Create a simple collision sound effect"""
    sample_rate = 44100
    duration = 0.5  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a descending tone with some noise
    freq_start = 800
    freq_end = 200
    freq = np.linspace(freq_start, freq_end, int(sample_rate * duration))
    note = np.sin(2 * np.pi * freq * t)
    
    # Add some noise
    noise = np.random.uniform(-0.5, 0.5, int(sample_rate * duration))
    note = note + noise
    
    # Apply a volume envelope
    envelope = np.exp(-3 * t)
    note = note * envelope
    
    # Normalize
    note = note * 32767 / np.max(np.abs(note))
    note = note.astype(np.int16)
    
    # Save as WAV file
    wavfile.write("sounds/collision.wav", sample_rate, note)
    print("Created collision sound")

def create_point_sound():
    """Create a simple point scoring sound effect"""
    sample_rate = 44100
    duration = 0.2  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate two ascending tones
    freq1 = 800
    freq2 = 1200
    note1 = np.sin(2 * np.pi * freq1 * t)
    note2 = np.sin(2 * np.pi * freq2 * t)
    note = note1 + note2
    
    # Apply a volume envelope
    envelope = np.exp(-10 * t)
    note = note * envelope
    
    # Normalize
    note = note * 32767 / np.max(np.abs(note))
    note = note.astype(np.int16)
    
    # Save as WAV file
    wavfile.write("sounds/point.wav", sample_rate, note)
    print("Created point sound")

def create_background_music():
    """Create a simple background music loop"""
    sample_rate = 44100
    duration = 5.0  # seconds
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Generate a simple melody
    melody = np.zeros_like(t)
    
    # Define some notes
    notes = [262, 294, 330, 349, 392, 440, 494]  # C4, D4, E4, F4, G4, A4, B4
    
    # Create a simple melody pattern
    note_duration = 0.25  # quarter note
    samples_per_note = int(note_duration * sample_rate)
    
    for i in range(0, len(t), samples_per_note):
        if i + samples_per_note > len(t):
            break
        
        # Choose a random note from our scale
        note_freq = notes[np.random.randint(0, len(notes))]
        
        # Generate the note
        note_t = t[i:i+samples_per_note] - t[i]
        melody[i:i+samples_per_note] = 0.5 * np.sin(2 * np.pi * note_freq * note_t)
    
    # Add a bass line
    bass_freq = 65.41  # C2
    bass = 0.3 * np.sin(2 * np.pi * bass_freq * t)
    
    # Combine melody and bass
    music = melody + bass
    
    # Normalize
    music = music * 32767 / np.max(np.abs(music))
    music = music.astype(np.int16)
    
    # Save as WAV file
    wavfile.write("sounds/background_music.wav", sample_rate, music)
    print("Created background music")

def main():
    try:
        import scipy
        create_jump_sound()
        create_collision_sound()
        create_point_sound()
        create_background_music()
        print("All sound files created successfully!")
    except ImportError:
        print("SciPy not installed. Creating empty sound files instead.")
        
        # Create empty sound files
        for sound_file in ["jump.wav", "collision.wav", "point.wav", "background_music.wav"]:
            with open(os.path.join("sounds", sound_file), "wb") as f:
                # Write a minimal WAV header
                f.write(b"RIFF")
                f.write((36).to_bytes(4, byteorder='little'))  # File size - 8
                f.write(b"WAVE")
                f.write(b"fmt ")
                f.write((16).to_bytes(4, byteorder='little'))  # Subchunk1Size
                f.write((1).to_bytes(2, byteorder='little'))   # AudioFormat (PCM)
                f.write((1).to_bytes(2, byteorder='little'))   # NumChannels
                f.write((44100).to_bytes(4, byteorder='little'))  # SampleRate
                f.write((44100 * 2).to_bytes(4, byteorder='little'))  # ByteRate
                f.write((2).to_bytes(2, byteorder='little'))   # BlockAlign
                f.write((16).to_bytes(2, byteorder='little'))  # BitsPerSample
                f.write(b"data")
                f.write((0).to_bytes(4, byteorder='little'))   # Subchunk2Size
            print(f"Created empty {sound_file}")

if __name__ == "__main__":
    main()
