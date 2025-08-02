from flask import Flask, render_template, request, session
from utils.pdf_processor import extract_chunks_from_pdf
from utils.embedder import build_index, search
from utils.prompts import build_prompt
from openai import AzureOpenAI
import os

app = Flask(__name__)
app.secret_key = 'your-secret'

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)

# Load & preprocess PDF
chunks = extract_chunks_from_pdf("Luat xu ly VPHC tieng Anh.pdf")
print(f"Extracted {len(chunks)} chunks from PDF.")
index = build_index(chunks)

@app.route("/", methods=["GET", "POST"])
def chat():
    if "messages" not in session:
        session["messages"] = []

    reply = ""
    if request.method == "POST":
        user_input = request.form["message"]
        session["messages"].append({"role": "user", "content": user_input})

        # Search context
        context = search(user_input, index)

        # Create prompt
        full_prompt = build_prompt(user_input, context)

        # Chat Completion
        completion = client.chat.completions.create(
            model="GPT-4.1",
            messages=[{"role": "system", "content": "Bạn là luật sư dày dặn kinh nghiệm."}] +
                     session["messages"][-4:] +
                     [{"role": "user", "content": full_prompt}]
        )
        reply = completion.choices[0].message.content
        session["messages"].append({"role": "assistant", "content": reply})

    return render_template("index.html", messages=session["messages"], reply=reply)

if __name__ == "__main__":
    app.run(debug=True)
