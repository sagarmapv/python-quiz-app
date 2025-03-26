from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("quiz_data.json") as f:
    all_questions = json.load(f)

def get_topics():
    topic_map = {}
    for q in all_questions:
        topic = q["topic"]
        if topic not in topic_map:
            topic_map[topic] = 0
        topic_map[topic] += 1
    return topic_map

@app.route("/")
def home():
    topics = get_topics()
    return render_template("index.html", topics=topics)

@app.route("/quiz/<topic>")
def quiz(topic):
    topic_questions = [q for q in all_questions if q["topic"].lower() == topic.lower()]
    all_topics = list(get_topics().keys())
    return render_template("quiz_one_by_one.html", topic=topic, questions=topic_questions, topic_sequence=all_topics)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    score = 0
    detailed = []
    for q in data["responses"]:
        correct = q["selected"] == q["answer"]
        detailed.append({"question": q["question"], "correct": correct, "topic": q["topic"]})
        if correct:
            score += 1
    return jsonify({"score": score, "total": len(data["responses"]), "details": detailed})

if __name__ == "__main__":
    app.run(debug=True)
