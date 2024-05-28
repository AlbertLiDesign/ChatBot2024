import sys
import json
import os

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from main_app import MainWindow


if __name__ == "__main__":
    flag = os.path.exists("../data/history.json")
    if not flag:
        os.mkdir("../data")
        with open("../data/history.json", "w") as f:
            f.write(json.dumps([]))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())