"""
Model Training Script
Fine-tune models using extracted training data
Supports multiple training frameworks and models
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, Any, Literal
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class ModelTrainer:
    """
    Trains/fine-tunes models using extracted training data
    Supports Llama, Mixtral, and other models via different frameworks
    """

    def __init__(self,
                 model_path: Optional[str] = None,
                 output_dir: str = "trained_models",
                 framework: Literal["unsloth", "axolotl", "transformers"] = "unsloth"):
        """
        Initialize the trainer

        Args:
            model_path: Path to base model or model identifier
            output_dir: Directory to save trained models
            framework: Training framework to use
        """
        self.model_path = model_path or os.getenv("MODEL_PATH", "models/Mixtral-8x7B-Instruct-v0.1.Q4_K_M.gguf")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.framework = framework

        print(f"[TRAINER] Initializing with framework: {framework}")
        print(f"[TRAINER] Base model: {self.model_path}")
        print(f"[TRAINER] Output directory: {self.output_dir}")

    def prepare_unsloth_training(self,
                                  training_data_path: str,
                                  model_name: str = "unsloth/mistral-7b-v0.3",
                                  max_seq_length: int = 2048,
                                  learning_rate: float = 2e-4,
                                  num_epochs: int = 3,
                                  batch_size: int = 2,
                                  gradient_accumulation_steps: int = 4) -> str:
        """
        Prepare Unsloth training configuration

        Args:
            training_data_path: Path to training data (JSONL)
            model_name: HuggingFace model identifier
            max_seq_length: Maximum sequence length
            learning_rate: Learning rate
            num_epochs: Number of training epochs
            batch_size: Batch size per device
            gradient_accumulation_steps: Gradient accumulation steps

        Returns:
            Path to generated training script
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_name = f"train_unsloth_{timestamp}.py"
        script_path = self.output_dir / script_name

        training_script = f'''"""
Unsloth Training Script
Auto-generated: {datetime.now().isoformat()}
"""

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import torch

# Configuration
max_seq_length = {max_seq_length}
model_name = "{model_name}"
dtype = None  # Auto-detect
load_in_4bit = True  # Use 4-bit quantization

# Load model and tokenizer
print("[LOADING] Model and tokenizer...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=load_in_4bit,
)

# Add LoRA adapters
print("[SETUP] Adding LoRA adapters...")
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=3407,
    use_rslora=False,
    loftq_config=None,
)

# Load dataset
print("[LOADING] Training data...")
dataset = load_dataset("json", data_files="{training_data_path}", split="train")

print(f"[INFO] Dataset size: {{len(dataset)}} examples")

# Format function for OpenAI format
def formatting_prompts_func(examples):
    texts = []
    for messages in examples["messages"]:
        # Convert messages to prompt format
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
        texts.append(text)
    return {{"text": texts}}

# Apply formatting
dataset = dataset.map(formatting_prompts_func, batched=True)

# Training arguments
print("[SETUP] Training arguments...")
training_args = TrainingArguments(
    output_dir="{self.output_dir / 'checkpoints'}",
    per_device_train_batch_size={batch_size},
    gradient_accumulation_steps={gradient_accumulation_steps},
    warmup_steps=5,
    num_train_epochs={num_epochs},
    learning_rate={learning_rate},
    fp16=not torch.cuda.is_bf16_supported(),
    bf16=torch.cuda.is_bf16_supported(),
    logging_steps=1,
    optim="adamw_8bit",
    weight_decay=0.01,
    lr_scheduler_type="linear",
    seed=3407,
    save_strategy="epoch",
    save_total_limit=2,
    report_to="none",  # Change to "tensorboard" or "wandb" if desired
)

# Initialize trainer
print("[SETUP] Initializing trainer...")
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=max_seq_length,
    dataset_num_proc=2,
    packing=False,
    args=training_args,
)

# Train
print("[TRAINING] Starting training...")
print("="*80)
trainer_stats = trainer.train()

# Save model
print("\\n[SAVING] Saving trained model...")
model.save_pretrained("{self.output_dir / 'final_model'}")
tokenizer.save_pretrained("{self.output_dir / 'final_model'}")

# Save in GGUF format for llama.cpp
print("[SAVING] Saving in GGUF format...")
model.save_pretrained_gguf(
    "{self.output_dir / 'final_model_gguf'}",
    tokenizer,
    quantization_method="q4_k_m"
)

print("="*80)
print("[COMPLETE] Training finished!")
print(f"Model saved to: {self.output_dir / 'final_model'}")
print(f"GGUF model saved to: {self.output_dir / 'final_model_gguf'}")
'''

        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(training_script)

        print(f"[CREATED] Training script: {script_path}")
        return str(script_path)

    def prepare_axolotl_config(self,
                               training_data_path: str,
                               base_model: str = "mistralai/Mistral-7B-Instruct-v0.3",
                               num_epochs: int = 3,
                               learning_rate: float = 2e-4) -> str:
        """
        Prepare Axolotl configuration file

        Args:
            training_data_path: Path to training data (JSONL)
            base_model: HuggingFace model identifier
            num_epochs: Number of training epochs
            learning_rate: Learning rate

        Returns:
            Path to generated config file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        config_name = f"axolotl_config_{timestamp}.yml"
        config_path = self.output_dir / config_name

        config = f'''# Axolotl Configuration
# Auto-generated: {datetime.now().isoformat()}

base_model: {base_model}
model_type: MistralForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: {training_data_path}
    type: chat_template
    chat_template: chatml
    field_messages: messages
    message_field_role: role
    message_field_content: content

dataset_prepared_path:
val_set_size: 0.05
output_dir: {self.output_dir / 'axolotl_output'}

sequence_len: 2048
sample_packing: false

adapter: lora
lora_r: 16
lora_alpha: 16
lora_dropout: 0.05
lora_target_linear: true

wandb_project:
wandb_entity:
wandb_watch:
wandb_name:
wandb_log_model:

gradient_accumulation_steps: 4
micro_batch_size: 2
num_epochs: {num_epochs}
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: {learning_rate}

train_on_inputs: false
group_by_length: false
bf16: auto
fp16:
tf32: false

gradient_checkpointing: true
early_stopping_patience:
resume_from_checkpoint:
local_rank:
logging_steps: 1
xformers_attention:
flash_attention: true

warmup_steps: 10
evals_per_epoch: 4
eval_table_size:
saves_per_epoch: 1
debug:
deepspeed:
weight_decay: 0.01
fsdp:
fsdp_config:
special_tokens:
  pad_token: <|end_of_text|>
'''

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(config)

        print(f"[CREATED] Axolotl config: {config_path}")
        print(f"\nTo train with Axolotl, run:")
        print(f"  accelerate launch -m axolotl.cli.train {config_path}")

        return str(config_path)

    def create_quick_start_guide(self, training_data_path: str) -> str:
        """
        Create a quick start guide for training

        Args:
            training_data_path: Path to training data

        Returns:
            Path to guide file
        """
        guide_path = self.output_dir / "TRAINING_QUICKSTART.md"

        guide_content = f'''# Training Quick Start Guide

Generated: {datetime.now().isoformat()}

## Training Data
- **Location:** `{training_data_path}`
- **Format:** JSONL with OpenAI messages format

---

## Option 1: Unsloth (Recommended - Fastest)

**Why Unsloth?**
- 2x faster than standard fine-tuning
- Uses less VRAM
- Built-in GGUF export for llama.cpp
- Optimized for consumer GPUs

**Setup:**
```bash
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

**Train:**
```bash
python {self.output_dir}/train_unsloth_*.py
```

**Expected Time:**
- RTX 5090: ~2-4 hours for 1000 Q&A pairs (3 epochs)
- VRAM Usage: ~20-25GB

---

## Option 2: Axolotl (Advanced)

**Why Axolotl?**
- More configuration options
- Better for complex training setups
- Supports multiple model architectures

**Setup:**
```bash
pip install axolotl
```

**Train:**
```bash
accelerate launch -m axolotl.cli.train {self.output_dir}/axolotl_config_*.yml
```

---

## Option 3: Standard Transformers

**Setup:**
```bash
pip install transformers datasets peft bitsandbytes trl
```

**Train:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from trl import SFTTrainer
from datasets import load_dataset
from peft import LoraConfig

# Load model
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3",
    load_in_4bit=True,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

# LoRA config
peft_config = LoraConfig(
    r=16,
    lora_alpha=16,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
    task_type="CAUSAL_LM"
)

# Load dataset
dataset = load_dataset("json", data_files="{training_data_path}", split="train")

# Training args
training_args = TrainingArguments(
    output_dir="{self.output_dir}/output",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    learning_rate=2e-4,
    save_strategy="epoch"
)

# Train
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    args=training_args,
    tokenizer=tokenizer
)

trainer.train()
model.save_pretrained("{self.output_dir}/final_model")
```

---

## Post-Training: Using Your Model

### With llama.cpp (if using Unsloth GGUF):
```bash
./llama-server -m {self.output_dir}/final_model_gguf/model-q4_k_m.gguf --n-gpu-layers 33 -c 4096
```

### With Transformers:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("{self.output_dir}/final_model")
tokenizer = AutoTokenizer.from_pretrained("{self.output_dir}/final_model")

# Use for inference
messages = [
    {{"role": "user", "content": "What is a bull flag pattern?"}}
]
inputs = tokenizer.apply_chat_template(messages, return_tensors="pt")
outputs = model.generate(inputs, max_new_tokens=500)
response = tokenizer.decode(outputs[0])
print(response)
```

---

## Training Tips

1. **Start Small:** Try 1 epoch first to verify everything works
2. **Monitor VRAM:** Use `nvidia-smi` to watch GPU memory
3. **Adjust Batch Size:** If OOM, reduce `batch_size` to 1
4. **Learning Rate:** 2e-4 is a good starting point for LoRA
5. **Epochs:** 3-5 epochs typically sufficient for Q&A data

---

## Troubleshooting

**Out of Memory:**
- Reduce batch_size to 1
- Reduce max_seq_length to 1024
- Enable gradient checkpointing
- Use 4-bit quantization

**Slow Training:**
- Use Unsloth instead of standard training
- Enable flash_attention
- Increase batch_size if VRAM allows
- Use gradient_accumulation_steps

**Model Not Learning:**
- Increase learning rate to 3e-4 or 5e-4
- Train for more epochs
- Check data formatting is correct
- Verify tokenizer is properly configured

---

## Expected Results

After training on your Q&A dataset, the model should:
- ✅ Answer crypto/trading questions with expert-level detail
- ✅ Maintain consistent style and structure from training data
- ✅ Provide 3000+ character comprehensive answers
- ✅ Demonstrate knowledge from your curated dataset

---

For more help, see:
- Unsloth: https://github.com/unslothai/unsloth
- Axolotl: https://github.com/OpenAccess-AI-Collective/axolotl
- Transformers: https://huggingface.co/docs/transformers
'''

        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide_content)

        print(f"[CREATED] Training guide: {guide_path}")
        return str(guide_path)


def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python train_model.py <training_data_path> [options]")
        print()
        print("Options:")
        print("  --framework unsloth|axolotl|transformers  Training framework (default: unsloth)")
        print("  --model MODEL_NAME                        HuggingFace model identifier")
        print("  --epochs N                                Number of epochs (default: 3)")
        print("  --lr RATE                                 Learning rate (default: 2e-4)")
        print("  --output DIR                              Output directory (default: trained_models)")
        print()
        print("Examples:")
        print("  python train_model.py training_data/train_openai_*.jsonl")
        print("  python train_model.py data.jsonl --framework unsloth --epochs 5")
        sys.exit(1)

    training_data = sys.argv[1]

    if not Path(training_data).exists():
        print(f"[ERROR] Training data not found: {training_data}")
        sys.exit(1)

    # Parse options
    framework = "unsloth"
    model_name = "unsloth/mistral-7b-v0.3"
    epochs = 3
    lr = 2e-4
    output_dir = "trained_models"

    for i, arg in enumerate(sys.argv):
        if arg == "--framework" and i + 1 < len(sys.argv):
            framework = sys.argv[i + 1]
        elif arg == "--model" and i + 1 < len(sys.argv):
            model_name = sys.argv[i + 1]
        elif arg == "--epochs" and i + 1 < len(sys.argv):
            epochs = int(sys.argv[i + 1])
        elif arg == "--lr" and i + 1 < len(sys.argv):
            lr = float(sys.argv[i + 1])
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    # Initialize trainer
    trainer = ModelTrainer(output_dir=output_dir, framework=framework)

    print("\n" + "="*80)
    print("TRAINING SETUP")
    print("="*80)
    print(f"Training data: {training_data}")
    print(f"Framework: {framework}")
    print(f"Base model: {model_name}")
    print(f"Epochs: {epochs}")
    print(f"Learning rate: {lr}")
    print(f"Output: {output_dir}")
    print("="*80)

    # Prepare training
    if framework == "unsloth":
        script_path = trainer.prepare_unsloth_training(
            training_data_path=training_data,
            model_name=model_name,
            num_epochs=epochs,
            learning_rate=lr
        )
        print(f"\n[NEXT] Run the training script:")
        print(f"  python {script_path}")

    elif framework == "axolotl":
        config_path = trainer.prepare_axolotl_config(
            training_data_path=training_data,
            base_model=model_name,
            num_epochs=epochs,
            learning_rate=lr
        )
        print(f"\n[NEXT] Run Axolotl training:")
        print(f"  accelerate launch -m axolotl.cli.train {config_path}")

    # Create guide
    guide_path = trainer.create_quick_start_guide(training_data)

    print("\n" + "="*80)
    print("SETUP COMPLETE")
    print("="*80)
    print(f"📚 Quick Start Guide: {guide_path}")
    print("\nReady to train! See the guide for detailed instructions.")


if __name__ == "__main__":
    main()
