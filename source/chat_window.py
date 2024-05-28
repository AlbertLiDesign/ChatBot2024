from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, QDate, QLocale

from gui.user_widget import Ui_Form as user_form
from gui.gpt_widget import Ui_Form as gpt_form
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