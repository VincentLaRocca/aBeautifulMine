"""
Checkpoint Saver
Save pipeline state periodically for better resume capability
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def save_checkpoint(orchestrator_state: dict, output_dir: Path):
    """Save a checkpoint of the current pipeline state"""
    checkpoint_dir = output_dir / "checkpoints"
    checkpoint_dir.mkdir(exist_ok=True)
    
    checkpoint_file = checkpoint_dir / f"checkpoint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    checkpoint_data = {
        "timestamp": datetime.now().isoformat(),
        "state": orchestrator_state,
        "topic": orchestrator_state.get("topic"),
        "subtopics": orchestrator_state.get("subtopics", []),
        "current_subtopic_index": orchestrator_state.get("current_subtopic_index", 0),
        "qa_pairs_count": len(orchestrator_state.get("qa_pairs", []))
    }
    
    with open(checkpoint_file, 'w', encoding='utf-8') as f:
        json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    # Keep only the latest checkpoint
    checkpoints = sorted(checkpoint_dir.glob("checkpoint_*.json"), key=lambda p: p.stat().st_mtime)
    if len(checkpoints) > 5:  # Keep last 5 checkpoints
        for old_checkpoint in checkpoints[:-5]:
            old_checkpoint.unlink()
    
    return checkpoint_file

def load_latest_checkpoint(output_dir: Path):
    """Load the most recent checkpoint"""
    checkpoint_dir = output_dir / "checkpoints"
    if not checkpoint_dir.exists():
        return None
    
    checkpoints = list(checkpoint_dir.glob("checkpoint_*.json"))
    if not checkpoints:
        return None
    
    latest = max(checkpoints, key=lambda p: p.stat().st_mtime)
    
    with open(latest, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    print("Checkpoint utilities for multi-agent pipeline")
    print("This module is used by the orchestrator internally")

