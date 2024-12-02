from event_stream_parse import parse
from flask import Flask, render_template, Response, url_for

import openai

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI()

app = Flask(__name__)

def generate(prompt):
    chat = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an HTML document writing machine. You write single HTML documents with any CSS or JavaScript written in-line with the HTML. You take the prompts for websites given by the user and translate them into documents. You also apply any necessary styles or scripts to make the site look aesthetically pleasing, interesting, and interactive."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return f'data: <div>{parse(chat.choices[0].message.content)}\ndata:</div>\n\n'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ai")
def ai():
    def eventStream():
        with open('prompts/index.prompt', 'r') as ifile:
            return generate(ifile.read())

    return Response(eventStream(), mimetype='text/event-stream')
