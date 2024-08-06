from flask import Flask, send_file, jsonify, request
import os
import threading
import time
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_file(os.path.join(os.path.dirname(__file__), "public", "index.html"))

@app.route('/start', methods=['POST'])
def start_commenting():
    thread = threading.Thread(target=auto_comment)
    thread.start()
    return jsonify({"status": "started"}), 200

# Function to post comments
def post_comment(post_id, message):
    with open('token.txt', 'r') as file:
        access_token = file.read().strip()

    url = f'https://graph.facebook.com/{post_id}/comments'
    payload = {
        'message': message,
        'access_token': access_token
    }
    response = requests.post(url, data=payload)
    return response.json()

# Comments पोस्ट करना
def auto_comment():
    with open('file.txt', 'r') as file:
        post_links = [line.strip() for line in file.readlines()]

    with open('time.txt', 'r') as file:
        time_intervals = [int(line.strip()) for line in file.readlines()]

    with open('comments.txt', 'r') as file:
        comments = [line.strip() for line in file.readlines()]

    for i, post_link in enumerate(post_links):
        post_id = post_link.split('/')[-1]  # Assuming the post_id is the last part of the URL
        comment = comments[i % len(comments)]
        
        response = post_comment(post_id, comment)
        print(f'Commented on {post_link}: {response}')
        
        if i < len(time_intervals):
            time.sleep(time_intervals[i])

    print("All comments have been posted.")

# Function to ping the server
def ping_server():
    sleep_time = 10 * 60  # 10 minutes
    while True:
        time.sleep(sleep_time)
        try:
            response = requests.get('past_webserver.url', timeout=10)
            print(f"Pinged server with response: {response.status_code}")
        except requests.RequestException as e:
            if isinstance(e, requests.Timeout):
                print("Couldn't connect to the site URL..!")
            else:
                print(e)

# Start the ping function in a separate thread
ping_thread = threading.Thread(target=ping_server)
ping_thread.start()

# Serve static files from the "public" directory
app.static_folder = 'public'

# Start the Flask server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
