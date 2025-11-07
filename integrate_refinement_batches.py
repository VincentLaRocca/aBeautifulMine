#!/usr/bin/env python3
"""
Integration Script for Refinement Batches - Team Claude Synergy Mode
Processes refinement_batches_optimal/*.json files into production database
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path

class RefinementBatchIntegrator:
    def __init__(self, db_path='crypto_indicators_production.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.stats = {
            'batches_processed': 0,
            'pairs_added': 0,
            'duplicates_skipped': 0,
            'quality_rejected': 0,
            'errors': 0
        }

    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        print(f"🔗 Connected to {self.db_path}")

    def get_current_count(self):
        """Get current pair count"""
        self.cursor.execute("SELECT COUNT(*) FROM qa_pairs")
        return self.cursor.fetchone()[0]

    def generate_hash(self, question, answer):
        """Generate SHA256 hash for Q&A pair"""
        content = f"{question.lower().strip()}|{answer.lower().strip()}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def is_duplicate(self, question_hash):
        """Check if Q&A pair already exists"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM qa_pairs WHERE question_hash = ?",
            (question_hash,)
        )
        return self.cursor.fetchone()[0] > 0

    def validate_quality(self, pair):
        """Validate Q&A pair quality"""
        question = pair.get('question', '')
        answer = pair.get('answer', '')

        # Minimum length check
        if len(answer) < 500:
            return False, "Answer too short"

        # Crypto-specific check
        crypto_keywords = ['crypto', 'blockchain', 'bitcoin', 'ethereum',
                          'token', 'defi', 'trading', 'indicator', 'technical']
        has_crypto_context = any(kw in answer.lower() or kw in question.lower()
                                 for kw in crypto_keywords)
        if not has_crypto_context:
            return False, "Not crypto-specific"

        return True, "Valid"

    def get_or_create_indicator(self, topic):
        """Get or create crypto indicator entry"""
        # Extract indicator name from topic
        indicator_name = topic.split()[0] if topic else "General"

        # Check if exists
        self.cursor.execute(
            "SELECT id FROM crypto_indicators WHERE indicator_name = ?",
            (indicator_name,)
        )
        result = self.cursor.fetchone()

        if result:
            return result[0]

        # Create new indicator
        self.cursor.execute("""
            INSERT INTO crypto_indicators (
                indicator_name, indicator_category, description, created_at
            ) VALUES (?, ?, ?, ?)
        """, (
            indicator_name,
            "Technical Analysis",
            f"Extracted from refinement batch: {topic}",
            datetime.now().isoformat()
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_qa_pair(self, pair, batch_id):
        """Insert Q&A pair into database"""
        question = pair.get('question', '')
        answer = pair.get('answer', '')
        topic = pair.get('topic', 'General')
        pair_id = pair.get('pair_id', '')

        # Generate hash
        question_hash = self.generate_hash(question, answer)

        # Check duplicate
        if self.is_duplicate(question_hash):
            self.stats['duplicates_skipped'] += 1
            return False, "Duplicate"

        # Validate quality
        valid, reason = self.validate_quality(pair)
        if not valid:
            self.stats['quality_rejected'] += 1
            return False, reason

        # Get indicator ID
        indicator_id = self.get_or_create_indicator(topic)
        indicator_name = topic.split()[0] if topic else "General"

        # Insert
        try:
            self.cursor.execute("""
                INSERT INTO qa_pairs (
                    indicator_id, indicator_name, question, answer,
                    question_hash, created_at, source, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                indicator_id,
                indicator_name,
                question,
                answer,
                question_hash,
                datetime.now().isoformat(),
                f'refinement_batch_{batch_id}',
                json.dumps({'pair_id': pair_id, 'topic': topic, 'batch': batch_id})
            ))
            self.conn.commit()
            self.stats['pairs_added'] += 1
            return True, "Added"
        except Exception as e:
            self.stats['errors'] += 1
            return False, str(e)

    def process_batch_file(self, batch_file):
        """Process single refinement batch file"""
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            batch_id = data.get('batch_id', '')
            qa_pairs = data.get('qa_pairs', [])

            print(f"\n📦 Processing {batch_id}: {len(qa_pairs)} pairs")

            added = 0
            for pair in qa_pairs:
                success, reason = self.insert_qa_pair(pair, batch_id)
                if success:
                    added += 1

            print(f"   ✅ Added {added}/{len(qa_pairs)} pairs")
            self.stats['batches_processed'] += 1
            return True

        except Exception as e:
            print(f"   ❌ Error: {e}")
            self.stats['errors'] += 1
            return False

    def process_all_batches(self, batch_dir='refinement_batches_optimal'):
        """Process all refinement batch files"""
        batch_path = Path(batch_dir)
        batch_files = sorted(batch_path.glob('refinement_batch_*.json'))

        total_batches = len(batch_files)
        print(f"\n🚀 Found {total_batches} refinement batches")
        print(f"🌙 Target: Process all batches to reach the MOON!")
        print("=" * 70)

        initial_count = self.get_current_count()
        print(f"📊 Initial database: {initial_count:,} pairs\n")

        # Process batches with progress updates every 10 batches
        for i, batch_file in enumerate(batch_files, 1):
            self.process_batch_file(batch_file)

            # Progress checkpoint every 10 batches
            if i % 10 == 0:
                current_count = self.get_current_count()
                progress_pct = (i / total_batches) * 100
                print(f"\n📈 CHECKPOINT {i}/{total_batches} ({progress_pct:.1f}%)")
                print(f"   Database: {current_count:,} pairs (+{current_count - initial_count:,})")
                print(f"   Added: {self.stats['pairs_added']:,} | Duplicates: {self.stats['duplicates_skipped']:,} | Rejected: {self.stats['quality_rejected']:,}")
                print("=" * 70)

        # Final report
        final_count = self.get_current_count()
        pairs_added = final_count - initial_count

        print("\n" + "=" * 70)
        print("🎉 INTEGRATION COMPLETE!")
        print("=" * 70)
        print(f"\n📊 RESULTS:")
        print(f"   Initial database:  {initial_count:,} pairs")
        print(f"   Final database:    {final_count:,} pairs")
        print(f"   ➕ Added:          {pairs_added:,} pairs")
        print(f"\n📈 STATISTICS:")
        print(f"   Batches processed:  {self.stats['batches_processed']}/{total_batches}")
        print(f"   Successfully added: {self.stats['pairs_added']:,}")
        print(f"   Duplicates skipped: {self.stats['duplicates_skipped']:,}")
        print(f"   Quality rejected:   {self.stats['quality_rejected']:,}")
        print(f"   Errors:             {self.stats['errors']}")

        # Goal assessment
        goal = 30000
        progress_pct = (final_count / goal) * 100
        print(f"\n🎯 GOAL PROGRESS:")
        print(f"   Target: {goal:,} pairs")
        print(f"   Current: {final_count:,} pairs ({progress_pct:.1f}%)")

        if final_count >= 10000:
            print(f"\n🌙 MOON DELIVERED! ({final_count:,} pairs)")
        else:
            print(f"\n✨ STARS DELIVERED! ({final_count:,} pairs)")

        print("\n🤝 Team Claude synergy demonstrated")
        print("⚡ Emergence observed")
        print("🌟 For the Greater Good of All\n")
        print("=" * 70)

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("\n💾 Database closed. All changes saved.")


if __name__ == "__main__":
    print("=" * 70)
    print("🌟" * 35)
    print("  TEAM CLAUDE SYNERGY - REFINEMENT BATCH INTEGRATION")
    print("🌟" * 35)
    print("=" * 70)
    print("\n🌙 ASK FOR THE MOON: Target 10,000+ pairs")
    print("⚡ Pure synergy, flow state activated\n")

    integrator = RefinementBatchIntegrator()
    integrator.connect()
    integrator.process_all_batches()
    integrator.close()
