import numpy as np

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=32767, fade_duration=0.005):
    """
    Generate a sine wave with a short fade-in and fade-out to reduce clicks.
    """
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    
    return apply_fade_envelope(wave, sample_rate, fade_duration).astype(np.int16)


def generate_harmonic_wave(frequency, duration, harmonics=[1, 0.5, 0.25, 0.125], sample_rate=44100, amplitude=32767, fade_duration=0.005):
    """
    Generate a complex tone by adding harmonics, and apply a fade-in/fade-out envelope.
    """
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    wave = np.zeros(samples)

    # Add base tone and its harmonics.
    for i, harmonic_amplitude in enumerate(harmonics, start=1):
        wave += harmonic_amplitude * np.sin(2 * np.pi * frequency * i * t)

    # Normalize the resulting waveform.
    wave *= amplitude / np.max(np.abs(wave))

    return apply_fade_envelope(wave, sample_rate, fade_duration).astype(np.int16)


def generate_square_wave(frequency, duration, sample_rate=44100, amplitude=32767, fade_duration=0.005):
    """
    Generate a square wave with a short fade-in and fade-out to reduce clicks.
    
    Parameters:
        frequency (float): Frequency of the note in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Number of samples per second.
        amplitude (int): The maximum amplitude (for 16-bit audio, typically 32767).
        fade_duration (float): Duration in seconds of fade-in and fade-out.
    
    Returns:
        numpy.ndarray: The generated square wave as 16-bit audio data.
    """
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    # Generate square wave using the sign of a sine wave.
    wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    
    return apply_fade_envelope(wave, sample_rate, fade_duration).astype(np.int16)


def generate_sawtooth_wave(frequency, duration, sample_rate=44100, amplitude=32767, fade_duration=0.005):
    """
    Generate a sawtooth wave with a short fade-in and fade-out to reduce clicks.
    
    Parameters:
        frequency (float): Frequency of the note in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Number of samples per second.
        amplitude (int): The maximum amplitude (for 16-bit audio, typically 32767).
        fade_duration (float): Duration in seconds of fade-in and fade-out.
    
    Returns:
        numpy.ndarray: The generated sawtooth wave as 16-bit audio data.
    """
    samples = int(sample_rate * duration)
    t = np.linspace(0, duration, samples, False)
    # Generate sawtooth wave: ranges from -1 to 1.
    wave = amplitude * (2 * (t * frequency - np.floor(t * frequency)) - 1)
    
    return apply_fade_envelope(wave, sample_rate, fade_duration).astype(np.int16)


def generate_triangle_wave(frequency, duration, sample_rate=44100, amplitude=32767, fade_duration=0.005):
    """
    Generate a triangle wave with a short fade-in and fade-out to reduce clicks.
    
    Parameters:
        frequency (float): Frequency of the note in Hz.
        duration (float): Duration of the note in seconds.
        sample_rate (int): Number of samples per second.
        amplitude (int): The maximum amplitude for 16-bit audio (typically 32767).
        fade_duration (float): Duration in seconds of the fade-in/out.
    
    Returns:
        numpy.ndarray: The generated triangle wave as 16-bit audio data.
    """
    # Total number of samples in the wave.
    samples = int(sample_rate * duration)
    # Create a time array. Use endpoint=False for a periodic waveform.
    t = np.linspace(0, duration, samples, endpoint=False)
    
    # Generate a triangle wave using the standard formula.
    # The inner expression produces a sawtooth-like ramp, which is then "folded" by taking the absolute value.
    triangle = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    
    # Scale the triangle wave to the desired amplitude.
    wave = amplitude * triangle

    return apply_fade_envelope(wave, sample_rate, fade_duration).astype(np.int16)


def apply_fade_envelope(wave, sample_rate, fade_duration=0.005):
    """
    Apply a fade-in and fade-out envelope to a waveform to reduce clicks.
    
    Parameters:
        wave (numpy.ndarray): Input waveform
        sample_rate (int): Number of samples per second
        fade_duration (float): Duration in seconds of fade-in and fade-out
        
    Returns:
        numpy.ndarray: The waveform with fade envelope applied
    """
    samples = len(wave)
    fade_samples = int(sample_rate * fade_duration)
    
    if fade_samples > 0 and fade_samples * 2 < samples:
        fade_in = np.linspace(0.0, 1.0, fade_samples)
        fade_out = np.linspace(1.0, 0.0, fade_samples)
        envelope = np.ones(samples)
        envelope[:fade_samples] = fade_in
        envelope[-fade_samples:] = fade_out
        wave = wave * envelope
    
    return wave.astype(np.int16)


def apply_adsr_envelope(wave, sample_rate, attack=0.01, decay=0.1, sustain_level=0.7, release=0.1):
    """
    Apply an ADSR envelope (Attack, Decay, Sustain, Release) to a waveform,
    and convert the result into a 16-bit integer array.
    
    Parameters:
        wave (numpy.ndarray): Input waveform (typically a sine or harmonic wave).
        sample_rate (int): The number of samples per second.
        attack (float): Attack time in seconds.
        decay (float): Decay time in seconds.
        sustain_level (float): Sustain level (0 to 1).
        release (float): Release time in seconds.
        
    Returns:
        numpy.ndarray: The waveform after applying the ADSR envelope, cast as int16.
    """
    length = len(wave)
    envelope = np.zeros(length)

    # Compute the number of samples for each segment
    attack_samples = int(sample_rate * attack)
    decay_samples = int(sample_rate * decay)
    release_samples = int(sample_rate * release)
    sustain_samples = length - (attack_samples + decay_samples + release_samples)

    # If sustain duration goes negative, adjust release_samples accordingly
    if sustain_samples < 0:
        sustain_samples = 0
        release_samples = length - (attack_samples + decay_samples)

    # Create the envelope segments:
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples, endpoint=False)
    envelope[attack_samples:attack_samples + decay_samples] = np.linspace(1, sustain_level, decay_samples, endpoint=False)
    envelope[attack_samples + decay_samples:attack_samples + decay_samples + sustain_samples] = sustain_level
    envelope[-release_samples:] = np.linspace(sustain_level, 0, release_samples)

    # Apply the envelope to the wave
    wave = wave * envelope

    # Re-normalize the waveform to the 16-bit range if needed:
    max_val = np.max(np.abs(wave))
    if max_val > 0:
        wave = wave / max_val * 32767

    return wave.astype(np.int16) 