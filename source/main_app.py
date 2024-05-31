import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QVBoxLayout,\
    QWidget, QHBoxLayout, QLabel, QTextBrowser
from PyQt5.QtCore import Qt, QTimer, QTime, QDate, QLocale, QSize
from PyQt5.QtGui import QFont, QFontMetrics, QPixmap

from gui.main_page import Ui_MainWindow

from connect_db import ConnectDB
from chat_class import ChatClass

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
        self.sum=0

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
        self.chat_layout = QVBoxLayout(self.chat_scroll_content)
        self.usr_icon = QPixmap("1.jpg")
        self.gpt_icon = QPixmap("1.jpg")

        #设置聊天窗口样式 隐藏滚动条
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # self.message_layout = QVBoxLayout(self.chat_scroll_area)

        scrollbar = self.chat_scroll_area.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.adjustScrollToMaxValue) #监听窗口滚动条范围

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
        # chat_data = self.connect_db.get_chat_data()

    def recording(self):
        # 语音转文字
        # question = gpt.voice2text(self.qus_path)
        question = "who are you?"
        self.connect_db.add_chat_data("user", question)
        self.create_widget(question)
        self.set_widget(question)

    def create_widget(self, message):
        self.sum += 1
        if self.sum % 2:   # 根据判断创建左右气泡
            ChatClass.set_chat(self, self.usr_icon, message, Qt.LeftToRight)    # 调用new_widget.py中方法生成左气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列
        else:
            ChatClass.set_chat(self, self.gpt_icon, message, Qt.RightToLeft)   # 调用new_widget.py中方法生成右气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列

    def set_widget(self, message):
        font = QFont()
        font.setPointSize(12)
        fm = QFontMetrics(font)
        text_width = fm.width(message) + 115  # 根据字体大小生成适合的气泡宽度
        if self.sum != 0:
            if text_width > 350:  # 宽度上限
                text_width = int(self.textBrowser.document().size().width()) + 50  # 固定宽度
            self.widget.setMinimumSize(text_width, int(self.textBrowser.document().size().height()) + 40)  # 规定气泡大小
            self.widget.setMaximumSize(text_width, int(self.textBrowser.document().size().height()) + 40)  # 规定气泡大小
            self.chat_scroll_area.verticalScrollBar().setValue(10)

    def adjustScrollToMaxValue(self):
        scrollbar = self.chat_scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

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


