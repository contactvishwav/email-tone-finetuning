import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import sys

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_DIR = "gemma3-270m-tone-lora-adapter"
TONES = ["friendly", "assertive", "apologetic", "persuasive"]

def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def pick_tone():
    """Show the tone menu and return the selected tone string, or None to quit."""
    print("\nSelect a tone:")
    for i, tone in enumerate(TONES, 1):
        print(f"  {i}) {tone.capitalize()}")
    print("  q) Quit")

    choice = input("Choice (1-4 or q): ").strip().lower()
    if choice in ["q", "quit", "exit"]:
        return None
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        return pick_tone()
    return TONES[int(choice) - 1]

def generate(email, tone):
    instruction = f"Rewrite in a {tone} tone: {email}"
    messages = [{"role": "user", "content": instruction}]

    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(device)
    input_length = inputs["input_ids"].shape[1]

    print(f"\nGenerating {tone} rewrite...")
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


print_header("TONE TRANSFORMER — Powered by LoRA")
device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

print(f"Loading model to {device.upper()}...")
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

try:
    print(f"Loading tone adapter from '{ADAPTER_DIR}'...")
    model = PeftModel.from_pretrained(model, ADAPTER_DIR, adapter_name="tone")
except Exception:
    print(f"\nERROR: Could not find adapter folder '{ADAPTER_DIR}'.")
    print("Please run 'python train_tone_transformer.py' first.")
    sys.exit()

model.eval()
print_header("READY  |  Type a blunt email and choose a tone")
print("Type 'quit' at any prompt to exit.\n")

while True:
    user_input = input("[BLUNT EMAIL]: ").strip()

    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    # Inner loop: keep trying tones on the same email until user says no
    while True:
        selected_tone = pick_tone()

        if selected_tone is None:
            print("Goodbye!")
            sys.exit()

        result = generate(user_input, selected_tone)

        print("\n" + "-" * 50)
        print(f"ORIGINAL  : {user_input}")
        print(f"TONE      : {selected_tone.capitalize()}")
        print(f"REWRITTEN : {result}")
        print("-" * 50)

        again = input("\nTry another tone with the same email? (y/n): ").strip().lower()
        if again not in ["y", "yes"]:
            break  # back to [BLUNT EMAIL] prompt
