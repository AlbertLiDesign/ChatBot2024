import json
from datetime import datetime

class ConnectDB:
    def __init__(self):
        self.chat_db_path = "../data/history.json"


    def get_chat_data(self):
        with open(self.chat_db_path, "r") as f:
            chat_db = json.load(f)

        return chat_db

    def set_start_date(self):
        timestamp = datetime.utcnow().isoformat() + 'Z'  # 获取当前时间戳
        chat_db = self.get_chat_data()
        # 更新结束时间
        chat_db["start_time"] = timestamp

        # 将更新后的聊天记录写回文件
        with open(self.chat_db_path, "w", encoding='utf-8') as f:
            json.dump(chat_db, f, indent=4, ensure_ascii=False)

    def add_chat_data(self, role, content):
        timestamp = datetime.utcnow().isoformat() + 'Z'  # 获取当前时间戳
        chat_db = self.get_chat_data()
        chat_db["messages"].append({
            "timestamp": timestamp,
            "role": role,
            "content": content
        })

        # 更新结束时间
        chat_db["end_time"] = timestamp

        # 将更新后的聊天记录写回文件
        with open(self.chat_db_path, "w", encoding='utf-8') as f:
            json.dump(chat_db, f, indent=4, ensure_ascii=False)

    def reset(self):
        chat_db = {
            "session_id": "unique_session_id_12345",
            "start_time": datetime.utcnow().isoformat() + 'Z',
            "end_time": None,
            "participants": {
                "user": "user_id_67890",
                "assistant": "gpt-4o"
            },
            "messages": []
        }
        with open(self.chat_db_path, "w", encoding='utf-8') as f:
            json.dump(chat_db, f, indent=4, ensure_ascii=False)

