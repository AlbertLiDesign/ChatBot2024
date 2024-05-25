import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Global variables
frames_global = []
recording = False
silence_counter = 0
silence_limit = 20  # Two seconds of silence at a sample rate of fs and block size defined below


def audio_callback(indata, frame_count, time_info, status):
    global frames_global, silence_counter, recording
    volume_norm = np.linalg.norm(indata) * 10  # Calculate the volume

    # Append the processed frame to the global frames list
    frames_global.append(indata.copy())

    # Adjust the threshold and silence limit according to your microphone sensitivity and environment noise
    if volume_norm < 5:  # Threshold for silence detection can be adjusted
        silence_counter += 1
        if silence_counter >= silence_limit:
            recording = False
            raise sd.CallbackStop()  # Stop the audio processing callback
    else:
        silence_counter = 0  # Reset silence counter on detecting noise


def run(qus_path, fs=44100, duration=10):
    global frames_global, recording, silence_counter
    frames_global = []  # Clear previous recordings
    recording = True
    silence_counter = 0

    print("Start listening...")
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=fs, dtype='float32', blocksize=int(fs*0.1)):
        while recording:
            sd.sleep(100)  # Short sleep to reduce latency in stopping

    if frames_global:
        recording_data = np.concatenate(frames_global)
        wav.write(qus_path, fs, np.int16(recording_data * 32767))
        print('Recording saved.')
    else:
        print('No data recorded.')
