import openai
from google.cloud import texttospeech
def openai_api(answer, ans_path):
    client = openai.OpenAI()
    # 声音可以被调整为 Alloy, Echo, Fable, Onyx, Nova, Shimmer (https://platform.openai.com/docs/guides/text-to-speech)
    voice = "alloy"
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=answer
    )
    response.stream_to_file(ans_path)


def google_api(answer, ans_path, language_code="en-US", gender="FEMALE", pitch=5.0, speaking_rate=1.0, voice_name="en-US-Standard-C"):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=answer)

    gender_map = {
        "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
        "MALE": texttospeech.SsmlVoiceGender.MALE,
        "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL
    }

    # 在这里预览声音效果：https://console.cloud.google.com/speech/text-to-speech;
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=gender_map.get(gender.upper(), texttospeech.SsmlVoiceGender.FEMALE),
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        pitch=pitch,
        speaking_rate=speaking_rate
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    with open(ans_path, "wb") as out:
        out.write(response.audio_content)
        out.close()