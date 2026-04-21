import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-improver-lora-adapter"

def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

print_header("EMAIL IMPROVER — Grammar & Clarity")
device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    print(f"Loading improver adapter from '{ADAPTER_DIR}'...")
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="improver")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_email_improver.py' first.")
    sys.exit()

model.eval()
print_header("READY  |  Paste an email with grammar or clarity issues")
print("Type 'quit' to exit.\n")

def generate(email):
    instruction = f"Fix the grammar and improve clarity: {email}"
    messages = [{"role": "user", "content": instruction}]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    input_length = inputs["input_ids"].shape[1]

    model.set_adapter("improver")
    model.to("cpu").float()
    cpu_inputs = inputs.to("cpu")

    with torch.no_grad():
        out = model.generate(
            **cpu_inputs,
            max_new_tokens=128,
            do_sample=True,
            temperature=0.7,
            repetition_penalty=1.1,
        )

    model.to(device)
    return tokenizer.decode(out[0][input_length:], skip_special_tokens=True).strip()

while True:
    user_input = input("[EMAIL]: ").strip()

    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    result = generate(user_input)

    print("\n" + "-" * 50)
    print(f"ORIGINAL : {user_input}")
    print(f"IMPROVED : {result}")
    print("-" * 50 + "\n")
