from transformers import AutoModelForCausalLM, AutoTokenizer

# Use an existing small model for now
model_path = "microsoft/DialoGPT-small"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path)

def get_baymax_reply(user_input):
    prompt = f"User: {user_input}\nBaymax:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=60)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.split("Baymax:")[-1].strip()
