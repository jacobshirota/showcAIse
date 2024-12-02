from event_stream_parse import parse
from flask import Flask, render_template, Response, url_for

import openai

from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ai")
def ai():
    def eventStream():
        chat = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an HTML document writing machine. You write single HTML documents with any CSS or JavaScript written in-line with the HTML. You take the prompts for websites given by the user and translate them into documents."},
                {"role": "user", "content": "Write a unique and interactive portfolio website for a Computer Science student named Jacob Shirota who is set to graduate in December of 2024. Jacob has interests in cybersecurity, data sciences, and software engineering. Jacob is the leader of the Naitonal Cyber League team at Biola University and recently led the team to an all-time-best finish of 61st place, with a personal best finish within the top 100 participants. Include a headshot of him located at /static/profile.png"}
            ],
            stream=False
        )

        return f'data: <div>{parse(chat.choices[0].message.content)}\ndata:</div>\n\n'

    return Response(eventStream(), mimetype='text/event-stream')
