import pyaudio
import pvporcupine
import struct
import os

ppn_key = os.environ['PORCUPINE']

porcupine = pvporcupine.create(
    access_key=ppn_key,
    keywords=['Hey Echo'],
    #keyword_paths=['..\wake-up-word\Hey-Amoeba_en_raspberry-pi_v2_2_0.ppn']
    keyword_paths=['wake-up-word\Hey-Echo_en_windows_v3_0_0.ppn']
)

pa = pyaudio.PyAudio()

audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length)


def check():
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    return porcupine.process(pcm)