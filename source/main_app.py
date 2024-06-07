from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout,\
    QWidget
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, QLocale, pyqtSlot
from PyQt5.QtGui import QPixmap

from source.gui.main_page import Ui_MainWindow

from source.connect_db import ConnectDB
from source.chat_class import BubbleLabel

from source.conversation_thread import RecordingThread, GPTThread, VoicePlayThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showFullScreen()

        self.show_main_page()  # 设置主页面

        # 各种文件的路径
        self.qus_path = "question.wav"
        self.ans_path = "answer.mp3"  # 使用openai的api，这里得改成mp3格式
        self.role_path = "role_settings.txt"

        self.connect_db = ConnectDB()

        # 初始化线程
        self.recording_thread = None
        self.gpt_thread = None
        self.vp_thread = None

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
        self.usr_icon = QPixmap("1.jpg")
        self.gpt_icon = QPixmap("1.jpg")

        self.chatWidget = QWidget()
        self.chat_layout = QVBoxLayout(self.chatWidget)
        self.chat_layout.addStretch(1)
        self.chat_scroll_area.setWidget(self.chatWidget)

        # 设置聊天窗口样式 隐藏滚动条
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.sparking)
        self.timer.start(1000)  # 每秒更新一次

        self.colon_visible = True

        # 初始化时钟显示
        self.update_time()

        self.record_btn.clicked.connect(self.conversation)
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

    def conversation(self):
        # 创建并启动录音线程
        self.recording_thread = RecordingThread(self.qus_path)
        self.recording_thread.result_ready.connect(self.handle_recording_result)
        self.recording_thread.start()

        # 禁用录音按钮
        self.record_btn.setEnabled(False)


    @pyqtSlot(str)
    def handle_recording_result(self, question):
        # 更新 UI，显示用户问题
        self.addBubble(question, is_user=True)
        self.connect_db.add_chat_data(role="user", content=question)

        # 创建并启动 GPT 线程
        self.gpt_thread = GPTThread(question, self.role_path, self.connect_db)
        self.gpt_thread.result_ready.connect(self.handle_gpt_result)
        self.gpt_thread.start()

    @pyqtSlot(str)
    def handle_gpt_result(self, answer):
        # 更新 UI，显示 GPT 回答
        self.addBubble(answer, is_user=False)

        # 创建并启动播放声音线程
        self.vp_thread = VoicePlayThread(answer, self.ans_path)
        self.vp_thread.finished_signal.connect(self.enable_record_btn)  # 连接完成信号
        self.vp_thread.start()

    @pyqtSlot()
    def enable_record_btn(self):
        # 启用录音按钮
        self.record_btn.setEnabled(True)

    def addBubble(self, message, is_user=True):
        bubble = BubbleLabel(message, is_user)
        alignment = Qt.AlignRight if is_user else Qt.AlignLeft
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, bubble, 0, alignment)
        self.chat_scroll_area.verticalScrollBar().setValue(self.chat_scroll_area.verticalScrollBar().maximum())

    def show_main_page(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def show_chat_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        # 记录开始时间
        self.connect_db.set_start_date()

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


