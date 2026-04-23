import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-instruction-lora-adapter"

def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

print_header("INSTRUCTION-BASED EMAIL TRANSFORMER")
device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    print(f"Loading instruction adapter from '{ADAPTER_DIR}'...")
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="instruction")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_instruction_model.py' first.")
    sys.exit()

model.eval()
print_header("READY  |  Enter an instruction and an email")
print("Type 'quit' at any prompt to exit.\n")
print("Example instructions:")
print("  - Rewrite this email in a polite and confident tone")
print("  - Make this email more assertive")
print("  - Fix the grammar errors in this email")
print("  - Make this email more concise without losing the key message")
print("  - Rewrite this email to be polite but firm\n")

def generate(instruction, email):
    prompt = f"Instruction: {instruction}\nEmail: {email}"
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    input_length = inputs["input_ids"].shape[1]

    model.set_adapter("instruction")
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
    instruction = input("[INSTRUCTION]: ").strip()

    if instruction.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not instruction:
        continue

    email = input("[EMAIL]: ").strip()

    if email.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not email:
        continue

    result = generate(instruction, email)

    print("\n" + "-" * 50)
    print(f"INSTRUCTION : {instruction}")
    print(f"ORIGINAL    : {email}")
    print(f"RESULT      : {result}")
    print("-" * 50 + "\n")
