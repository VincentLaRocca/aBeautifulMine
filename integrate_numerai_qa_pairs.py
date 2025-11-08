#!/usr/bin/env python3
"""
Integrate Numerai-inspired Crypto Q&A Pairs into Database
Processes numerai_crypto_qa_pairs.json and adds to production database
"""

import sqlite3
import json
import hashlib
from datetime import datetime

class NumeraiQAIntegrator:
    def __init__(self, db_path='crypto_indicators_production.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.stats = {
            'pairs_added': 0,
            'duplicates_skipped': 0,
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

    def get_or_create_indicator(self, topic):
        """Get or create crypto indicator entry"""
        # Extract indicator name from topic (first word or phrase)
        indicator_name = topic.split()[0] if topic else "Numerai"

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
            f"Adapted from Numerai Signals: {topic}",
            datetime.now().isoformat()
        ))
        self.conn.commit()
        return self.cursor.lastrowid

    def insert_qa_pair(self, pair):
        """Insert Q&A pair into database"""
        question = pair.get('question', '')
        answer = pair.get('answer', '')
        topic = pair.get('topic', 'Numerai Signals')
        pair_id = pair.get('pair_id', '')

        # Generate hash
        question_hash = self.generate_hash(question, answer)

        # Check duplicate
        if self.is_duplicate(question_hash):
            self.stats['duplicates_skipped'] += 1
            return False, "Duplicate"

        # Get indicator ID
        indicator_id = self.get_or_create_indicator(topic)
        indicator_name = topic.split()[0] if topic else "Numerai"

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
                'numerai_signals_crypto_adaptation',
                json.dumps({'pair_id': pair_id, 'topic': topic})
            ))
            self.conn.commit()
            self.stats['pairs_added'] += 1
            return True, "Added"
        except Exception as e:
            self.stats['errors'] += 1
            return False, str(e)

    def process_json_file(self, json_file):
        """Process Numerai crypto Q&A JSON file"""
        print(f"\n📄 Processing: {json_file}")

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            qa_pairs = data.get('qa_pairs', [])
            total_pairs = data.get('total_pairs', len(qa_pairs))

            print(f"📊 Found {total_pairs} Q&A pairs")
            print("=" * 70)

            initial_count = self.get_current_count()
            print(f"📊 Initial database: {initial_count:,} pairs\n")

            # Process each pair
            for i, pair in enumerate(qa_pairs, 1):
                success, reason = self.insert_qa_pair(pair)
                status = "✅" if success else "❌"
                print(f"{status} Pair {i}/{total_pairs}: {pair.get('pair_id', 'unknown')} - {reason}")

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
            print(f"   Successfully added: {self.stats['pairs_added']}")
            print(f"   Duplicates skipped: {self.stats['duplicates_skipped']}")
            print(f"   Errors:             {self.stats['errors']}")

            if pairs_added > 0:
                print(f"\n✨ NUMERAI SIGNALS CRYPTO Q&A INTEGRATED!")
                print(f"🌟 Database enhanced with quantitative finance methodology\n")

        except Exception as e:
            print(f"❌ Error processing file: {e}")
            self.stats['errors'] += 1

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("💾 Database closed. All changes saved.")


if __name__ == "__main__":
    print("=" * 70)
    print("🔬 NUMERAI SIGNALS CRYPTO Q&A INTEGRATION")
    print("=" * 70)
    print("\n📈 Adapting quantitative finance tournament methodology")
    print("⚡ Integrating technical indicators for crypto markets\n")

    integrator = NumeraiQAIntegrator()
    integrator.connect()
    integrator.process_json_file('numerai_crypto_qa_pairs.json')
    integrator.close()
