import os
import json
import shutil
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =========================
# YOUR ENGINE (UNCHANGED)
# =========================

DEFAULT_FOLDER_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Code": [".py", ".js", ".html", ".css", ".ts"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
}

HISTORY_FILE = "history.json"


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def get_destination(extension):
    extension = extension.lower()
    for folder, exts in DEFAULT_FOLDER_MAP.items():
        if extension in exts:
            return folder
    return "Other"


# =========================
# ORGANIZE (NOW FIXED)
# =========================

@app.route("/organize", methods=["POST"])
def organize():
    data = request.json
    files = data.get("files", [])

    plan = []
    history = load_history()

    for f in files:
        name = f["name"]
        ext = os.path.splitext(name)[1]

        category = get_destination(ext)

        plan.append({
            "file": name,
            "move_to": category
        })

    history.append({
        "time": datetime.now().isoformat(),
        "action": "organize",
        "plan": plan
    })

    save_history(history)

    return jsonify({
        "status": "success",
        "count": len(plan),
        "plan": plan
    })


# =========================
# STATS (FIXED)
# =========================

@app.route("/stats", methods=["POST"])
def stats():
    data = request.json
    files = data.get("files", [])

    report = {}

    for f in files:
        ext = os.path.splitext(f["name"])[1] or "no_ext"
        report[ext] = report.get(ext, 0) + 1

    return jsonify({
        "status": "success",
        "stats": report
    })


# =========================
# UNDO (FIXED)
# =========================

@app.route("/undo", methods=["POST"])
def undo():
    history = load_history()

    if not history:
        return jsonify({"status": "nothing_to_undo"})

    last = history.pop()
    save_history(history)

    return jsonify({
        "status": "success",
        "reverted_action": last
    })


if __name__ == "__main__":
    app.run(debug=True)