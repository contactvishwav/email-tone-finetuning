import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-instruction-lora-adapter"

# Same email, 5 different instructions — the showpiece demo
DEMO_EMAIL = "Send me the report ASAP."
DEMO_INSTRUCTIONS = [
    "Rewrite this email in a polite and confident tone",
    "Rewrite this email to sound more assertive",
    "Rewrite this email to sound friendlier",
    "Rewrite this email to be polite but firm",
    "Rewrite this email to be professional and concise",
]

device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="instruction")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_instruction_model.py' first.")
    sys.exit()

model.eval()

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


# Allow custom email + instructions from command line:
#   python compare_instructions.py "Your email here."
email = sys.argv[1] if len(sys.argv) > 1 else DEMO_EMAIL
instructions = DEMO_INSTRUCTIONS

print("\n" + "=" * 60)
print("INSTRUCTION-BASED TRANSFORMER — COMPARISON")
print("=" * 60)
print(f"EMAIL: {email}")
print("=" * 60)

for instruction in instructions:
    print(f"\n[ {instruction.upper()} ]")
    print(generate(instruction, email))
    print("-" * 60)

print("\nDone.")
