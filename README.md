# 🔬 AI Disease Detector
> Full-stack AI-powered disease detection using LLaMA 3.3 70B

A web application that takes patient symptoms and medical images as input and returns a full clinical diagnostic report — powered by a Large Language Model, built with Python and FastAPI.

---

## 🖥️ What it does

- Enter symptoms using quick-add buttons or type manually
- Upload X-ray, skin photo, or lab report (optional)
- Fill in patient info — age, sex, duration, severity
- Get full diagnostic report in 2-3 seconds

---

## ✨ Features

- 🩺 Differential diagnosis — top 5 diseases ranked by probability
- 🩻 Medical image analysis — upload X-rays, skin photos, lab reports
- 🚨 Urgency detection — routine / within 48h / same day / emergency
- 📋 Full clinical report — abnormalities, risk factors, recommended tests, treatment suggestions
- 🔬 4 disease categories — skin, respiratory, blood, general medicine
- ⚡ Fast — results in 2-3 seconds via Groq API

---

## 🧠 AI Concepts Used

| Concept | How it is used |
|---|---|
| Large Language Model | LLaMA 3.3 70B reasons across symptoms to predict diseases |
| Prompt Engineering | System prompt controls model role, output format, and behavior |
| Zero-Shot Learning | Model predicts diseases without any custom training data |
| Natural Language Understanding | Maps colloquial symptoms to clinical terms |
| Multimodal AI | Processes both image and text together |
| Calibrated Uncertainty | Returns probability scores for each diagnosis |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| AI Model | LLaMA 3.3 70B via Groq API |
| API Client | OpenAI Python SDK |
| Server | uvicorn |
| Config | python-dotenv |
| Image processing | base64 Python stdlib |

---

## 🗂️ Project Structure
disease-detector/
│
├── backend/
│   ├── main.py        ← FastAPI backend
│   └── .env           ← API keys (never commit this)
│
└── frontend/
├── welcome.html   ← Landing page
└── index.html     ← Detector interface

---

## 🚀 Getting Started

### 1. Get a free Groq API key

Go to console.groq.com → Sign up → API Keys → Create key

### 2. Clone the repo

```bash
git clone https://github.com/VanshikaAsthana/disease-detector.git
cd disease-detector
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn openai python-dotenv
```

### 4. Create .env file inside the backend folder
GROQ_API_KEY=gsk_...your key here...
GROQ_MODEL=llama-3.3-70b-versatile

### 5. Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 6. Open the frontend

Open frontend/welcome.html in your browser

---

## 🔄 How It Works
User enters symptoms + optional image
↓
JavaScript fetch() sends FormData to FastAPI
↓
FastAPI validates input + encodes image to base64
↓
Groq API called with system prompt + patient context + image
↓
LLaMA 3.3 70B reasons across all inputs
↓
JSON response parsed and cleaned
↓
Full diagnostic report returned to browser
↓
Results rendered dynamically on screen

---

## 📤 API Reference

### POST /api/detect

Request multipart/form-data:

| Field | Type | Description |
|---|---|---|
| symptoms | string | Comma separated symptom list |
| age | string | Patient age |
| sex | string | male or female |
| duration | string | How long symptoms lasted |
| severity | string | mild / moderate / severe |
| medical_history | string | Any relevant history |
| image | file | X-ray, skin photo, lab report (optional) |

Response application/json:

```json
{
  "primary_diagnosis": {
    "disease": "Influenza",
    "category": "general",
    "probability": 84,
    "severity": "moderate",
    "description": "..."
  },
  "differential_diagnoses": [],
  "detected_abnormalities": [],
  "risk_factors": [],
  "recommended_tests": [],
  "treatment_suggestions": [],
  "urgency": "within_48h",
  "urgency_reason": "See a doctor within 48 hours.",
  "overall_confidence": 84,
  "model_used": "llama-3.3-70b-versatile"
}
```

### GET /health

Returns server status and model being used.

---

## ⚠️ Disclaimer

This project is for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider.

---

## 📚 References

- Groq Documentation — console.groq.com/docs
- FastAPI Documentation — fastapi.tiangolo.com
- LLaMA 3 — ai.meta.com/llama
- Vaswani et al. 2017. Attention Is All You Need. NeurIPS
- Brown et al. 2020. Language Models are Few-Shot Learners. NeurIPS

---

## 👩‍💻 Author

Vanshika
Built as part of an AI and ML academic project 2025-26

---

⭐ If you found this useful, consider giving it a star on GitHub
