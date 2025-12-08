from flask import Flask, render_template, request
from model import retrieve_chunks, rag_chat

app = Flask(__name__)
# Stores the conversation
history = []
# to handleget and post requests
@app.route("/", methods=["GET", "POST"])
def retrive():
    global history
    if request.method == "POST":
        # get the user query
        user_query = request.form["query"]
        # retrieve relevant chunks
        context = retrieve_chunks(user_query)
        # generate bot answer
        answer = rag_chat(user_query, context)
        # append the user query and bot answer in the history 
        history.append({"role": "user", "content": user_query})
        history.append({"role": "bot", "content": answer})
    # redering chat with chat history
    return render_template("index.html", chat_history=history)

if __name__ == '__main__':
    app.run(debug=True)
