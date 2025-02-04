from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Define model repository URL
model_name = "santerihukari/fine-tuned-imdb-model"

# Download and save the model locally
local_model_path = "./fine_tuned_model"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save the downloaded model
model.save_pretrained(local_model_path)
tokenizer.save_pretrained(local_model_path)

print(f"Model downloaded and saved at {local_model_path}")