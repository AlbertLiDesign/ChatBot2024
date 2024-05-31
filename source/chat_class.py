from PyQt5 import QtCore, QtWidgets
class ChatClass:
    def set_chat(self,ico,text,dir):  #头像，文本，方向
        self.widget = QtWidgets.QWidget(self.chat_scroll_content)
        self.widget.setLayoutDirection(dir)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(ico)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textBrowser.setStyleSheet("padding:10px;\n"
                                       "background-color: rgb(45,45,45);\n"
                                       "color: rgb(255,255,255);\n"
                                       "font: 12 pt \"Segoe UI\";")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 0))

        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout.addWidget(self.textBrowser)
        self.chat_layout.addWidget(self.widget)
