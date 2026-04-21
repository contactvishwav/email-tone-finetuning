# Email Tone Fine-Tuning with LoRA

Fine-tuning **Gemma 3 270M** using **LoRA (Low-Rank Adaptation)** to rewrite workplace emails in different tones. Built as a progression from a baseline tutorial to an original multi-tone conditioning model.

---

## What This Project Does

Takes blunt or unprofessional workplace emails and rewrites them in a chosen tone:

```
INPUT:  "You missed the deadline again and didn't bother to tell anyone."

FRIENDLY   → Hey! I noticed the deadline passed and we haven't received your
             submission yet. No worries — these things happen! Could you let me
             know when you think you'll be able to get it over to us?

ASSERTIVE  → The deadline passed without your submission. I need this delivered
             by end of day today. Please confirm you can meet this revised deadline.

APOLOGETIC → I'm sorry to bother you about this, but I noticed the deadline may
             have passed. I completely understand if you've been swamped — I
             apologize if my original timeline wasn't communicated clearly.

PERSUASIVE → I wanted to flag that the deadline has passed on this deliverable.
             Meeting these timelines matters because it affects the whole team's
             planning — if we can get this wrapped up today, we stay on track for
             the next milestone.
```

---

## Project Structure

```
├── datasets/
│   ├── generate_emails_dataset.py   # Generates baseline email pairs
│   ├── generate_tone_dataset.py     # Generates 4-tone dataset (80 examples)
│   ├── emails.jsonl                 # Baseline training data
│   └── tone_emails.jsonl            # Tone transformer training data
│
├── Part 1 — Email Rewriter (Baseline + Improved)
│   ├── interactive_train.py         # Intentional failure demo (model collapse)
│   ├── interactive_train_improved.py
│   ├── train_email_tone_rewriter_improved.py
│   ├── interactive_test_improved.py
│   ├── compare_models.py            # Base vs Instruct vs Fine-tuned
│   └── compare_all_models.py        # 4-way comparison including poor LoRA
│
└── Part 2 — Tone Transformer (Original Extension)
    ├── train_tone_transformer.py
    ├── interactive_test_tone.py     # Interactive demo with tone selection
    └── compare_tones.py             # Side-by-side all 4 tones
```

---

## The Story Behind It

This project has three acts:

**Act 1 — Baseline**: Fine-tune Gemma 3 to rewrite blunt emails professionally using LoRA. The first attempt (`interactive_train.py`) deliberately uses a high learning rate and too few epochs to demonstrate **model collapse** — where the model produces repetitive, broken output. This is an intentional lesson.

**Act 2 — Fix It**: Identify what went wrong (learning rate too high, insufficient epochs, no cosine scheduling) and produce a stable fine-tuned model. Also diagnoses and fixes MPS-specific crashes on Apple Silicon related to a 4GB per-NDArray hard limit in Metal Performance Shaders.

**Act 3 — Extend It**: Design a custom multi-tone dataset from scratch (20 blunt emails × 4 tones = 80 training examples), train a model that conditions on the tone instruction, and build an interactive demo. This is the original contribution — the model learns that the same blunt message should produce structurally different rewrites depending on the tone word in the prompt.

---

## Setup

### Requirements
- Python 3.11+
- Apple Silicon Mac (MPS), NVIDIA GPU (CUDA), or CPU
- Hugging Face account with access to [Gemma 3 270M](https://huggingface.co/google/gemma-3-270m-it)

### Install

```bash
git clone https://github.com/contactvishwav/email-tone-finetuning.git
cd email-tone-finetuning
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Hugging Face Login
Gemma 3 is a gated model. Accept the license on Hugging Face, then:
```bash
huggingface-cli login
```

---

## Running the Project

### Part 1 — Email Rewriter

**Generate the dataset:**
```bash
python generate_emails_dataset.py
```

**See model collapse in action (intentional failure):**
```bash
python interactive_train.py
```

**Train the improved model:**
```bash
python interactive_train_improved.py
```

**Compare base vs instruct vs fine-tuned:**
```bash
python compare_models.py
```

**Full 4-way comparison (base, instruct, poor LoRA, improved LoRA):**
```bash
python compare_all_models.py
```

---

### Part 2 — Tone Transformer

**Generate the tone dataset:**
```bash
python generate_tone_dataset.py
```

**Train the tone transformer:**
```bash
python train_tone_transformer.py
```

**Interactive demo — pick a tone for any blunt email:**
```bash
python interactive_test_tone.py
```

**Side-by-side all 4 tones (default email):**
```bash
python compare_tones.py
```

**Side-by-side all 4 tones (custom email):**
```bash
python compare_tones.py "Your code broke the build and the client is furious."
```

---

## Key Technical Decisions

**Why LoRA?** Training all 270M parameters is expensive. LoRA freezes the base model and trains only small low-rank adapter matrices (~15MB), which is fast and memory-efficient without sacrificing task-specific quality.

**Why does the first training fail?** `interactive_train.py` uses `lr=2e-4` (too high) and `epochs=3` (too few). The high learning rate causes the model to overfit aggressively to specific token patterns rather than learning the underlying task. The improved version uses `lr=5e-5`, 15 epochs, and a cosine scheduler.

**MPS fix**: Apple's Metal Performance Shaders backend has a hard 4GB limit per NDArray. `torch.multinomial` (used during sampling with `do_sample=True`) exceeds this with Gemma's 256,000-token vocabulary. Solution: run sampling inference on CPU with float32, use greedy decoding (`do_sample=False`) on MPS where possible.

**Tone conditioning**: The model learns to condition output style on the tone word in the instruction prefix (`"Rewrite in a {tone} tone: ..."`). Each blunt email in the dataset has 4 distinct rewrites, so the model sees the same input mapped to 4 structurally different outputs and learns that the tone word is the discriminating signal.

---

## Limitations

- **270M parameters is small.** The model generalizes well to inputs similar to its training distribution (workplace behavior feedback, deadlines, code quality). It degrades on inputs far from that distribution because a small model can't generalize as broadly.
- **80 training examples** is enough to learn tone patterns but not enough for robust semantic preservation across all input types. A larger dataset or a larger base model would improve meaning retention.
- **Subject confusion** occasionally occurs on direct personal criticisms — the model sometimes flips who is speaking. This is a known failure mode for small models on out-of-distribution inputs.

---

## Hardware

Tested on Apple M2 with 8GB unified memory. Training takes approximately 5–10 minutes per model on MPS. CPU training is supported but significantly slower.

---

## Tech Stack

- [Gemma 3 270M Instruct](https://huggingface.co/google/gemma-3-270m-it) — base model
- [PEFT](https://github.com/huggingface/peft) — LoRA implementation
- [TRL](https://github.com/huggingface/trl) — SFTTrainer
- [Transformers](https://github.com/huggingface/transformers) — model loading and inference
- PyTorch with MPS/CUDA/CPU backend
