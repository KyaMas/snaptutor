import os

from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
import assembly as assemblyai

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
aai.settings.api_key = "dcebad47486340d59b89946e616c9a2c"


app = Flask(__name__)


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

transcriber = aai.Transcriber()

transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)
