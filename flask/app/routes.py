from flask import Blueprint, request, jsonify
from app.openai_client import dialogue, update_personal_info

main = Blueprint('main', __name__)

@main.route('/dialogue', methods=['POST'])
def handle_dialogue():
    data = request.json
    user_input = data['user_input']
    username = data['username']
    intention = data.get('intention', '')
    target = data.get('target', '')
    
    try:
        response = dialogue(user_input, username, intention, target)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/update_info', methods=['POST'])
def handle_update_info():
    data = request.json
    username = data['username']
    info = data['info']
    
    try:
        update_personal_info(username, **info)
        return jsonify({"response": "Information updated successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
