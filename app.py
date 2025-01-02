from flask import Flask, render_template, request, jsonify
import openai
import time
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

API_KEY = os.getenv("API_KEY")
ASSISTANT = os.getenv("ASSISTANT")

if ASSISTANT and API_KEY:
    client = openai.OpenAI(api_key=API_KEY)  # Initialize client with API key
    # fetch the already made assistant
    mohawk_asst = client.beta.assistants.retrieve(
        ASSISTANT,
    )
    # create a thread
    thread = client.beta.threads.create(
    )

@app.route('/')
def index():
    if not ASSISTANT or not API_KEY:
        return render_template("outage.html")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    q = request.form.get("prompt", 'Not Found')
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=q
    )
    # run the message
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=mohawk_asst.id
    )
    
    # waiting until the run is complete
    while run.status != "completed":
        time.sleep(0.2)
        # check the run status
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    messages = client.beta.threads.messages.list(thread_id=thread.id) if (run.status == "completed") else run.status
    response = messages.data[0].content[0].text.value
    html_content = f"""<div class="message response-message">{response}</div>"""
    return html_content

if __name__ == '__main__':
    app.run()
