import sys
import json
import os

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from main_app import MainWindow

if __name__ == "__main__":
    flag = os.path.exists("../data/history.json")
    if not flag:
        os.makedirs("../data", exist_ok=True)  # 使用 makedirs 并确保父目录存在
        history_data = {
            "session_id": "unique_session_id_12345",
            "start_time": None,
            "end_time": None,
            "participants": {
                "user": "user_id_67890",
                "assistant": "gpt-4o"
            },
            "messages": []
        }
        with open("../data/history.json", "w", encoding='utf-8') as f:
            f.write(json.dumps(history_data, indent=4, ensure_ascii=False))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())