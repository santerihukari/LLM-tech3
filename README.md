# LLM-tech3
Technical exercise 3 for the course **Fine-tuning LLMs**

The setup has not been tested, so it might not run directly without resolving packages.

A full-stack sentiment analysis application using:
- **FastAPI** for the backend
- **Next.js (React)** for the frontend
- **Hugging Face Transformers & Groq API** for sentiment classification

---

## 📥 Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/santerihukari/sentiment-analysis-app.git
cd sentiment-analysis-app
```

---

## 🚀 Backend Setup (FastAPI)
### **2️⃣ Create and Activate a Conda Environment**
```bash

cd backend
conda create --name sentiment-env python=3.10 -y
conda activate sentiment-env
```
### **3️⃣ Install Python Dependencies**
```bash
python -m pip install -r requirements.txt
```

### **4️⃣ Start the API Server**

```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### ✅ API should now be running at:
### 👉 http://127.0.0.1:8000/docs (Swagger UI)

## 🎨 Frontend Setup (React/Next.js)
### **5️⃣ Install React Dependencies**


```bash
cd frontend/sentiment-ui
npm install
```


### 6️⃣ Start the Frontend
```bash
npm run dev
```
## 🔥 Using the API
### Analyze Sentiment (POST /analyze/)
 Use cURL, Postman, or Python requests:

```bash
curl -X 'POST' 'http://127.0.0.1:8000/analyze/' \
-H 'Content-Type: application/json' \
-d '{"text": "The movie was amazing!", "model": "custom"}'
```

