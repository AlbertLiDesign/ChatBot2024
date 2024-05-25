import speech_recognition as sr

import source.gpt as gpt
import source.recorder as recorder
import source.speaker as speaker
import source.wake_up as wake_up
import source.text2voice as t2v

voice_mode = True # 语音模式，设为False就可以通过修改question_txt直接与gpt交互
start_recording = True # 设为True则手动开始录音，否则会一直用先前的录音（测试用）
conversation_mode = False # 与GPT的交流模式，设为False则会先开启监听模式

question_txt = "who are you" # 不使用语音交互时可以用它来直接交互

# 角色信息
trigger_phrase = "Hey, Echo." + '\n'
host_role = "User: "
dev_role = "Echo: "

# 各种文件的路径
qus_path = "question.wav"
ans_path = "answer.wav" # 使用openai的api，这里得改成mp3格式
his_path = "history.txt"
role_path = "role_settings.txt"

if __name__ == "__main__":
    if voice_mode:
        while True:
            with open(his_path, "a") as file: # 记录对话历史
                # 监听模式，实时检查是否有唤醒词唤醒
                if not conversation_mode:
                    try:
                        keyword_index = wake_up.check()
                        # 检测到唤醒词
                        if keyword_index >= 0:
                            file.writelines(host_role + trigger_phrase)
                            # 播放回应音频
                            speaker.play_voice("defaultResponse.wav") # 使用openai的api，这里得改成mp3格式
                            file.writelines(dev_role + "Hey, I'm here. \n")  # 导出历史记录
                            file.flush()
                            # 进入对话模式
                            conversation_mode = True
                            continue  # Skip the rest of the loop and go to the next iteration
                    except sr.UnknownValueError:
                        file.writelines("System: Sorry, I did not get that")
                        file.flush()
                        pass
                    except sr.RequestError as e:
                        file.writelines("System: Could not request results; {0}".format(e))
                        file.flush()
                    except Exception as e:
                        file.writelines("System: Unexpected error: {0}".format(e))
                        file.flush()
                # 对话模式
                if conversation_mode:
                    # recording
                    if start_recording:
                        recorder.run(qus_path)  # record the user's question

                    # voice to text
                    question = gpt.voice2text(qus_path)
                    file.writelines(host_role + question)  # 导出历史记录
                    file.flush()
                    print(host_role + question)

                    if len(question) < 10:
                        # Come back to the listening mode
                        # If no sound or speech was detected in the recording, go back to the listening mode
                        file.writelines("System: No sound detected. Going back to listening mode...")
                        file.flush()
                        conversation_mode = False
                    else:
                        # conversation with GPT
                        answer = gpt.dialogue(question, role_path, his_path)
                        file.writelines(dev_role + answer)
                        file.flush()
                        print(dev_role + answer)

                        # text to voice
                        t2v.google_api(answer, ans_path)

                        # play voice
                        speaker.play_voice(ans_path)
                pass

    else:
        # 不使用语音交互时可以直接交互
        answer = gpt.dialogue(question_txt, dev_role)
        print(answer)







