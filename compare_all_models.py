import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import gc

# Configuration
BASE_MODEL_ID = "google/gemma-3-270m"
INSTRUCT_MODEL_ID = "google/gemma-3-270m-it"
POOR_ADAPTER = "gemma3-270m-email-lora-adapter"
IMPROVED_ADAPTER = "gemma3-270m-email-lora-adapter-improved"

prompt = "Rewrite professionally: This code is garbage and broke the build."
# Choose device (MPS > CUDA > CPU)
device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
# Use half‑precision when possible to reduce memory pressure
dtype = torch.float16 if device != "cpu" else torch.float32

def generate_text(model, tokenizer, is_base=False, improved=False):
    """Generate a response for the global *prompt*.
    *is_base* – use the simple "Request/Response" format for the base model.
    *improved* – enable sampling/temperature for the improved LoRA.
    """
    if is_base:
        inputs = tokenizer(f"Request: {prompt}\nResponse:", return_tensors="pt").to(device).to(dtype)
    else:
        messages = [{"role": "user", "content": prompt}]
        inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(device).to(dtype)

    gen_kwargs = {
        "max_new_tokens": 64,
        "do_sample": True if improved else False,
        "temperature": 0.7 if improved else 1.0,
        "repetition_penalty": 1.1 if improved else 1.0,
    }
    with torch.no_grad():
        out = model.generate(**inputs, **gen_kwargs)
    input_len = inputs["input_ids"].shape[1]
    return tokenizer.decode(out[0][input_len:], skip_special_tokens=True).strip()

def main():
    print(f"🚀 ULTIMATE COMPARISON DEMO (Device: {device.upper()})")
    outputs = {}

    # 1️⃣ Base model (load in half‑precision when possible)
    print("\n--- 1. BASE MODEL ---")
    tokenizer_base = AutoTokenizer.from_pretrained(BASE_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(BASE_MODEL_ID, torch_dtype=dtype).to(device)
    outputs["Base"] = generate_text(model, tokenizer_base, is_base=True)
    del model
    gc.collect()

    # 2️⃣ Instruct model
    print("\n--- 2. INSTRUCT MODEL ---")
    tokenizer_it = AutoTokenizer.from_pretrained(INSTRUCT_MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(INSTRUCT_MODEL_ID, torch_dtype=dtype).to(device)
    outputs["Instruct"] = generate_text(model, tokenizer_it)
    del model
    gc.collect()

    # 3️⃣ Poor LoRA (high LR, low epochs)
    print("\n--- 3. POOR LORA (High LR, Low Epochs) ---")
    try:
        model = AutoModelForCausalLM.from_pretrained(INSTRUCT_MODEL_ID, torch_dtype=dtype).to(device)
        model = PeftModel.from_pretrained(model, POOR_ADAPTER, adapter_name="poor")
        outputs["Poor LoRA"] = generate_text(model, tokenizer_it)
    except Exception as e:
        outputs["Poor LoRA"] = f"(Adapter load failed: {e})"
    finally:
        del model
        gc.collect()

    # 4️⃣ Improved LoRA (stable LR, high epochs)
    print("\n--- 4. IMPROVED LORA (Stable LR, High Epochs) ---")
    try:
        model = AutoModelForCausalLM.from_pretrained(INSTRUCT_MODEL_ID, torch_dtype=dtype).to(device)
        model.load_adapter(IMPROVED_ADAPTER, adapter_name="improved")
        model.set_adapter("improved")
        outputs["Improved LoRA"] = generate_text(model, tokenizer_it, improved=True)
    except Exception as e:
        outputs["Improved LoRA"] = f"(Adapter load failed: {e})"
    finally:
        del model
        gc.collect()

    # 🎉 Scoreboard
    print("\n" + "=" * 80)
    print("🏁 FINAL SCOREBOARD")
    print("=" * 80)
    print(f"PROMPT: {prompt}\n")
    for name, txt in outputs.items():
        print(f"[ {name} ]\n{txt}\n")
    print("=" * 80)

if __name__ == "__main__":
    main()
