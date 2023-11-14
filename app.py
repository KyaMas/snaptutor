import os

from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get(".env"),
)

app = Flask(__name__)


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        reflection = request.form["reflection"]
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.6,
            messages=[
                {"role": "system","content": "Students will provide you with short reflections on emerging trends in the business world. Evaluate the reflections in terms of spelling and grammar, and in terms of evidence of critical thought. Provide a grade between 0 and 20, where 4 points are allocated for spelling and grammar, 4 points are allocated for critical thought, 4 points are allocated for providing background information, 4 points are allocated for overall cohesion and structure, 4 points are allocated for engagement with emerging business trends. Provide the feedback in rubric form."},
                {"role": "user", "content": reflection}
            ]
        )
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)

'''
Sample prompt:

Strong:
I appreciated Walmart's implementation of sustainable practices. Their implementation of LED lighting and sustainable energy will likely have a measurable impact. I am not sure whether this is an example of greenwashing, though, because they provided their statistics in cumulative terms, rather than their annual emissions reductions.

Weak:


'''
