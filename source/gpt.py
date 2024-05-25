import openai

client = openai.OpenAI()
def dialogue(user_input, role_path, his_path):
    # 读取要让gpt扮演的角色信息
    with open(role_path, 'r', encoding='utf-8') as file:
        role_info = file.read()

    conversation = []
    # 如果有历史聊天信息，则打开并读取内容
    with open(his_path, 'r') as file:
        history_info = file.read()
        # 设置与gpt的对话
        conversation.extend([{"role": "system",
                              "content": role_info + history_info},
                             {"role": "user", "content": user_input}])

    # 获取gpt的回复
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o",
        messages=conversation
    )
    output_text = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": output_text})
    return output_text + '\n'

def voice2text(qus_path):
    audio_file = open(qus_path, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
    return transcript

