from flask import Flask, render_template
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
import requests
import os

load_dotenv(override=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
# app.config['DEBUG'] = True
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(message):
    print('Message: ' + message)
    if message != "User has connected!":

        key = os.getenv('NLP_API')
        url = f'https://language.googleapis.com/v1/documents:analyzeSentiment?key={key}'
        header = {'Content-Type': 'application/json'}
        body = {
            "document": {
                "type": "PLAIN_TEXT",
                "language": "JA",
                "content": message
            }
        }
        res = requests.post(url, headers=header, json=body)
        result = res.json()
        score = result['documentSentiment']['score']
        set = [message, score]


        send(set, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
