from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, QDate, QLocale

from gui.main_page import Ui_MainWindow
from gui.user_widget import Ui_Form as user_form
from gui.gpt_widget import Ui_Form as gpt_form

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        # 初始化时钟显示
        self.update_time()

        self.ui.dia_btn.clicked.connect(self.show_chat_page)
        self.ui.set_btn.clicked.connect(self.show_set_page)

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


# class ChatPage(QWidget):
#     def __init__(self, parent=None, chat_message=None, chat_data=None):
#         super().__init__(parent)
#         self.ui_chat = chat_form()
#         self.ui_chat.setupUi(self)
#
#         self.chat_data = chat_data
#
#         self.main_verticalLayout = QVBoxLayout(self)
#         self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
#         self.main_verticalLayout.setSpacing(0)
#         self.main_verticalLayout.setObjectName("main_verticalLayout")
#
#         self.chat_data={
#             "title": "",
#             "chat_list": []
#         }
#
#         if self.chat_data:
#             self.chat_data["title"] = self.chat_data["title"]
#             self.chat_data["chat_list"] += self.chat_data["chat_list"]
#
#         self.show_chats()
#
#     def show_chats(self):
#         chat_list = self.chat_data.get("chat_list")
#         for chat in chat_list:
#             input_str=chat.get("")



class UserWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_user = user_form()
        self.ui_user.setupUi(self)

        self.user_label = self.ui_user.message

    def set_user_text(self, question):
        self.user_label.setText(question)


class GPTWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_gpt = gpt_form()
        self.ui_gpt.setupUi(self)

        self.gpt_label = self.ui_gpt.message
    def set_gpt_text(self, answer):
        self.gpt_label.setText(answer)