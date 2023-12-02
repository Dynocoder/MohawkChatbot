import openai
import time
import json

openai.api_key = "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"

# fetch the already made assistant
mohawk_asst = openai.beta.assistants.retrieve("asst_vqCb0zabVklaiOVYnnmP2HIv")

# create a thread
thread = openai.beta.threads.create()

# create a message
message = openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="who is eligible for scholarships?"
)

# run the message
run = openai.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=mohawk_asst.id
)





while run.status != "completed":
    time.sleep(0.2)
    # check the run status
    run = openai.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    



messages = openai.beta.threads.messages.list(thread_id=thread.id) if (run.status == "completed") else run.status





print(messages.data[0].content[0].text.value)


