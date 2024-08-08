from flask import Flask, send_file
import os
import threading
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "public", "index.html"))

# Load configurations from files
def load_config():
    with open('Token.txt', 'r') as file:
        token = file.read().strip()
    with open('Time.txt', 'r') as file:
        sleep_time = int(file.read().strip())
    return token, sleep_time

token, sleep_time = load_config()

# Function to auto-post messages on Facebook
def post_message():
    while True:
        try:
            # Your code to post message on Facebook using token
            url = 'https://graph.facebook.com/YOUR_POST_ID/comments'
            message = 'Your message here'
            payload = {'message': message, 'access_token': token}
            response = requests.post(url, data=payload)
            print(f"Posted message with response: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {e}")
        time.sleep(sleep_time)

# Start the post message function in a separate thread
post_thread = threading.Thread(target=post_message)
post_thread.start()

# Start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(port=port, debug=True)
