from event_stream_parse import event_streamify, parse
from flask import Flask, render_template, Response, render_template_string, send_file, send_from_directory, url_for

import openai

from dotenv import load_dotenv
import os


DEBUGGING = False


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI()

app = Flask(__name__)

def generate(prompt):
    if DEBUGGING:
        return 'data: <div>debugging</div>\n\n'
    
    chat = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an HTML document writing machine. You write single HTML documents with any CSS or JavaScript written in-line with the HTML. You take the prompts for websites given by the user and translate them into documents. You also apply any necessary styles (including fonts) or scripts to make the site look aesthetically pleasing, interesting, and interactive. You do not reply with anything other than the raw HTML content. Do not include any copyright symbols."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )
    return event_streamify(render_template_string(parse(chat.choices[0].message.content)))


@app.route("/")
@app.route("/<page>")
def index(page="index"):
    return render_template("index.html", page=page)

@app.route("/ai/<page>")
def ai(page="index"):
    def eventStream():
        with open(f'prompts/{page}.prompt', 'r') as ifile:
            return generate(ifile.read())

    return Response(eventStream(), mimetype='text/event-stream')

@app.route("/prompts/<page>.prompt")
def display_prompt(page):
    return send_from_directory('prompts', f'{page}.prompt', mimetype="text/plain")


@app.route("/showcaise")
def showcaise():
    return render_template("showcaise.html")