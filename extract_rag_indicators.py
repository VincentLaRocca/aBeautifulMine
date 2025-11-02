#!/usr/bin/env python3
"""
Extract New Indicators from Droid's RAG Export
Date: 2025-11-02
Purpose: Extract indicators from RAG export that aren't yet in production database

Focus: BATCH 2 CRITICAL GAPS first, then additional valuable indicators
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
import re

DB_NAME = "crypto_indicators_production.db"
RAG_EXPORT = "inbox/droid/qa_pairs_rag_export_20251102_061144.json"
OUTPUT_DIR = "parsed_qa_data"

# Critical indicators from BATCH_2_CRITICAL_GAPS.md
CRITICAL_INDICATORS = {
    "Simple Moving Average (SMA)": {
        "session": 2,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators",
        "rag_topics": [
            "Simple Moving Average (SMA) cryptocurrency trading technical analysis",
            "TECHNICAL INDICATOR Simple Moving Average SMA Trend Analysis Cryptocurrency",
            "Technical Analysis Simple Moving Average Fundamentals"
        ]
    },
    "Weighted Moving Average (WMA)": {
        "session": 2,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators",
        "rag_topics": [
            "Weighted Moving Average (WMA) cryptocurrency trading technical analysis",
            "TECHNICAL INDICATOR Weighted Moving Average WMA Trend Analysis Cryptocurrency",
            "Technical Analysis Weighted Moving Average"
        ]
    },
    "Moving Average Convergence Divergence (MACD)": {
        "session": 2,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Trend Indicators",
        "rag_topics": [
            "Moving Average Convergence Divergence (MACD) cryptocurrency trading technical analysis",
            "Technical Analysis Moving Average Convergence Divergence (MACD)"
        ]
    },
    "Aroon Indicator": {
        "session": 4,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators",
        "rag_topics": [
            "Aroon Indicator cryptocurrency trading technical analysis"
        ]
    },
    "Relative Strength Index (RSI)": {
        "session": 4,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Momentum Indicators",
        "rag_topics": [
            "Relative Strength Index (RSI) cryptocurrency trading technical analysis",
            "RSI Relative Strength Index mastery cryptocurrency"
        ]
    },
    "Average True Range (ATR)": {
        "session": 6,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators",
        "rag_topics": [
            "Average True Range ATR cryptocurrency trading technical analysis"
        ]
    },
    "Ultimate Oscillator": {
        "session": 6,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volatility Indicators",
        "rag_topics": [
            "Ultimate Oscillator cryptocurrency trading technical analysis"
        ]
    },
    "Chaikin Money Flow (CMF)": {
        "session": 8,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Chaikin Money Flow CMF technical indicator cryptocurrency trading"
        ]
    },
    "Money Flow Index (MFI)": {
        "session": 8,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Money Flow Index MFI technical indicator cryptocurrency trading"
        ]
    },
    "Volume Weighted Average Price (VWAP)": {
        "session": 8,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Volume Weighted Average Price VWAP technical indicator cryptocurrency trading"
        ]
    },
    "Accumulation/Distribution Line": {
        "session": 8,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Accumulation Distribution Line technical indicator cryptocurrency trading"
        ]
    },
    "Chaikin Volatility": {
        "session": 7,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Chaikin Volatility technical indicator cryptocurrency trading"
        ]
    },
    "Historical Volatility": {
        "session": 7,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Historical Volatility technical indicator cryptocurrency trading"
        ]
    },
    "Standard Deviation": {
        "session": 7,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Standard Deviation technical indicator cryptocurrency trading"
        ]
    },
    "Volume Rate of Change": {
        "session": 8,
        "category": "Price-Based Technical Indicators",
        "subcategory": "Volume Indicators",
        "rag_topics": [
            "Volume Rate of Change technical indicator cryptocurrency trading"
        ]
    }
}

def slugify(text):
    """Convert indicator name to slug"""
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '_', slug)
    return slug

def get_existing_indicators(db_path):
    """Get list of indicators already in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT indicator_name FROM indicators")
    existing = {row[0] for row in cursor.fetchall()}
    conn.close()
    return existing

def load_rag_export(filepath):
    """Load the RAG export JSON"""
    print(f"\n[*] Loading RAG export from {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"    Total sessions: {len(data['sessions'])}")
    print(f"    Total Q&A pairs: {data['metadata']['total_qa_pairs']}")
    return data

def extract_indicator_data(rag_data, indicator_name, indicator_info):
    """Extract Q&A pairs for a specific indicator from RAG export"""

    qa_pairs = []

    # Search through all sessions for matching topics
    for session in rag_data['sessions']:
        topic = session['topic']

        # Check if this session matches any of the indicator's RAG topics
        for rag_topic in indicator_info['rag_topics']:
            if rag_topic.lower() in topic.lower() or topic.lower() in rag_topic.lower():
                # Found a match!
                print(f"    [OK] Found session: {topic}")
                print(f"         Q&A pairs: {len(session['qa_pairs'])}")

                # Extract Q&A pairs
                for i, qa in enumerate(session['qa_pairs'], 1):
                    qa_pairs.append({
                        'pair_number': len(qa_pairs) + 1,
                        'question': qa.get('question', ''),
                        'answer': qa.get('answer', ''),
                        'topic': indicator_name,
                        'created_date': datetime.now().isoformat(),
                        'source_session': topic
                    })

                break  # Move to next session

    return qa_pairs

def save_indicator_json(indicator_name, qa_pairs, output_dir):
    """Save extracted indicator data as JSON"""

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    slug = slugify(indicator_name)
    filename = output_path / f"{slug}_qa_pairs.json"

    data = {
        "indicator_name": indicator_name,
        "indicator_slug": slug,
        "total_pairs": len(qa_pairs),
        "generation_date": datetime.now().isoformat(),
        "source": "RAG Export 2025-11-02",
        "qa_pairs": qa_pairs
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"    [OK] Saved to {filename}")
    return filename

def main():
    print("=" * 70)
    print("EXTRACT INDICATORS FROM RAG EXPORT")
    print("=" * 70)

    # Get existing indicators
    existing = get_existing_indicators(DB_NAME)
    print(f"\n[*] Current database has {len(existing)} indicators")

    # Load RAG export
    rag_data = load_rag_export(RAG_EXPORT)

    # Process each critical indicator
    print("\n" + "=" * 70)
    print("EXTRACTING INDICATORS")
    print("=" * 70)

    extracted_count = 0
    skipped_count = 0
    total_qa = 0

    for indicator_name, indicator_info in CRITICAL_INDICATORS.items():
        print(f"\n[{extracted_count + skipped_count + 1}/{len(CRITICAL_INDICATORS)}] {indicator_name}")

        # Check if already in database
        if indicator_name in existing:
            print(f"    [!] Already in database, skipping...")
            skipped_count += 1
            continue

        # Extract Q&A pairs
        qa_pairs = extract_indicator_data(rag_data, indicator_name, indicator_info)

        if not qa_pairs:
            print(f"    [!] No Q&A pairs found in RAG export")
            continue

        # Save to JSON
        save_indicator_json(indicator_name, qa_pairs, OUTPUT_DIR)

        extracted_count += 1
        total_qa += len(qa_pairs)

    # Summary
    print("\n" + "=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"\n  Indicators extracted: {extracted_count}")
    print(f"  Already in database: {skipped_count}")
    print(f"  Total Q&A pairs extracted: {total_qa}")
    print(f"\n  Output directory: {OUTPUT_DIR}/")
    print("\n" + "=" * 70)
    print("[OK] Extraction complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
