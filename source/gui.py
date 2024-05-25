import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer, QTime, QDate, QLocale

from mainPage import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 创建一个定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新一次

        # 初始化时钟显示
        self.update_time()

    def update_time(self):
        # 设置应用程序语言环境为英语
        english_locale = QLocale(QLocale.English, QLocale.UnitedStates)
        QLocale.setDefault(english_locale)

        current_time = QTime.currentTime()
        current_day = QDate.currentDate()
        current_date = QDate.currentDate()

        formatted_time = english_locale.toString(current_time, 'hh:mm')
        formatted_day = english_locale.toString(current_day, 'dddd')
        formatted_date = english_locale.toString(current_date, 'dd MMM')

        self.time_label.setText(formatted_time)
        self.day_label.setText(formatted_day)
        self.date_label.setText(formatted_date)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())