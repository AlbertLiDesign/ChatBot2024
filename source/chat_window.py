from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from gui.usr_widget import Ui_Form as usr_form
from gui.gpt_widget import Ui_Form as gpt_form
class UsrWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_user = usr_form()
        self.ui_user.setupUi(self)

        self.user_label = self.ui_user.usr_chat

    def set_user_text(self, question):
        self.user_label.setText(question)


class GPTWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui_gpt = gpt_form()
        self.ui_gpt.setupUi(self)

        self.gpt_label = self.ui_gpt.gpt_chat
    def set_gpt_text(self, answer):
        self.gpt_label.setText(answer)

class ChatWindow(QWidget):
    def __init__(self, parent=None, chat_data=None):
        super().__init__(parent)

        self.chat_data = chat_data

        self.main_verticalLayout = QVBoxLayout(self)
        self.main_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.main_verticalLayout.setSpacing(0)
        self.main_verticalLayout.setObjectName("main_verticalLayout")

        self.show_chats()

    def show_chats(self):
        messages = self.chat_data.get("messages")
        for message in messages:
            if message.get("role") == "user":
                usr_str = message.get("content")
                usr_widget = UsrWidget()
                usr_widget.set_user_text(usr_str)
                self.main_verticalLayout.addWidget(usr_widget)

            if message.get("role") == "echo":
                gpt_str = message.get("content")
                gpt_widget = GPTWidget()
                gpt_widget.set_gpt_text(gpt_str)
                self.main_verticalLayout.addWidget(gpt_widget)


        # spacerItem = QSpacerItem(20, 293, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.main_verticalLayout.addItem(spacerItem)
        self.setLayout(self.main_verticalLayout)

        # 调整滚动条以显示最新消息
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())