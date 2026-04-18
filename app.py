# =============================================================
# app.py — Verifai Flask Backend
# =============================================================
# Routes:
#   GET  /              → login page
#   GET  /login         → login page
#   GET  /register      → register page
#   GET  /dashboard     → dashboard (protected via JS auth)
#   POST /predict       → JSON API: { text } → { result, confidence, score }
# =============================================================

import pickle
import os
import re
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (needed for JS fetch)

# ── Load model ────────────────────────────────────────────────
MODEL_PATH      = os.path.join("model", "model.pkl")
VECTORIZER_PATH = os.path.join("model", "vectorizer.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    print("=" * 55)
    print("  ERROR: Model files not found in /model folder.")
    print("  Run:  python train_model.py   first.")
    print("=" * 55)
    exit(1)

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)

print("✅ Model loaded from /model/")

# ── Page routes ───────────────────────────────────────────────
@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Accepts JSON: { "text": "..." }
    Returns JSON: {
        "result":     "fake" | "real",
        "label":      "Likely misinformation" | "Appears credible",
        "confidence": 91,        ← percentage (int)
        "score":      9,         ← authenticity score 0-100
        "explanation": "..."
    }
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    # Validation
    if not text:
        return jsonify({"error": "No text provided."}), 400
    if len(text.split()) < 4:
        return jsonify({"error": "Please enter at least 4 words."}), 400

    # Predict
    vec        = vectorizer.transform([text])
    prediction = model.predict(vec)[0]          # 0=real, 1=fake
    proba      = model.predict_proba(vec)[0]    # [p_real, p_fake]
    confidence = int(round(max(proba) * 100))

    if prediction == 1:
        score       = max(5,  100 - confidence)
        label       = "Likely misinformation"
        result      = "fake"
        explanation = (
            "This content contains patterns commonly found in misleading "
            "or unverified news — such as sensational language, exaggerated "
            "claims, or missing credible sources. We recommend verifying "
            "with a trusted outlet before sharing."
        )
    else:
        score       = min(98, confidence)
        label       = "Appears credible"
        result      = "real"
        explanation = (
            "This content aligns with the patterns of factual, well-sourced "
            "reporting. The language is measured and the structure matches "
            "professional journalism. Always cross-reference important news "
            "with multiple independent sources."
        )

    return jsonify({
        "result":      result,
        "label":       label,
        "confidence":  confidence,
        "score":       score,
        "explanation": explanation,
    })

if __name__ == "__main__":
    print("\n🚀 Verifai starting...")
    print("📡 Open: http://127.0.0.1:5000\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
