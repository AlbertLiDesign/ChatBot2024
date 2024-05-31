import openai
import json

client = openai.OpenAI()
def dialogue(user_input, role_path, chat_data):
    # 读取要让gpt扮演的角色信息
    with open(role_path, 'r', encoding='utf-8') as file:
        role_info = file.read()

    conversation = []

    history_info = chat_data.get("messages", [])
    # 将 JSON 文件中的所有消息添加到对话中
    for message in history_info:
        conversation.append({"role": message["role"], "content": message["content"]})

    # 设置与gpt的对话
    conversation.append({"role": "system", "content": role_info})
    conversation.append({"role": "user", "content": user_input})

    # 获取gpt的回复
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o",
        messages=conversation
    )
    output_text = response.choices[0].message.content

    return output_text + '\n'

def voice2text(qus_path):
    audio_file = open(qus_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
    return transcript

