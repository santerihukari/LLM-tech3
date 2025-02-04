import requests
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from groq import Groq

# Load fine-tuned IMDB sentiment analysis model
model_path = "./fine_tuned_model"
custom_model = AutoModelForSequenceClassification.from_pretrained(model_path)
custom_tokenizer = AutoTokenizer.from_pretrained(model_path)

# Groq API Key (Set this as an environment variable for security)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Alternatively, hardcode for testing
client = Groq(api_key=GROQ_API_KEY)

# Initialize FastAPI app
app = FastAPI()


# Define request model
class SentimentRequest(BaseModel):
    text: str
    model: str  # Accepts "custom" or "llama"


@app.post("/analyze/")
def analyze_sentiment(request: SentimentRequest):
    """Analyze sentiment of input text using either fine-tuned IMDB model or LLaMA 3 via Groq API."""

    if request.model == "custom":
        tokenizer = custom_tokenizer
        model = custom_model
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, padding=True, max_length=256)

        with torch.no_grad():
            outputs = model(**inputs)
            scores = torch.nn.functional.softmax(outputs.logits, dim=-1)
            confidence, prediction = torch.max(scores, dim=1)

        sentiment = "positive" if prediction.item() == 1 else "negative"
        return {"sentiment": sentiment, "confidence": round(confidence.item(), 4)}

    elif request.model == "llama":
        try:
            # Define the system prompt to instruct the model to act as a translator
            system_prompt = (
                "You are a highly accurate AI model specializing in binary sentiment analysis of text-based reviews. "
                "You will classify the given text as either 'positive' or 'negative', with no intermediate or neutral categories. "
                "Analyze the sentiment of the following text and respond strictly in the format: "
                "{\"sentiment\":\"negative\",\"confidence\":0.9982}. "
                "Do not include any additional explanation, comments, or formatting beyond this JSON structure. "
                "The confidence score must be a float between 0 and 1, rounded to four decimal places."
            )
            # Create the chat completion request
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.text},
                ],
                model="mixtral-8x7b-32768",  # Use a suitable Groq model
                temperature=0.3,  # Lower temperature for more deterministic translations
                max_tokens=1024,  # Limit the response length
            )

            # Extract the translated text
            translated_text = chat_completion.choices[0].message.content

            return {translated_text}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    else:
        raise HTTPException(status_code=400, detail="Invalid model selection. Use 'custom' or 'llama'.")

