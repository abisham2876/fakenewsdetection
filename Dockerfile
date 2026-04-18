# =============================================================
# Dockerfile — Verifai
# =============================================================
# Build:   docker build -t verifai .
# Run:     docker run -p 5000:5000 verifai
# =============================================================

FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Train the model so model/ files exist inside the image
RUN python train_model.py

# Expose Flask port
EXPOSE 5000

# Start with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
