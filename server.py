import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

history = []

def smart_classify(name):
    name = name.lower()

    if any(x in name for x in ["cv", "resume", "job", "portfolio"]):
        return "Career"

    if any(x in name for x in ["invoice", "bill", "receipt", "payment"]):
        return "Finance"

    if any(x in name for x in ["screenshot", "img", "photo", "image"]):
        return "Images"

    if any(x in name for x in ["movie", "series", "video", "clip"]):
        return "Media"

    if any(x in name for x in ["project", "code", "app", "script"]):
        return "Projects"

    return "Other"


@app.route("/organize", methods=["POST"])
def organize():
    data = request.json
    files = data.get("files", [])

    plan = []

    for f in files:
        plan.append({
            "file": f["name"],
            "move_to": smart_classify(f["name"])
        })

    history.append({
        "time": datetime.now().isoformat(),
        "action": "organize",
        "plan": plan
    })

    return jsonify({
        "status": "success",
        "count": len(plan),
        "plan": plan
    })


@app.route("/stats", methods=["POST"])
def stats():
    data = request.json
    files = data.get("files", [])

    report = {}

    for f in files:
        ext = f["name"].split(".")[-1] if "." in f["name"] else "no_ext"
        report[ext] = report.get(ext, 0) + 1

    return jsonify({
        "status": "success",
        "stats": report
    })


@app.route("/undo", methods=["POST"])
def undo():
    if not history:
        return jsonify({"status": "empty"})

    last = history.pop()

    return jsonify({
        "status": "reverted",
        "reverted_action": last,
        "remaining_steps": len(history)
    })


if __name__ == "__main__":
    app.run(debug=True)