"""
Update Answer Prompt Script
Easily switch between current and enhanced prompts
"""

import json
import sys
from pathlib import Path

def update_config_file(prompt_text: str):
    """Update config.json with new prompt"""
    config_path = Path("multi_agent_system/config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    config["answer_prompt"] = prompt_text
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Updated {config_path}")

def get_enhanced_prompt() -> str:
    """Load enhanced prompt from file"""
    prompt_path = Path("multi_agent_system/enhanced_answer_prompt.txt")
    
    if not prompt_path.exists():
        print(f"[ERROR] Enhanced prompt file not found: {prompt_path}")
        return None
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def get_current_prompt() -> str:
    """Get current prompt from config"""
    config_path = Path("multi_agent_system/config.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config.get("answer_prompt", "")

def main():
    print("="*80)
    print("ANSWER PROMPT UPDATER")
    print("="*80)
    print()
    
    if len(sys.argv) < 2:
        print("Usage: python update_answer_prompt.py [enhanced|current|show]")
        print()
        print("Options:")
        print("  enhanced  - Update to enhanced prompt (recommended)")
        print("  current   - Keep current prompt")
        print("  show      - Show current prompt")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "enhanced":
        print("[UPDATING] Switching to enhanced prompt...")
        prompt = get_enhanced_prompt()
        if prompt:
            update_config_file(prompt)
            print()
            print("[SUCCESS] Enhanced prompt is now active!")
            print()
            print("The enhanced prompt includes:")
            print("  ✅ Training-specific optimizations")
            print("  ✅ Detailed structure guidance")
            print("  ✅ Quality checklist")
            print("  ✅ Self-contained answer requirements")
            print("  ✅ Enhanced educational value")
        else:
            sys.exit(1)
    
    elif command == "current":
        print("[INFO] Keeping current prompt")
        print("[INFO] No changes made")
    
    elif command == "show":
        print("[CURRENT PROMPT]")
        print("="*80)
        prompt = get_current_prompt()
        print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        print("="*80)
        print(f"\nLength: {len(prompt)} characters")
    
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Use: enhanced, current, or show")
        sys.exit(1)

if __name__ == "__main__":
    main()

