<<<<<<< HEAD
# Verifai — Fake News Detection Web App

A production-style news authenticity checker with authentication, a modern SaaS UI, a Python/Flask backend, and a complete CI/CD pipeline.

---

## Architecture

```
Browser (HTML/CSS/JS)
        │
        │  HTTP requests
        ▼
  Flask App (app.py)
        │
        ├── GET  /login      → login.html
        ├── GET  /register   → register.html
        ├── GET  /dashboard  → dashboard.html
        │
        └── POST /predict    → load model → predict → JSON response
                                    │
                             model/model.pkl
                             model/vectorizer.pkl
                             (created by train_model.py)
```

## Folder Structure

```
verifai/
│
├── app.py                  ← Flask server (routes + /predict API)
├── train_model.py          ← Train & save ML model
├── requirements.txt        ← Python dependencies
├── Dockerfile              ← Container build
├── docker-compose.yml      ← Multi-service orchestration
├── Jenkinsfile             ← CI/CD pipeline
├── .gitignore
│
├── model/                  ← Auto-created by train_model.py
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── templates/
│   ├── login.html          ← Login page
│   ├── register.html       ← Register page
│   └── dashboard.html      ← Main app dashboard
│
└── static/
    ├── auth.css            ← Login/Register styles
    └── dashboard.css       ← Dashboard styles
```

---

## Quick Start (Local)

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/verifai.git
cd verifai

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train the model (creates model/ folder)
python train_model.py

# 5. Start the app
python app.py

# 6. Open browser
# http://127.0.0.1:5000
```

**Demo credentials:** `demo@verifai.com` / `demo1234`

---

## Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or manually
docker build -t verifai .
docker run -p 5000:5000 verifai
```

---

## Deploy to Render (Free)

1. Push your code to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Settings:
   - Build command: `pip install -r requirements.txt && python train_model.py`
   - Start command: `gunicorn app:app`
5. Click Deploy — your live URL is ready in ~2 minutes

---

## GitHub Push Commands

```bash
git init
git add .
git commit -m "Initial commit: Verifai fake news detector"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/verifai.git
git push -u origin main
```

---

## Authentication Flow

```
Register → credentials stored in localStorage (base64 password)
Login    → compare against localStorage → set session object
Dashboard → JS checks session on load → redirect to /login if missing
Logout   → clear session → redirect to /login
```

> Note: localStorage auth is for demo/college use. For production, use server-side sessions with a database.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JS |
| Backend | Python 3.11, Flask |
| ML | Scikit-learn (Logistic Regression + TF-IDF) |
| Auth | localStorage (frontend demo) |
| DevOps | Docker, Docker Compose, Jenkins, GitHub |
| Hosting | Render / Vercel (static proxy) |
=======
# fakenewsdetection
>>>>>>> 15fdb99e2e7b0d44b364b424a7954b361a367110
