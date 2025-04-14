from music21 import converter, note, chord
from wave_generation import (
    generate_sine_wave,
    generate_harmonic_wave,
    generate_square_wave,
    generate_sawtooth_wave,
    generate_triangle_wave
)
import numpy as np

def generate_notes(start_octave=0, end_octave=8):
    """
    Generate a dictionary mapping note names (e.g., C4, D#4) to their frequencies.
    Calculation uses the equal-tempered scale with A4=440 Hz as the reference.
    """
    note_names = ["C", "C#", "D", "D#", "E", "F",
                  "F#", "G", "G#", "A", "A#", "B"]
    notes = {}
    A4 = 440.0
    A4_index = note_names.index("A")
    A4_octave = 4

    for octave in range(start_octave, end_octave + 1):
        for i, n in enumerate(note_names):
            note_name = f"{n}{octave}"
            semitone_diff = (octave - A4_octave) * 12 + (i - A4_index)
            frequency = A4 * (2 ** (semitone_diff / 12))
            notes[note_name] = frequency
    return notes

def extract_melody(musicxml_path):
    """
    Extract a monophonic melody from a MusicXML file.
    
    Each note is represented as a tuple: (note_name, duration)
    Duration is taken from note.duration.quarterLength.
    Notes (or chords) with a zero duration (likely grace notes) are given a minimal value.
    """
    score = converter.parse(musicxml_path)
    melody = []
    for element in score.flat.notes:
        if isinstance(element, note.Rest):
            melody.append(("rest", element.duration.quarterLength))
        elif isinstance(element, note.Note):
            duration = element.duration.quarterLength
            melody.append((str(element.pitch), duration))
        elif isinstance(element, chord.Chord):
            duration = element.duration.quarterLength
            melody.append((str(element.root()), duration))
    return melody

notes_dict = generate_notes(0, 8)

def get_note_frequency(note_name):
    """Convert a note name (e.g., 'A4') to its frequency in Hz."""
    return notes_dict.get(note_name, 0)

def generate_notes_waveform(notes, waveform='sine', harmonics=[1, 0.5, 0.25, 0.125], sample_rate=44100, duration=2.0):
    """
    Generate a waveform for a list of notes.
    """
    wave_data = None
    
    for note_name in notes:
        frequency = get_note_frequency(note_name)
        if waveform == 'sine':
            note_wave = generate_sine_wave(frequency, duration, sample_rate)
        elif waveform == 'harmonic':
            note_wave = generate_harmonic_wave(frequency, duration, harmonics, sample_rate)
        elif waveform == 'square':
            note_wave = generate_square_wave(frequency, duration, sample_rate)
        elif waveform == 'sawtooth':
            note_wave = generate_sawtooth_wave(frequency, duration, sample_rate)
        elif waveform == 'triangle':
            note_wave = generate_triangle_wave(frequency, duration, sample_rate)
        else:
            raise ValueError("Invalid waveform type")
        
        if wave_data is None:
         wave_data = note_wave
        else:
            wave_data = np.concatenate((wave_data, note_wave))

    return wave_data

def generate_melody_waveform(melody, waveform='sine', harmonics=[1, 0.5, 0.25, 0.125], sample_rate=44100, duration_factor=0.25):
    """
    Generate a melody from a MusicXML file.
    """
    wave_data = None
    
    for note_name, duration in melody:
        if duration == 0:
            continue
        print(f"Generating waveform for note: {note_name} with duration: {duration * duration_factor} (duration factor: {duration_factor})")
        frequency = get_note_frequency(note_name)
        if frequency == 0:  # rest
            rest_samples = int(sample_rate * duration * duration_factor)
            note_wave = np.zeros(rest_samples, dtype=np.int16)
        else:
            if waveform == 'sine':
                note_wave = generate_sine_wave(frequency, duration * duration_factor, sample_rate)
            elif waveform == 'harmonic':
                note_wave = generate_harmonic_wave(frequency, duration * duration_factor, harmonics, sample_rate)
            elif waveform == 'square':
                note_wave = generate_square_wave(frequency, duration * duration_factor, sample_rate)
            elif waveform == 'sawtooth':
                note_wave = generate_sawtooth_wave(frequency, duration * duration_factor, sample_rate)
            elif waveform == 'triangle':
                note_wave = generate_triangle_wave(frequency, duration * duration_factor, sample_rate)
            else:
                raise ValueError("Invalid waveform type")
        
        if wave_data is None:
            wave_data = note_wave
        else:
            wave_data = np.concatenate((wave_data, note_wave))

    return wave_data
    