import json
from flask import Flask, request
import requests

app = Flask(__name__)

# Load cấu hình từ file config.json
with open("config.json", "r") as f:
    config = json.load(f)

PROJECT_CHAT_MAPPING = config["projects"]

def send_google_chat_message(chat_id, message):
    """ Gửi tin nhắn vào Google Chat """
    payload = {"text": message}
    headers = {"Content-Type": "application/json"}
    requests.post(chat_id, json=payload, headers=headers)

def send_telegram_message(chat_id, message):
    TELEGRAM_TOKEN = "8043847080:AAFHwUxFD0Te79qbM6kwJnWWPLKOU-Mno7M"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data and "object_kind" in data and data["object_kind"] == "merge_request":
        project_id = str(data["project"]["id"])  # Lấy projectID từ GitLab
        chat_id = PROJECT_CHAT_MAPPING.get(project_id)  # Tìm chatID tương ứng
        
        if chat_id:  # Nếu có chatID, gửi tin nhắn
            user = data["user"]["name"]
            title = data["object_attributes"]["last_commit"]["title"]
            url = data["object_attributes"]["last_commit"]["url"]
            message = f"🚀 *Merge Request Created!*\n👤 By: {user}\n📌 Title: {title}\n🔗 [View MR]({url})"
            # send_telegram_message(chat_id, message)
            send_google_chat_message(chat_id, message)
            return "OK", 200
        else:
            return "Project ID not found in config", 404
    return "Ignored", 400

@app.route("/")
def home():
    return "Hello, Railway is running!"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
