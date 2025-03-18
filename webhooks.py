from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = "8043847080:AAFHwUxFD0Te79qbM6kwJnWWPLKOU-Mno7M"
CHAT_ID = "-1002290882824"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data and "object_kind" in data and data["object_kind"] == "merge_request":
        user = data["user"]["name"]
        title = data["object_attributes"]["last_commit"]["title"]
        url = data["object_attributes"]["last_commit"]["url"]
        message = f"🚀 *Merge Request Created!*\n👤 By: {user}\n📌 Title: {title}\n🔗 [View MR]({url})"
        send_telegram_message(message)
        return "OK", 200
    return "Ignored", 400

@app.route("/")
def home():
    return "Hello, Railway is running!"

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
