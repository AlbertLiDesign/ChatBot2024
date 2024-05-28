from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QTimer, QTime, QDate, QLocale

from gui.main_page import Ui_MainWindow

from connect_db import ConnectDB
from chat_window import UsrWidget, GPTWidget

import source.gpt as gpt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 各种文件的路径
        self.qus_path = "../question.wav"
        self.ans_path = "answer.wav"  # 使用openai的api，这里得改成mp3格式
        self.his_path = "history.txt"
        self.role_path = "role_settings.txt"

        self.connect_db = ConnectDB()

        # 设置一个垂直布局，用于消息列表
        self.message_layout = QVBoxLayout(self.ui.scrollAreaWidgetContents)

        # 定义ui控件
        self.chat_btn = self.ui.dia_btn
        self.set_btn = self.ui.set_btn
        self.record_btn = self.ui.record_btn
        self.chat_scrollArea = self.ui.scroll_area

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        # 初始化时钟显示
        self.update_time()

        # 按钮功能
        self.chat_num = 0 # 检测是否是第一次输入
        if self.chat_num == 0:
            self.record_btn.clicked.connect(self.start_chat)
        else:
            self.record_btn.clicked.connect(self.recording)

        self.chat_btn.clicked.connect(self.show_chat_page)
        self.set_btn.clicked.connect(self.show_set_page)

    def update_time(self):
        # 设置应用程序语言环境为英语
        english_locale = QLocale(QLocale.English, QLocale.UnitedStates)
        QLocale.setDefault(english_locale)

        current_time = QTime.currentTime()
        current_day = QDate.currentDate()

        formatted_hour = english_locale.toString(current_time, 'hh')
        formatted_minute = english_locale.toString(current_time, 'mm')
        formatted_day = english_locale.toString(current_day, 'dddd')
        formatted_date = english_locale.toString(current_day, 'dd MMM')

        self.ui.hour_label.setText(formatted_hour)
        self.ui.minute_label.setText(formatted_minute)
        self.ui.day_label.setText(formatted_day)
        self.ui.date_label.setText(formatted_date)
    def show_main_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)
    def show_chat_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    def show_set_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def start_chat(self):
        # 记录开始时间
        self.connect_db.set_start_date()
        # 先录音
        self.recording()
        chat_data = self.connect_db.get_chat_data()

        self.ui.scroll_area.setLayout(self.message_layout)
        self.show_chats(chat_data)

    def recording(self):
        # 语音转文字
        question = gpt.voice2text(self.qus_path)
        self.connect_db.add_chat_data("user", question)
        print(question)

    def get_response(self):
        if __name__ == '__main__':
            message_input = self.message_input.toPlainText().strip()
            chat_db = self.connect_db.get_chat_data()

            # if message_input:
                # response_list = gpt.dialogue()

    def show_chats(self, chat_data):
        messages = chat_data.get("messages")
        for message in messages:
            if message.get("role") == "user":
                usr_str = message.get("content")
                usr_widget = UsrWidget()
                usr_widget.set_user_text(usr_str)
                self.message_layout.addWidget(usr_widget)

            if message.get("role") == "echo":
                gpt_str = message.get("content")
                gpt_widget = GPTWidget()
                gpt_widget.set_gpt_text(gpt_str)
                self.message_layout.addWidget(gpt_widget)


        # 添加一个spacer item，使得消息能自动靠上显示
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.message_layout.addItem(spacer_item)

        # 调整滚动条以显示最新消息
        self.ui.scroll_area.verticalScrollBar().setValue(self.ui.scroll_area.verticalScrollBar().maximum())

        # 调整滚动条以显示最新消息
        self.ui.scroll_area.verticalScrollBar().setValue(self.ui.scroll_area.verticalScrollBar().maximum())
