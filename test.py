# from openai import OpenAI
# client = OpenAI()
#
# response = client.audio.speech.create(
#   model="tts-1",
#   voice="shimmer",
#   input="Hey, I'm here"
# )
# response.stream_to_file('defaultResponse.mp3')

from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()
input_text = texttospeech.SynthesisInput(text="Hey, I'm here.")

# 在这里预览声音效果：https://console.cloud.google.com/speech/text-to-speech;
voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        name="en-US-Standard-C"
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.LINEAR16,
    pitch=5.0,
    speaking_rate=1.0
)

response = client.synthesize_speech(
    request={"input": input_text, "voice": voice, "audio_config": audio_config}
)

with open("defaultResponse.wav", "wb") as out:
    out.write(response.audio_content)
    out.close()