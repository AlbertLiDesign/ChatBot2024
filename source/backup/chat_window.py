from PyQt5.QtWidgets import QWidget, QSpacerItem, QSizePolicy

from source.gui.backup.usr_widget import Ui_Form as usr_form
from source.gui.backup.gpt_widget import Ui_Form as gpt_form
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
    def __init__(self, parent=None, layout=None, chat_data=None):
        super().__init__(parent)

        self.chat_data = chat_data
        self.layout = layout
        self.show_chats()

    def show_chats(self):
        messages = self.chat_data.get("messages", [])

        for message in messages:
            role = message.get("role")
            if role == "user":
                usr_str = message.get("content", "")
                usr_widget = UsrWidget()
                usr_widget.set_user_text(usr_str)
                self.layout.addWidget(usr_widget)
                print(f"Added User Message: {usr_str}")  # 调试信息

            elif role == "echo":
                gpt_str = message.get("content", "")
                gpt_widget = GPTWidget(self.chat_scroll_content)
                gpt_widget.set_gpt_text(gpt_str)
                self.layout.addWidget(gpt_widget)
                print(f"Added GPT Message: {gpt_str}")  # 调试信息

        # 添加一个spacer item，使得消息能自动靠上显示
        spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_item)