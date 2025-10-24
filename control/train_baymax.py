from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments

# 1️⃣ Load dataset
dataset = load_dataset("json", data_files="C:/Users/Shreyansh Singh/Desktop/Baymax/baymax/engine/baymax_dataset.jsonl")

# 2️⃣ Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

# 3️⃣ Combine prompt and response for training
def tokenize_function(examples):
    texts = [p + r for p, r in zip(examples["prompt"], examples["response"])]
    tokens = tokenizer(texts, truncation=True, padding="max_length", max_length=128)
    tokens["labels"] = tokens["input_ids"].copy()  # ✅ Trainer needs this for loss calculation
    return tokens

# 4️⃣ Tokenize dataset
tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 5️⃣ Load base model
model = AutoModelForCausalLM.from_pretrained("gpt2")

# 6️⃣ Training arguments
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results",
    # evaluation_strategy="epoch",   # ✅ correct spelling
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)


# 7️⃣ Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
)

# 8️⃣ Train the model
trainer.train()

# 9️⃣ Save the fine-tuned model
model.save_pretrained("./baymax_finetuned")
tokenizer.save_pretrained("./baymax_finetuned")

print("✅ Fine-tuning complete! Model saved in ./baymax_finetuned")
