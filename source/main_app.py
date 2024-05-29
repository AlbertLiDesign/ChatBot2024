import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QVBoxLayout, QSizePolicy, QSpacerItem, QLabel
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

        self.show_main_page() # 设置主页面

        # 各种文件的路径
        self.qus_path = "../question.wav"
        self.ans_path = "../answer.wav"  # 使用openai的api，这里得改成mp3格式
        self.role_path = "../role_settings.txt"

        self.connect_db = ConnectDB()

        # 定义ui控件
        self.chat_btn = self.ui.chat_btn
        self.set_btn = self.ui.set_btn
        self.record_btn = self.ui.record_btn
        self.return_btn = self.ui.return_btn
        self.return_btn2 = self.ui.return_btn2
        self.quit_btn = self.ui.quit_btn
        self.light_btn = self.ui.light_btn
        self.volume_btn = self.ui.volume_btn
        self.wifi_btn = self.ui.wifi_btn
        self.bluetooth_btn = self.ui.bluetooth_btn
        self.language_btn = self.ui.language_btn
        self.clear_history_btn = self.ui.clear_history_btn
        self.spark_label = self.ui.spark_label
        self.chat_scroll_area = self.ui.chat_scroll_area
        self.chat_scroll_content = self.ui.chat_scroll_content

        # 设置一个垂直布局，用于消息列表
        self.message_layout = QVBoxLayout(self.chat_scroll_content)
        self.chat_scroll_content.setLayout(self.message_layout)

        usr_widget = UsrWidget(self.chat_scroll_content)
        usr_widget.set_user_text("who are you")
        self.message_layout.addWidget(usr_widget)
        usr_widget2 = UsrWidget(self.chat_scroll_content)
        usr_widget2.set_user_text("who are you")
        self.message_layout.addWidget(usr_widget2)

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.sparking)
        self.timer.start(1000)  # 每秒更新一次

        self.colon_visible = True

        # 初始化时钟显示
        self.update_time()

        # 按钮功能
        self.chat_num = 0  # 检测是否是第一次输入
        if self.chat_num == 0:
            self.record_btn.clicked.connect(self.start_chat)
        else:
            self.record_btn.clicked.connect(self.recording)

        self.chat_btn.clicked.connect(self.show_chat_page)
        self.set_btn.clicked.connect(self.show_set_page)
        self.return_btn.clicked.connect(self.show_main_page)
        self.return_btn2.clicked.connect(self.show_main_page)
        self.quit_btn.clicked.connect(QApplication.quit)
        self.light_btn.clicked.connect(self.show_light_page)
        self.wifi_btn.clicked.connect(self.show_wifi_page)
        self.bluetooth_btn.clicked.connect(self.show_bluetooth_page)
        self.language_btn.clicked.connect(self.switch_language)
        self.volume_btn.clicked.connect(self.show_volume_page)

    def start_chat(self):
        # 记录开始时间
        self.connect_db.set_start_date()
        # 先录音
        self.recording()
        chat_data = self.connect_db.get_chat_data()
        self.show_chats(chat_data)

    def recording(self):
        # 语音转文字
        question = gpt.voice2text(self.qus_path)
        # question = "who are you?"
        self.connect_db.add_chat_data("user", question)

    def show_chats(self, chat_data):
        messages = chat_data.get("messages", [])

        # for message in messages:
        #     role = message.get("role")
        #     if role == "user":
        #         usr_str = message.get("content", "")
        #         usr_widget = UsrWidget(self.chat_scroll_content)
        #         usr_widget.set_user_text(usr_str)
        #         self.message_layout.addWidget(usr_widget)
        #         print(f"Added User Message: {usr_str}")  # 调试信息
        #
        #     elif role == "echo":
        #         gpt_str = message.get("content", "")
        #         gpt_widget = GPTWidget(self.chat_scroll_content)
        #         gpt_widget.set_gpt_text(gpt_str)
        #         self.message_layout.addWidget(gpt_widget)
        #         print(f"Added GPT Message: {gpt_str}")  # 调试信息

        # 添加一个spacer item，使得消息能自动靠上显示
        # spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.message_layout.addItem(spacer_item)

        # 调整滚动条以显示最新消息
        # self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())

    def show_main_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_chat_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_set_page(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def show_wifi_page(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def show_bluetooth_page(self):
        self.ui.stackedWidget.setCurrentIndex(4)

    def show_light_page(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def show_volume_page(self):
        self.ui.stackedWidget.setCurrentIndex(6)

    def switch_language(self):
        print("switch language")

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

    def sparking(self):
        # Toggle the color of the colon
        text = self.spark_label.text()
        if self.colon_visible:
            new_text = text.replace(":", '<span style="color: transparent;">:</span>')
        else:
            new_text = text.replace('<span style="color: transparent;">:</span>', ":")
        self.colon_visible = not self.colon_visible
        self.spark_label.setText(new_text)