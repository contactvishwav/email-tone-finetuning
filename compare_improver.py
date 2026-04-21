import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-improver-lora-adapter"

DEMO_EMAILS = [
    "The team are struggling to meet the deadline and we needs your help.",
    "I have spoke with the vendor this morning and they have said that they can have the fix ready by Wednesday which is earlier than we expected and we should let the client know about this update as soon as possible.",
    "Between you and I, the same identical issue has occurred before in the past and nothing was done about it.",
    "Hope all is well! Wanted to touch base about couple of things, first I like to say the documentation is great, but main issue is that the API endpoint is returning incorrect data.",
]

device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="improver")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_email_improver.py' first.")
    sys.exit()

model.eval()

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


# Allow a single custom email from command line:
#   python compare_improver.py "Your email with errors here."
emails = [sys.argv[1]] if len(sys.argv) > 1 else DEMO_EMAILS

print("\n" + "=" * 60)
print("EMAIL IMPROVER — BEFORE / AFTER COMPARISON")
print("=" * 60)

for i, email in enumerate(emails, 1):
    print(f"\n[Example {i}]")
    print(f"BEFORE: {email}")
    print(f"AFTER : {generate(email)}")
    print("-" * 60)

print("\nDone.")
