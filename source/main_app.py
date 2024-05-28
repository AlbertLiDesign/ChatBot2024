from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, QDate, QLocale

from gui.main_page import Ui_MainWindow

from connect_db import ConnectDB

import source.gpt as gpt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connect_db = ConnectDB()

        self.chat_btn = self.ui.dia_btn
        self.set_btn = self.ui.set_btn
        self.record_btn = self.ui.record_btn

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        # 初始化时钟显示
        self.update_time()

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

    def get_response(self):
        if __name__ == '__main__':
            message_input = self.message_input.toPlainText().strip()
            chat_db = self.connect_db.get_chat_data()

            # if message_input:
                #response_list = gpt.dialogue()

class CustomWidget(QWidget):
    # Create each chat in chat list
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create layout for chat title
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5,0,0,0)
