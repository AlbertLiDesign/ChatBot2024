from PyQt5.QtWidgets import QLabel, QSizePolicy
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QTextOption

class BubbleLabel(QLabel):
    def __init__(self, text, is_user=True):
        super().__init__()
        self.is_user = is_user
        self.setText(text)
        self.setFont(QFont('Segoe UI', 12))
        self.setWordWrap(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStyleSheet(self.get_stylesheet())
        self.setMaximumWidth(380)
        self.adjustSize()

    def get_stylesheet(self):
        if self.is_user:
            return """
                QLabel {
                    background-color: rgb(62, 204, 145);
                    border: none;
                    border-radius: 10px;
                    padding: 5px 10px;
                    margin: 2px;
                    color: rgb(0, 0, 0);
                }
            """
        else:
            return """
                QLabel {
                    background-color: rgb(45, 45, 45);
                    border: none;
                    border-radius: 10px;
                    padding: 5px 10px;
                    margin: 2px;
                    color: rgb(255, 255, 255);
                }
            """

    def sizeHint(self):
        max_width = 300  # 限制文本宽度以确保正确换行
        metrics = self.fontMetrics()
        text_rect = metrics.boundingRect(0, 0, max_width, 0, Qt.TextWordWrap, self.text())
        text_width = min(max_width, text_rect.width() + 20)  # 增加一些宽度以适应 padding
        text_height = text_rect.height() + 20  # 增加一些高度以适应 padding
        return QSize(text_width, text_height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.setFixedHeight(self.sizeHint().height())
