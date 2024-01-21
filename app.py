import os

from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
import assemblyai as aai
import asyncio
import websocket
import json
from flask_socketio import SocketIO, send, emit
from threading import Thread
import pyaudio



client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
#set up assembly api key
ASSEMBLYAI_API_KEY = os.environ.get("ASSEMBLYAI_API_KEY")


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        reflection = request.form["Reading-level"]
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.6,
            messages=[
                {"role": "system","content": "You are a reading aid, prompt the user to input their reading level and output an appropriate 100-word long text to match."},
                {"role": "user", "content": reflection}
            ]
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)

# speach to text transcriber 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = os.path.join('/tmp', file.filename)
            file.save(filename)
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(filename)
            return transcript.text
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(FILE_URL)

print(transcript.text)

