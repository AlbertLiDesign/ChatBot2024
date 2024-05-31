from PyQt5.QtCore import QThread, pyqtSignal

import source.gpt as gpt
import source.recorder as recorder
import source.speaker as speaker
# import source.wake_up as wake_up
import source.text2voice as t2v
class RecordingThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, qus_path):
        super().__init__()
        self.qus_path = qus_path

    def run(self):
        # 录音
        recorder.run(self.qus_path)
        # 语音转文字
        question = gpt.voice2text(self.qus_path)
        self.result_ready.emit(question)
class GPTThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, question, role_path, connect_db):
        super().__init__()
        self.question = question
        self.role_path = role_path
        self.connect_db = connect_db

    def run(self):
        chat_data = self.connect_db.get_chat_data()
        answer = gpt.dialogue(self.question, self.role_path, chat_data)
        self.connect_db.add_chat_data(role="assistant", content=answer)
        self.result_ready.emit(answer)


class VoicePlayThread(QThread):
    def __init__(self, answer, ans_path):
        super().__init__()
        self.ans_path = ans_path
        self.answer = answer

    def run(self):
        # text to voice
        t2v.google_api(self.answer, self.ans_path)
        # play voice
        speaker.play_voice(self.ans_path)
