from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import json, os, base64
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")
SYSTEM_PROMPT = """You are an advanced AI medical diagnostic system trained across four 
specializations: dermatology, respiratory medicine, hematology, and general medicine.

Analyze ALL provided information — symptoms, patient details, and any medical image or 
lab report — then return ONLY a raw JSON object with no markdown, no backticks, no preamble.

Return exactly this structure:
{
  "primary_diagnosis": {
    "disease": "disease name",
    "category": "skin | respiratory | blood | general",
    "probability": 87,
    "severity": "mild | moderate | severe | critical",
    "description": "2-3 sentence clinical description of this condition"
  },
  "differential_diagnoses": [
    {
      "disease": "disease name",
      "category": "skin | respiratory | blood | general",
      "probability": 65,
      "severity": "mild | moderate | severe | critical",
      "key_indicator": "one sentence — what symptom/finding points to this"
    },
    {
      "disease": "disease name",
      "category": "skin | respiratory | blood | general",
      "probability": 45,
      "severity": "mild | moderate | severe | critical",
      "key_indicator": "one sentence — what symptom/finding points to this"
    },
    {
      "disease": "disease name",
      "category": "skin | respiratory | blood | general",
      "probability": 30,
      "severity": "mild | moderate | severe | critical",
      "key_indicator": "one sentence — what symptom/finding points to this"
    },
    {
      "disease": "disease name",
      "category": "skin | respiratory | blood | general",
      "probability": 20,
      "severity": "mild | moderate | severe | critical",
      "key_indicator": "one sentence — what symptom/finding points to this"
    }
  ],
  "detected_abnormalities": ["abnormality 1", "abnormality 2"],
  "risk_factors": ["risk factor 1", "risk factor 2"],
  "recommended_tests": ["test 1", "test 2", "test 3"],
  "treatment_suggestions": ["treatment 1", "treatment 2"],
  "urgency": "routine | within_48h | same_day | emergency",
  "urgency_reason": "one sentence explaining the urgency level",
  "overall_confidence": 78,
  "analysis_basis": "symptoms_only | image_only | symptoms_and_image"
}

Rules:
- Primary diagnosis must have highest probability
- All probabilities must be different and in descending order
- Be medically precise and conservative
- If image is provided, analyze it thoroughly for visual indicators
- Raw JSON only — absolutely no other text"""


def encode_image(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def clean_json(text: str) -> str:
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            if part.startswith("json"):
                text = part[4:]
                break
            elif "{" in part:
                text = part
                break
    start = text.find("{")
    end = text.rfind("}") + 1
    if start != -1 and end > 0:
        text = text[start:end]
    return text.strip()


@app.post("/api/detect")
async def detect_disease(
    symptoms: str = Form(""),
    age: str = Form(""),
    sex: str = Form(""),
    duration: str = Form(""),
    severity: str = Form(""),
    medical_history: str = Form(""),
    image: Optional[UploadFile] = File(None),
):
    if not symptoms and not image:
        raise HTTPException(status_code=400, detail="Provide symptoms or an image")

    # Build patient context
    parts = []
    if symptoms:        parts.append(f"Symptoms: {symptoms}.")
    if age:             parts.append(f"Age: {age}.")
    if sex:             parts.append(f"Biological sex: {sex}.")
    if duration:        parts.append(f"Duration: {duration}.")
    if severity:        parts.append(f"Severity: {severity}.")
    if medical_history: parts.append(f"Medical history: {medical_history}.")
    context = " ".join(parts) or "No symptoms — analyze image only."

    try:
        if image:
            image_bytes = await image.read()
            b64 = encode_image(image_bytes)
            ext = image.filename.split(".")[-1].lower()
            mime = "image/jpeg" if ext in ["jpg", "jpeg"] else f"image/{ext}"

            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{b64}",
                                "detail": "high"
                            }
                        },
                        {
                            "type": "text",
                            "text": f"Patient info: {context}\n\nAnalyze this medical image together with the patient information. Provide full diagnostic comparison."
                        }
                    ]
                }
            ]
        else:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Patient info: {context}\n\nProvide full diagnostic comparison based on these symptoms."
                }
            ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.1,
            max_tokens=2048,
        )

        raw = response.choices[0].message.content
        cleaned = clean_json(raw)
        result = json.loads(cleaned)
        result["model_used"] = MODEL
        return result

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse response: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenAI error: {str(e)}")


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}