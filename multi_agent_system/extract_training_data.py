"""
Training Data Extraction Tool
Extracts Q&A pairs from ChromaDB and formats for training
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Literal
from datetime import datetime
from dotenv import load_dotenv

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

load_dotenv()


class TrainingDataExtractor:
    """
    Extracts Q&A pairs from ChromaDB and formats for training
    Supports multiple output formats for different training frameworks
    """

    def __init__(self, db_path: Optional[str] = None, collection_name: str = "qa_dataset"):
        """
        Initialize the extractor

        Args:
            db_path: Path to ChromaDB directory
            collection_name: Name of the collection
        """
        if not CHROMADB_AVAILABLE:
            raise ImportError("chromadb is not installed. Install with: pip install chromadb")

        self.db_path = db_path or os.getenv("CHROMADB_PATH", "chroma_db")
        self.collection_name = collection_name

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.db_path),
            settings=Settings(anonymized_telemetry=False)
        )

        # Get collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"[EXTRACT] Connected to collection: {collection_name}")
            print(f"[EXTRACT] Total Q&A pairs in database: {self.collection.count()}")
        except Exception as e:
            raise ValueError(f"Collection '{collection_name}' not found: {e}")

    def extract_all(self,
                    output_format: Literal["openai", "alpaca", "sharegpt", "jsonl", "raw"] = "openai",
                    output_dir: str = "training_data",
                    filter_by: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Extract all Q&A pairs and save in specified format

        Args:
            output_format: Format for training data
                - "openai": OpenAI fine-tuning format (messages format)
                - "alpaca": Alpaca instruction format
                - "sharegpt": ShareGPT conversation format
                - "jsonl": Simple JSONL format (question/answer pairs)
                - "raw": Raw format with all metadata
            output_dir: Directory to save extracted data
            filter_by: Optional filters (e.g., {"topic": "Cryptocurrency"})

        Returns:
            Dictionary with extraction stats and file path
        """
        print(f"\n[EXTRACT] Starting extraction in '{output_format}' format...")

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Get all data from collection
        total_count = self.collection.count()

        # Fetch in batches to handle large datasets
        batch_size = 1000
        all_data = []

        print(f"[EXTRACT] Fetching {total_count} Q&A pairs from database...")

        for offset in range(0, total_count, batch_size):
            limit = min(batch_size, total_count - offset)

            # Query batch
            results = self.collection.get(
                limit=limit,
                offset=offset,
                include=["metadatas", "documents"]
            )

            # Process batch
            for i in range(len(results["ids"])):
                metadata = results["metadatas"][i]

                # Apply filters if specified
                if filter_by:
                    skip = False
                    for key, value in filter_by.items():
                        if metadata.get(key) != value:
                            skip = True
                            break
                    if skip:
                        continue

                # Extract question and full answer (reconstruct from document)
                document = results["documents"][i]

                # Parse question and answer from document
                if "Question: " in document and "\n\nAnswer: " in document:
                    parts = document.split("\n\nAnswer: ", 1)
                    question = parts[0].replace("Question: ", "")
                    answer = parts[1]
                else:
                    # Fallback to metadata
                    question = metadata.get("question", "")
                    answer = metadata.get("answer", "")

                all_data.append({
                    "question": question,
                    "answer": answer,
                    "topic": metadata.get("topic", ""),
                    "subtopic": metadata.get("subtopic", ""),
                    "answer_length": metadata.get("answer_length", 0),
                    "generated_at": metadata.get("generated_at", "")
                })

            print(f"  [PROGRESS] Fetched {min(offset + batch_size, total_count)}/{total_count} pairs")

        print(f"[OK] Extracted {len(all_data)} Q&A pairs")

        # Convert to requested format
        formatted_data = self._format_data(all_data, output_format)

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"training_data_{output_format}_{timestamp}.jsonl"
        output_file = output_path / filename

        # Save to file
        print(f"[SAVING] Writing to {output_file}...")

        with open(output_file, 'w', encoding='utf-8') as f:
            for item in formatted_data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

        print(f"[OK] Saved {len(formatted_data)} training examples")

        # Calculate statistics
        stats = self._calculate_stats(all_data, formatted_data)

        return {
            "success": True,
            "output_file": str(output_file),
            "format": output_format,
            "total_pairs": len(all_data),
            "formatted_examples": len(formatted_data),
            "stats": stats
        }

    def _format_data(self, data: List[Dict], format_type: str) -> List[Dict]:
        """Convert data to specified training format"""

        if format_type == "openai":
            # OpenAI fine-tuning format (messages)
            return [
                {
                    "messages": [
                        {"role": "system", "content": "You are an expert cryptocurrency and blockchain consultant with deep knowledge of trading, technical analysis, and market dynamics."},
                        {"role": "user", "content": item["question"]},
                        {"role": "assistant", "content": item["answer"]}
                    ]
                }
                for item in data
            ]

        elif format_type == "alpaca":
            # Alpaca instruction format
            return [
                {
                    "instruction": item["question"],
                    "input": "",
                    "output": item["answer"]
                }
                for item in data
            ]

        elif format_type == "sharegpt":
            # ShareGPT conversation format
            return [
                {
                    "conversations": [
                        {"from": "human", "value": item["question"]},
                        {"from": "gpt", "value": item["answer"]}
                    ]
                }
                for item in data
            ]

        elif format_type == "jsonl":
            # Simple JSONL format
            return [
                {
                    "question": item["question"],
                    "answer": item["answer"]
                }
                for item in data
            ]

        elif format_type == "raw":
            # Raw format with all metadata
            return data

        else:
            raise ValueError(f"Unknown format: {format_type}")

    def _calculate_stats(self, raw_data: List[Dict], formatted_data: List[Dict]) -> Dict[str, Any]:
        """Calculate statistics about the extracted data"""

        if not raw_data:
            return {}

        # Calculate answer length stats
        lengths = [item["answer_length"] for item in raw_data if item.get("answer_length")]

        # Topic distribution
        topics = {}
        for item in raw_data:
            topic = item.get("topic", "unknown")
            topics[topic] = topics.get(topic, 0) + 1

        # Subtopic distribution
        subtopics = {}
        for item in raw_data:
            subtopic = item.get("subtopic", "unknown")
            subtopics[subtopic] = subtopics.get(subtopic, 0) + 1

        stats = {
            "total_qa_pairs": len(raw_data),
            "avg_answer_length": sum(lengths) // len(lengths) if lengths else 0,
            "min_answer_length": min(lengths) if lengths else 0,
            "max_answer_length": max(lengths) if lengths else 0,
            "total_topics": len(topics),
            "total_subtopics": len(subtopics),
            "topic_distribution": topics,
            "meets_3000_char_minimum": sum(1 for l in lengths if l >= 3000),
            "percentage_meeting_minimum": (sum(1 for l in lengths if l >= 3000) / len(lengths) * 100) if lengths else 0
        }

        return stats

    def extract_by_topic(self, topic: str, output_format: str = "openai", output_dir: str = "training_data") -> Dict[str, Any]:
        """Extract Q&A pairs for a specific topic"""
        return self.extract_all(
            output_format=output_format,
            output_dir=output_dir,
            filter_by={"topic": topic}
        )

    def extract_by_subtopic(self, subtopic: str, output_format: str = "openai", output_dir: str = "training_data") -> Dict[str, Any]:
        """Extract Q&A pairs for a specific subtopic"""
        return self.extract_all(
            output_format=output_format,
            output_dir=output_dir,
            filter_by={"subtopic": subtopic}
        )

    def export_splits(self,
                      train_ratio: float = 0.8,
                      val_ratio: float = 0.1,
                      test_ratio: float = 0.1,
                      output_format: str = "openai",
                      output_dir: str = "training_data") -> Dict[str, Any]:
        """
        Export data split into train/validation/test sets

        Args:
            train_ratio: Ratio for training set (default 0.8)
            val_ratio: Ratio for validation set (default 0.1)
            test_ratio: Ratio for test set (default 0.1)
            output_format: Format for training data
            output_dir: Directory to save splits

        Returns:
            Dictionary with file paths and stats
        """
        import random

        print(f"\n[SPLIT] Creating train/val/test splits...")
        print(f"[SPLIT] Ratios - Train: {train_ratio}, Val: {val_ratio}, Test: {test_ratio}")

        # Validate ratios
        if abs(train_ratio + val_ratio + test_ratio - 1.0) > 0.01:
            raise ValueError("Ratios must sum to 1.0")

        # Extract all data
        result = self.extract_all(output_format="raw", output_dir=output_dir)

        # Load the raw data file
        raw_file = Path(result["output_file"])
        all_data = []
        with open(raw_file, 'r', encoding='utf-8') as f:
            for line in f:
                all_data.append(json.loads(line))

        # Shuffle data
        random.shuffle(all_data)

        # Calculate split indices
        total = len(all_data)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)

        # Split data
        train_data = all_data[:train_end]
        val_data = all_data[train_end:val_end]
        test_data = all_data[val_end:]

        print(f"[SPLIT] Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")

        # Format each split
        train_formatted = self._format_data(train_data, output_format)
        val_formatted = self._format_data(val_data, output_format)
        test_formatted = self._format_data(test_data, output_format)

        # Save splits
        output_path = Path(output_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        splits = {}
        for split_name, split_data in [("train", train_formatted), ("val", val_formatted), ("test", test_formatted)]:
            filename = f"{split_name}_{output_format}_{timestamp}.jsonl"
            split_file = output_path / filename

            with open(split_file, 'w', encoding='utf-8') as f:
                for item in split_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')

            splits[split_name] = {
                "file": str(split_file),
                "count": len(split_data)
            }
            print(f"[SAVED] {split_name}: {split_file}")

        # Remove temporary raw file
        raw_file.unlink()

        return {
            "success": True,
            "format": output_format,
            "splits": splits,
            "total": total
        }


def main():
    """CLI interface"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_training_data.py <format> [options]")
        print()
        print("Formats:")
        print("  openai   - OpenAI fine-tuning format (messages)")
        print("  alpaca   - Alpaca instruction format")
        print("  sharegpt - ShareGPT conversation format")
        print("  jsonl    - Simple JSONL format")
        print("  raw      - Raw format with metadata")
        print()
        print("Options:")
        print("  --split        Create train/val/test splits (80/10/10)")
        print("  --topic TOPIC  Extract only specific topic")
        print("  --output DIR   Output directory (default: training_data)")
        print()
        print("Examples:")
        print("  python extract_training_data.py openai")
        print("  python extract_training_data.py alpaca --split")
        print("  python extract_training_data.py openai --topic 'Cryptocurrency'")
        sys.exit(1)

    format_type = sys.argv[1]

    # Parse options
    do_split = "--split" in sys.argv
    topic = None
    output_dir = "training_data"

    for i, arg in enumerate(sys.argv):
        if arg == "--topic" and i + 1 < len(sys.argv):
            topic = sys.argv[i + 1]
        elif arg == "--output" and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]

    # Initialize extractor
    try:
        extractor = TrainingDataExtractor()
    except Exception as e:
        print(f"[ERROR] Failed to initialize extractor: {e}")
        sys.exit(1)

    # Extract data
    try:
        if do_split:
            result = extractor.export_splits(output_format=format_type, output_dir=output_dir)
            print("\n" + "="*80)
            print("EXTRACTION COMPLETE - SPLITS CREATED")
            print("="*80)
            print(f"Format: {result['format']}")
            print(f"Total Q&A pairs: {result['total']}")
            print()
            for split_name, split_info in result['splits'].items():
                print(f"{split_name.upper()}: {split_info['count']} examples")
                print(f"  File: {split_info['file']}")
        elif topic:
            result = extractor.extract_by_topic(topic=topic, output_format=format_type, output_dir=output_dir)
            print("\n" + "="*80)
            print("EXTRACTION COMPLETE")
            print("="*80)
            print(f"Output file: {result['output_file']}")
            print(f"Format: {result['format']}")
            print(f"Total examples: {result['formatted_examples']}")
            print(f"\nStatistics:")
            for key, value in result['stats'].items():
                if key not in ['topic_distribution']:
                    print(f"  {key}: {value}")
        else:
            result = extractor.extract_all(output_format=format_type, output_dir=output_dir)
            print("\n" + "="*80)
            print("EXTRACTION COMPLETE")
            print("="*80)
            print(f"Output file: {result['output_file']}")
            print(f"Format: {result['format']}")
            print(f"Total examples: {result['formatted_examples']}")
            print(f"\nStatistics:")
            for key, value in result['stats'].items():
                if key not in ['topic_distribution', 'subtopic_distribution']:
                    print(f"  {key}: {value}")
            print(f"\nTopics: {result['stats'].get('total_topics', 0)}")
            print(f"Subtopics: {result['stats'].get('total_subtopics', 0)}")

    except Exception as e:
        print(f"\n[ERROR] Extraction failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
