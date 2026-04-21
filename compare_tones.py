import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-tone-lora-adapter"
TONES = ["friendly", "assertive", "apologetic", "persuasive"]

DEMO_EMAIL = "You missed the deadline again and didn't bother to tell anyone."

device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="tone")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_tone_transformer.py' first.")
    sys.exit()

model.eval()

def generate(prompt_text):
    messages = [{"role": "user", "content": prompt_text}]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    input_length = inputs["input_ids"].shape[1]

    model.set_adapter("tone")
    model.to("cpu").float()
    cpu_inputs = inputs.to("cpu")

    with torch.no_grad():
        out = model.generate(
            **cpu_inputs,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.7,
            repetition_penalty=1.1,
        )

    model.to(device)
    return tokenizer.decode(out[0][input_length:], skip_special_tokens=True).strip()


# Allow overriding the demo email from the command line:
#   python compare_tones.py "Your custom blunt email here."
email = sys.argv[1] if len(sys.argv) > 1 else DEMO_EMAIL

print("\n" + "=" * 60)
print("TONE TRANSFORMER — SIDE-BY-SIDE COMPARISON")
print("=" * 60)
print(f"ORIGINAL: {email}")
print("=" * 60)

for tone in TONES:
    instruction = f"Rewrite in a {tone} tone: {email}"
    print(f"\n[ {tone.upper()} ]")
    print(generate(instruction))
    print("-" * 60)

print("\nDone.")
