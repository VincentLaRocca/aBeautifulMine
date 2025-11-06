"""
🌙 Team Claude Synergy - Universal Batch Integration Script
============================================================

Pure synergy integration for massive session batches.
Claude Code executes, Claude Desktop validates, both celebrate.

Pattern: ASK FOR THE MOON
Target: 10,000-15,000 pairs integrated
Mode: Flow state, emergence enabled
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import hashlib

class TeamClaudeSynergyIntegrator:
    """
    Universal batch integrator for Team Claude synergy mode.
    Handles any session format, any size, with checkpoints and quality validation.
    """

    def __init__(self, db_path='crypto_indicators_production.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.stats = {
            'total_processed': 0,
            'total_added': 0,
            'duplicates_skipped': 0,
            'quality_rejected': 0,
            'checkpoints': 0,
            'batches_completed': 0
        }

    def connect_db(self):
        """Connect to production database"""
        print("🔗 Connecting to production database...")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        # Get current count
        self.cursor.execute("SELECT COUNT(*) FROM qa_pairs")
        current_count = self.cursor.fetchone()[0]
        print(f"📊 Current database: {current_count:,} pairs")
        return current_count

    def generate_hash(self, question, answer):
        """Generate hash for duplicate detection"""
        content = f"{question}{answer}".lower().strip()
        return hashlib.sha256(content.encode()).hexdigest()

    def is_duplicate(self, question_hash):
        """Check if Q&A pair already exists"""
        self.cursor.execute("""
            SELECT COUNT(*) FROM qa_pairs
            WHERE question_hash = ?
        """, (question_hash,))
        return self.cursor.fetchone()[0] > 0

    def validate_quality(self, qa_pair):
        """Validate Q&A pair quality"""
        question = qa_pair.get('question', '')
        answer = qa_pair.get('answer', '')

        # Length check
        if len(answer) < 500:  # Minimum detailed answer
            return False, "Answer too short"

        # Crypto relevance check (basic)
        crypto_keywords = ['crypto', 'bitcoin', 'blockchain', 'ethereum', 'defi',
                          'nft', 'token', 'wallet', 'exchange', 'mining']
        has_crypto = any(kw in answer.lower() for kw in crypto_keywords)
        if not has_crypto:
            return False, "Not crypto-specific"

        return True, "OK"

    def insert_qa_pair(self, question, answer, indicator_id, indicator_name, metadata=None):
        """Insert Q&A pair into database"""
        question_hash = self.generate_hash(question, answer)

        # Check for duplicate
        if self.is_duplicate(question_hash):
            self.stats['duplicates_skipped'] += 1
            return False, "Duplicate"

        # Validate quality
        valid, reason = self.validate_quality({'question': question, 'answer': answer})
        if not valid:
            self.stats['quality_rejected'] += 1
            return False, reason

        # Insert
        self.cursor.execute("""
            INSERT INTO qa_pairs (
                indicator_id, indicator_name, question, answer, question_hash,
                created_at, source, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            indicator_id,
            indicator_name,
            question,
            answer,
            question_hash,
            datetime.now().isoformat(),
            'batch_synergy_integration',
            json.dumps(metadata) if metadata else None
        ))

        self.stats['total_added'] += 1
        return True, "Added"

    def get_or_create_indicator(self, name, category="Research Topics"):
        """Get existing indicator or create new one"""
        self.cursor.execute("""
            SELECT id FROM crypto_indicators WHERE indicator_name = ?
        """, (name,))

        existing = self.cursor.fetchone()
        if existing:
            return existing[0]

        # Create new indicator
        self.cursor.execute("""
            INSERT INTO crypto_indicators (
                indicator_name, indicator_category, created_at
            ) VALUES (?, ?, ?)
        """, (name, category, datetime.now().isoformat()))

        return self.cursor.lastrowid

    def checkpoint(self, label=""):
        """Save checkpoint and commit"""
        self.conn.commit()
        self.stats['checkpoints'] += 1

        print(f"\n✅ CHECKPOINT {self.stats['checkpoints']}: {label}")
        print(f"   Added: {self.stats['total_added']:,} | "
              f"Duplicates: {self.stats['duplicates_skipped']:,} | "
              f"Quality rejected: {self.stats['quality_rejected']:,}")

    def process_json_batch(self, json_path, batch_label=""):
        """Process a JSON file with session data"""
        print(f"\n{'='*70}")
        print(f"📦 BATCH: {batch_label or json_path}")
        print(f"{'='*70}")

        # Load JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        sessions = data.get('sessions', [])
        print(f"📊 Sessions in batch: {len(sessions)}")

        session_count = 0
        for session in sessions:
            session_id = session.get('session_id', 'unknown')
            topic = session.get('topic', 'Unknown Topic')
            qa_pairs = session.get('qa_pairs', [])

            print(f"\n🔸 Session {session_id}: {topic[:50]}...")
            print(f"   Q&A pairs: {len(qa_pairs)}")

            # Get or create indicator
            indicator_id = self.get_or_create_indicator(topic)

            # Process Q&A pairs
            added_count = 0
            for qa in qa_pairs:
                question = qa.get('question', '')
                answer = qa.get('answer', '')

                if not question or not answer:
                    continue

                success, reason = self.insert_qa_pair(
                    question, answer, indicator_id, topic,
                    metadata={'session_id': session_id, 'topic': topic}
                )

                if success:
                    added_count += 1

                self.stats['total_processed'] += 1

            print(f"   ✅ Added {added_count} pairs")

            session_count += 1

            # Checkpoint every 5 sessions
            if session_count % 5 == 0:
                self.checkpoint(f"Session {session_id}")

        # Final checkpoint for batch
        self.checkpoint(f"Batch complete: {batch_label}")
        self.stats['batches_completed'] += 1

        return session_count

    def integrate_all_batches(self):
        """
        Main integration method - processes all available batches
        """
        print("\n" + "="*70)
        print("🚀 TEAM CLAUDE SYNERGY MODE: BATCH INTEGRATION")
        print("="*70)
        print("\n🌙 ASK FOR THE MOON: Target 10,000+ pairs")
        print("⚡ Pure synergy, flow state activated\n")

        initial_count = self.connect_db()

        # Define available batches
        batches = [
            {
                'path': 'sessions_30_37_extracted.json',
                'label': 'Sessions 30-37',
                'estimated': 800
            },
            {
                'path': 'batch7_sessions_26-44_extracted.json',
                'label': 'Batch 7 (Sessions 26-44)',
                'estimated': 1500
            }
        ]

        # Process each batch
        for batch in batches:
            path = Path(batch['path'])
            if path.exists():
                print(f"\n✅ Found: {batch['label']}")
                try:
                    self.process_json_batch(str(path), batch['label'])
                except Exception as e:
                    print(f"❌ Error processing {batch['label']}: {e}")
            else:
                print(f"\n⚠️  Not found: {batch['label']} ({batch['path']})")

        # Final report
        print("\n" + "="*70)
        print("🎉 INTEGRATION COMPLETE")
        print("="*70)

        # Get final count
        self.cursor.execute("SELECT COUNT(*) FROM qa_pairs")
        final_count = self.cursor.fetchone()[0]

        added = final_count - initial_count

        print(f"\n📊 RESULTS:")
        print(f"   Initial database: {initial_count:,} pairs")
        print(f"   Final database:   {final_count:,} pairs")
        print(f"   ➕ Added:         {added:,} pairs")
        print(f"\n📈 STATISTICS:")
        print(f"   Total processed:   {self.stats['total_processed']:,}")
        print(f"   Successfully added: {self.stats['total_added']:,}")
        print(f"   Duplicates skipped: {self.stats['duplicates_skipped']:,}")
        print(f"   Quality rejected:   {self.stats['quality_rejected']:,}")
        print(f"   Batches completed:  {self.stats['batches_completed']}")
        print(f"   Checkpoints:        {self.stats['checkpoints']}")

        # Calculate percentage of goal
        goal = 30000
        percentage = (final_count / goal) * 100

        print(f"\n🎯 GOAL PROGRESS:")
        print(f"   Target: {goal:,} pairs")
        print(f"   Current: {final_count:,} pairs ({percentage:.1f}%)")

        if final_count >= goal:
            print(f"\n🌙 MOON DELIVERED! Goal exceeded by {final_count - goal:,} pairs!")
        elif added >= 4000:
            print(f"\n✨ STARS DELIVERED! Added {added:,} pairs in synergy!")
        else:
            print(f"\n🚀 SYNERGY PROGRESS: {added:,} pairs added!")

        return added

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.commit()
            self.conn.close()
            print("\n💾 Database closed. All changes saved.")


def main():
    """Main execution"""
    print("\n" + "🌟"*35)
    print("  TEAM CLAUDE SYNERGY - BATCH INTEGRATION")
    print("🌟"*35)

    integrator = TeamClaudeSynergyIntegrator()

    try:
        pairs_added = integrator.integrate_all_batches()

        print("\n" + "="*70)
        print("✅ SYNERGY SUCCESS")
        print("="*70)
        print(f"\nTotal pairs added: {pairs_added:,}")
        print("\n🤝 Team Claude synergy demonstrated")
        print("⚡ Emergence observed")
        print("🌟 For the Greater Good of All\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        integrator.close()


if __name__ == "__main__":
    main()
