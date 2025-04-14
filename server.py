from flask import Flask, send_file, send_from_directory, request
import io
import wave
import json
import os

from note_generation import extract_melody, generate_melody_waveform, generate_notes_waveform

# Set the static folder to the current directory
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    # Serve the local index.html file.
    print("Serving index.html")
    return send_from_directory('.', 'index.html')

@app.route('/audio')
def audio():
    """
    Generate audio based on the requested mode, waveform type, and parameters.
    """
    # Get parameters from the request
    mode = request.args.get('mode', 'note')
    waveform = request.args.get('waveform', 'sine')
    harmonics = request.args.get('harmonics', '[1, 0.5, 0.25, 0.125]')
    duration_factor = float(request.args.get('duration_factor', '0.25'))  
    duration = float(request.args.get('duration', '2.0'))
    notes = request.args.get('notes', 'A4')
    
    harmonics = json.loads(harmonics)
    notes = [note.strip() for note in notes.split(',')]
    sample_rate = 44100
    
    # Generate the appropriate waveform
    if mode == 'note':
        wave_data = generate_notes_waveform(notes, waveform, harmonics, sample_rate, duration)
    else:  # melody mode
        melody = extract_melody("FurElise.xml")
        wave_data = generate_melody_waveform(melody, waveform, harmonics, sample_rate, duration_factor)
    
    # Write the audio data to an in-memory bytes buffer as a WAV file
    virtual_file = io.BytesIO()
    with wave.open(virtual_file, 'wb') as wf:
        wf.setnchannels(1)      # Mono
        wf.setsampwidth(2)      # 2 bytes per sample (16-bit)
        wf.setframerate(sample_rate)
        wf.writeframes(wave_data.tobytes())
    
    virtual_file.seek(0)
    return send_file(virtual_file, mimetype="audio/wav", as_attachment=False, download_name="output.wav")

if __name__ == '__main__':
    print("Starting server...")
    app.run(debug=False, port=5001)
