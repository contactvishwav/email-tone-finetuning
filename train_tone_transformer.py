import torch
from datasets import load_dataset
from trl import SFTTrainer, SFTConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model

MODEL_ID = "google/gemma-3-270m-it"
ADAPTER_PATH = "gemma3-270m-tone-lora-adapter"
device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32).to(device)

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

ds = load_dataset("json", data_files="tone_emails.jsonl", split="train")

def format_prompts(ex):
    messages = [
        {"role": "user",      "content": ex["instruction"]},
        {"role": "assistant", "content": ex["output"]},
    ]
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)}

ds = ds.map(format_prompts)
# Stratified-style split: shuffle with fixed seed so all 4 tones appear in both splits
ds = ds.shuffle(seed=42).train_test_split(test_size=0.1, seed=42)
train_ds, eval_ds = ds["train"], ds["test"]

print(f"Train examples: {len(train_ds)}  |  Eval examples: {len(eval_ds)}")

args = SFTConfig(
    output_dir="gemma3-270m-tone-lora",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,   # effective batch size = 8
    dataloader_pin_memory=False,      # required for MPS stability
    learning_rate=5e-5,
    num_train_epochs=20,              # more epochs: 80 examples vs 45 in original
    weight_decay=0.01,
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,                 # gentle warmup helps with multi-class conditioning
    logging_steps=1,
    eval_strategy="steps",
    eval_steps=10,
    save_steps=50,
    save_total_limit=1,
    report_to="none",
    max_length=512,
    dataset_text_field="text",
)

trainer = SFTTrainer(
    model=model,
    processing_class=tokenizer,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    args=args,
)

print(f"Starting Tone Transformer training on {device.upper()}...")
trainer.train()
trainer.model.save_pretrained(ADAPTER_PATH)
tokenizer.save_pretrained(ADAPTER_PATH)
print(f"Training complete. Adapter saved to {ADAPTER_PATH}")
