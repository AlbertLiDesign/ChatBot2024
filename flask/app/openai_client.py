import openai
from flask import current_app
from app.db import get_user_id, get_user_info, update_user_info, get_conversation_history, update_conversation_history
from app.utils import read_role_info

def get_openai_client():
    return openai.OpenAI(api_key=current_app.config['OPENAI_API_KEY'])

def collect_personal_info(username):
    user_id = get_user_id(username)
    user_info = get_user_info(user_id)
    
    missing_info = []
    if not user_info[0]:
        missing_info.append("name")
    if not user_info[1]:
        missing_info.append("date of birth")
    if not user_info[2]:
        missing_info.append("job")
    if not user_info[3]:
        missing_info.append("mental health status")
    if not user_info[4]:
        missing_info.append("hobby")
    if not user_info[5]:
        missing_info.append("physical health")
    if not user_info[6]:
        missing_info.append("other information")
    
    if missing_info:
        return f"Please provide your {', '.join(missing_info)}."
    else:
        return None

def update_personal_info(username, **kwargs):
    user_id = get_user_id(username)
    update_user_info(user_id, **kwargs)

def dialogue(user_input, username, intention, target):
    user_id = get_user_id(username)
    role_info, history_info, existing_intention, existing_target = get_conversation_history(user_id)
    user_info = get_user_info(user_id)
    
    if not role_info:
        role_info = read_role_info()
    
    if not existing_intention:
        existing_intention = intention
    
    if not existing_target:
        existing_target = target

    personal_info_prompt = collect_personal_info(username)
    if personal_info_prompt:
        return personal_info_prompt
    
    user_info_text = f"Name: {user_info[0]}, DOB: {user_info[1]}, Job: {user_info[2]}, Mental Health Status: {user_info[3]}, Hobby: {user_info[4]}, Physical Health: {user_info[5]}, Others: {user_info[6]}"
    
    conversation = [
        {"role": "system", "content": role_info + history_info + "\n" + user_info_text},
        {"role": "user", "content": user_input}
    ]

    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation
    )
    
    output_text = response.choices[0].message.content
    history_info += f"\nUser: {user_input}\nAssistant: {output_text}\n"
    update_conversation_history(user_id, role_info, history_info, existing_intention, existing_target)
    return output_text
