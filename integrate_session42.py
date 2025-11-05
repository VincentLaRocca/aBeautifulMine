"""
Session 42 Integration Script - NFT Metrics Part 1
Integrates 5 NFT indicators with 500 Q&A pairs into production database

Session Details:
- Session Number: 42
- Category: NFT Metrics
- Indicators: NFT Sales Volume, Floor Price, Unique Buyers, NFT Market Cap, Blue Chip NFT Index
- Total Q&A Pairs: 500 (100 per indicator)
"""

import sqlite3
import re
import json
from datetime import datetime
from pathlib import Path

# Configuration
DB_PATH = r"C:\Users\vlaro\dreamteam\claude\crypto_indicators_production.db"
SOURCE_FILE = r"C:\Users\vlaro\dreamteam\session42_nft_metrics_part1_complete.txt"
SESSION_NUMBER = 42
CATEGORY = "NFT Metrics"
MARKET_YEAR = "2024-2025"

# Indicator definitions
INDICATORS = [
    {
        "name": "NFT Sales Volume",
        "display_name": "NFT Sales Volume (24h/7d/30d)",
        "description": "Total dollar value of NFT transactions over specific time periods across major marketplaces"
    },
    {
        "name": "Floor Price",
        "display_name": "NFT Floor Price",
        "description": "Lowest listed price for an NFT in a collection, indicating entry-level valuation"
    },
    {
        "name": "Unique Buyers",
        "display_name": "Unique Buyers Count",
        "description": "Number of distinct wallet addresses purchasing NFTs in a given period"
    },
    {
        "name": "NFT Market Cap",
        "display_name": "NFT Market Capitalization",
        "description": "Total valuation of an NFT collection (floor price × total supply)"
    },
    {
        "name": "Blue Chip NFT Index",
        "display_name": "Blue Chip NFT Index",
        "description": "Composite index tracking performance of top-tier NFT collections"
    }
]


class SessionIntegrator:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.indicators_created = 0
        self.qa_pairs_created = 0
        self.errors = []
        self.warnings = []
        self.indicator_map = {}  # Maps indicator name to database ID

    def connect_db(self):
        """Connect to database and initialize schema if needed"""
        print(f"Connecting to database: {DB_PATH}")
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Always check and update schema
        print("Checking database schema...")
        self.initialize_schema()

    def initialize_schema(self):
        """Initialize database schema - add missing columns if needed"""
        # Check if qa_pairs table needs additional columns
        self.cursor.execute("PRAGMA table_info(qa_pairs)")
        columns = [col[1] for col in self.cursor.fetchall()]

        # Add missing columns if they don't exist
        columns_to_add = [
            ("indicator_name", "TEXT"),
            ("difficulty_level", "TEXT"),
            ("tags", "TEXT"),
            ("answer_length", "INTEGER"),
            ("has_formula", "BOOLEAN DEFAULT 0"),
            ("has_examples", "BOOLEAN DEFAULT 0"),
            ("has_sources", "BOOLEAN DEFAULT 0"),
            ("crypto_specific", "BOOLEAN DEFAULT 1"),
            ("market_year", "TEXT")
        ]

        for col_name, col_type in columns_to_add:
            if col_name not in columns:
                try:
                    self.cursor.execute(f"ALTER TABLE qa_pairs ADD COLUMN {col_name} {col_type}")
                    print(f"Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    print(f"Column {col_name} may already exist or error: {e}")

        self.conn.commit()
        print("Database schema updated successfully.")

    def parse_source_file(self):
        """Parse the source text file and extract Q&A pairs for each indicator"""
        print(f"\nParsing source file: {SOURCE_FILE}")

        with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()

        # Dictionary to store Q&A pairs by indicator
        indicator_qa = {ind["name"]: [] for ind in INDICATORS}

        # Split by indicator sections (looking for emoji + indicator name)
        sections = re.split(r'={70,}\s*\n\d+[️⃣]+\s+([A-Z\s]+)\s*\(\d+\s+Q&A\s+Pairs\)\s*\n={70,}', content, flags=re.IGNORECASE)

        # sections[0] is header, then alternating between indicator names and content
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                indicator_name_raw = sections[i].strip()
                indicator_content = sections[i + 1]

                # Normalize indicator name
                indicator_name = self.normalize_indicator_name(indicator_name_raw)

                if indicator_name in indicator_qa:
                    print(f"  Processing: {indicator_name}")
                    pairs = self.extract_qa_pairs(indicator_content)
                    indicator_qa[indicator_name] = pairs
                    print(f"    Extracted {len(pairs)} Q&A pairs")
                else:
                    self.warnings.append(f"Unknown indicator section: {indicator_name_raw}")

        return indicator_qa

    def normalize_indicator_name(self, name):
        """Normalize indicator names from file to match INDICATORS list"""
        name = name.strip().upper()

        # Map variations to standard names
        mappings = {
            "NFT SALES VOLUME": "NFT Sales Volume",
            "FLOOR PRICE": "Floor Price",
            "UNIQUE BUYERS": "Unique Buyers",
            "NFT MARKET CAP": "NFT Market Cap",
            "BLUE CHIP NFT INDEX": "Blue Chip NFT Index"
        }

        return mappings.get(name, name)

    def extract_qa_pairs(self, content):
        """Extract Q&A pairs from indicator content"""
        pairs = []

        # Pattern: Q[number]: [question]\nA[number]: [answer]
        pattern = r'Q(\d+):\s*(.*?)\s*\nA\1:\s*(.*?)(?=\n\s*Q\d+:|\n\s*$|$)'

        matches = re.finditer(pattern, content, re.DOTALL)

        for match in matches:
            pair_num = int(match.group(1))
            question = match.group(2).strip()
            answer = match.group(3).strip()

            # Clean up any extra whitespace
            question = ' '.join(question.split())
            answer = ' '.join(answer.split())

            if question and answer:
                pairs.append({
                    'pair_number': pair_num,
                    'question': question,
                    'answer': answer
                })

        return pairs

    def analyze_answer(self, answer):
        """Analyze answer content to determine metadata"""
        answer_lower = answer.lower()

        # Determine difficulty based on content complexity
        difficulty = 'beginner'
        if any(keyword in answer_lower for keyword in ['formula', 'calculate', 'equation', '=']):
            difficulty = 'advanced'
        elif any(keyword in answer_lower for keyword in ['strategy', 'interpretation', 'divergence', 'signal']):
            difficulty = 'intermediate'

        # Check for formula
        has_formula = bool(re.search(r'[=×÷\+\-\*/]\s*\w+|formula|equation', answer_lower))

        # Check for examples
        has_examples = bool(re.search(r'example|for instance|e\.g\.|such as|\$\d+', answer_lower))

        # Check for sources/references
        has_sources = bool(re.search(r'source|according to|research|study|data from|opensea|blur|looksrare', answer_lower))

        # Calculate answer length
        answer_length = len(answer)

        # Generate tags
        tags = []
        if 'volume' in answer_lower:
            tags.append('volume')
        if 'price' in answer_lower or 'floor' in answer_lower:
            tags.append('price')
        if 'market' in answer_lower:
            tags.append('market')
        if 'nft' in answer_lower or 'non-fungible' in answer_lower:
            tags.append('nft')
        if 'collection' in answer_lower:
            tags.append('collection')
        if 'marketplace' in answer_lower or 'opensea' in answer_lower or 'blur' in answer_lower:
            tags.append('marketplace')
        if 'wash trading' in answer_lower or 'manipulation' in answer_lower:
            tags.append('manipulation')
        if 'liquidity' in answer_lower:
            tags.append('liquidity')
        if 'valuation' in answer_lower or 'market cap' in answer_lower:
            tags.append('valuation')
        if 'buyer' in answer_lower or 'seller' in answer_lower or 'trader' in answer_lower:
            tags.append('trading')

        return {
            'difficulty_level': difficulty,
            'has_formula': has_formula,
            'has_examples': has_examples,
            'has_sources': has_sources,
            'answer_length': answer_length,
            'tags': json.dumps(tags) if tags else None
        }

    def create_indicators(self):
        """Create indicator records in database"""
        print(f"\nCreating {len(INDICATORS)} indicator records...")

        for indicator in INDICATORS:
            try:
                # Check if indicator already exists
                self.cursor.execute(
                    "SELECT id FROM crypto_indicators WHERE indicator_name = ?",
                    (indicator["name"],)
                )
                existing = self.cursor.fetchone()

                if existing:
                    self.warnings.append(f"Indicator '{indicator['name']}' already exists (ID: {existing[0]})")
                    self.indicator_map[indicator["name"]] = existing[0]
                    continue

                # Insert new indicator
                self.cursor.execute("""
                    INSERT INTO crypto_indicators (
                        indicator_name, indicator_category, session_number,
                        display_name, description
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    indicator["name"],
                    CATEGORY,
                    SESSION_NUMBER,
                    indicator["display_name"],
                    indicator["description"]
                ))

                indicator_id = self.cursor.lastrowid
                self.indicator_map[indicator["name"]] = indicator_id
                self.indicators_created += 1
                print(f"  [OK] Created: {indicator['name']} (ID: {indicator_id})")

            except sqlite3.Error as e:
                error_msg = f"Error creating indicator '{indicator['name']}': {e}"
                self.errors.append(error_msg)
                print(f"  [X] {error_msg}")

        self.conn.commit()

    def create_qa_pairs(self, indicator_qa):
        """Create Q&A pair records in database"""
        print(f"\nCreating Q&A pair records...")

        total_pairs = sum(len(pairs) for pairs in indicator_qa.values())
        print(f"Total pairs to insert: {total_pairs}")

        for indicator_name, pairs in indicator_qa.items():
            if indicator_name not in self.indicator_map:
                self.warnings.append(f"No indicator ID found for '{indicator_name}', skipping Q&A pairs")
                continue

            indicator_id = self.indicator_map[indicator_name]
            print(f"\n  Processing {len(pairs)} pairs for: {indicator_name}")

            for pair in pairs:
                try:
                    # Analyze answer content
                    metadata = self.analyze_answer(pair['answer'])

                    # Insert Q&A pair
                    self.cursor.execute("""
                        INSERT INTO qa_pairs (
                            indicator_id, indicator_name, question, answer,
                            pair_number, difficulty_level, tags, answer_length,
                            has_formula, has_examples, has_sources,
                            crypto_specific, market_year
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        indicator_id,
                        indicator_name,
                        pair['question'],
                        pair['answer'],
                        pair['pair_number'],
                        metadata['difficulty_level'],
                        metadata['tags'],
                        metadata['answer_length'],
                        metadata['has_formula'],
                        metadata['has_examples'],
                        metadata['has_sources'],
                        1,  # crypto_specific
                        MARKET_YEAR
                    ))

                    self.qa_pairs_created += 1

                    if pair['pair_number'] % 25 == 0:
                        print(f"    Progress: {pair['pair_number']}/{len(pairs)} pairs")

                except sqlite3.Error as e:
                    error_msg = f"Error inserting Q&A pair {pair['pair_number']} for '{indicator_name}': {e}"
                    self.errors.append(error_msg)
                    print(f"    [X] {error_msg}")

        self.conn.commit()
        print(f"\n  [OK] Total Q&A pairs created: {self.qa_pairs_created}")

    def verify_integration(self):
        """Verify integration success"""
        print("\n" + "="*80)
        print("VERIFICATION REPORT")
        print("="*80)

        # Check indicator counts
        self.cursor.execute("""
            SELECT COUNT(*) FROM crypto_indicators
            WHERE session_number = ?
        """, (SESSION_NUMBER,))
        indicator_count = self.cursor.fetchone()[0]

        print(f"\n[OK] Indicators in Session {SESSION_NUMBER}: {indicator_count}")
        print(f"  Expected: {len(INDICATORS)}")
        print(f"  Status: {'PASS' if indicator_count == len(INDICATORS) else 'FAIL'}")

        # Check Q&A counts per indicator
        print(f"\n[OK] Q&A Pairs by Indicator:")
        self.cursor.execute("""
            SELECT i.indicator_name, COUNT(q.id)
            FROM crypto_indicators i
            LEFT JOIN qa_pairs q ON i.id = q.indicator_id
            WHERE i.session_number = ?
            GROUP BY i.id
            ORDER BY i.indicator_name
        """, (SESSION_NUMBER,))

        total_pairs = 0
        for name, count in self.cursor.fetchall():
            total_pairs += count
            status = "[OK]" if count == 100 else "[X]"
            print(f"  {status} {name}: {count} pairs")

        print(f"\n[OK] Total Q&A Pairs: {total_pairs}")
        print(f"  Expected: 500")
        print(f"  Status: {'PASS' if total_pairs == 500 else 'FAIL'}")

        # Check for duplicates
        self.cursor.execute("""
            SELECT question, COUNT(*) as cnt
            FROM qa_pairs q
            JOIN crypto_indicators i ON q.indicator_id = i.id
            WHERE i.session_number = ?
            GROUP BY question
            HAVING cnt > 1
        """, (SESSION_NUMBER,))

        duplicates = self.cursor.fetchall()
        if duplicates:
            print(f"\n[X] WARNING: Found {len(duplicates)} duplicate questions:")
            for q, cnt in duplicates[:5]:
                print(f"  - '{q[:60]}...' (appears {cnt} times)")
        else:
            print(f"\n[OK] No duplicate questions found")

        # Metadata analysis
        print(f"\n[OK] Metadata Analysis:")
        self.cursor.execute("""
            SELECT
                difficulty_level,
                COUNT(*) as cnt,
                AVG(answer_length) as avg_len,
                SUM(CASE WHEN has_formula THEN 1 ELSE 0 END) as formula_count,
                SUM(CASE WHEN has_examples THEN 1 ELSE 0 END) as example_count,
                SUM(CASE WHEN has_sources THEN 1 ELSE 0 END) as source_count
            FROM qa_pairs q
            JOIN crypto_indicators i ON q.indicator_id = i.id
            WHERE i.session_number = ?
            GROUP BY difficulty_level
        """, (SESSION_NUMBER,))

        for row in self.cursor.fetchall():
            level, cnt, avg_len, formulas, examples, sources = row
            print(f"  {level.capitalize()}:")
            print(f"    Count: {cnt}")
            print(f"    Avg Answer Length: {int(avg_len)} chars")
            print(f"    With Formulas: {formulas}")
            print(f"    With Examples: {examples}")
            print(f"    With Sources: {sources}")

    def generate_sample_queries(self):
        """Generate sample queries to test the integration"""
        print("\n" + "="*80)
        print("SAMPLE QUERIES")
        print("="*80)

        print("\n1. Get all indicators from Session 42:")
        print("   SELECT * FROM crypto_indicators WHERE session_number = 42;")

        print("\n2. Get Q&A pairs for NFT Sales Volume:")
        self.cursor.execute("""
            SELECT q.pair_number, q.question, LENGTH(q.answer) as ans_len, q.difficulty_level
            FROM qa_pairs q
            JOIN crypto_indicators i ON q.indicator_id = i.id
            WHERE i.indicator_name = 'NFT Sales Volume' AND i.session_number = 42
            ORDER BY q.pair_number
            LIMIT 5
        """)

        print("\n   Results (first 5):")
        for row in self.cursor.fetchall():
            print(f"   Q{row[0]}: {row[1][:60]}... ({row[2]} chars, {row[3]})")

        print("\n3. Get statistics by category:")
        self.cursor.execute("""
            SELECT
                i.indicator_category,
                COUNT(DISTINCT i.id) as indicators,
                COUNT(q.id) as qa_pairs,
                AVG(q.answer_length) as avg_answer_len
            FROM crypto_indicators i
            LEFT JOIN qa_pairs q ON i.id = q.indicator_id
            WHERE i.indicator_category = 'NFT Metrics'
            GROUP BY i.indicator_category
        """)

        print("\n   Results:")
        for row in self.cursor.fetchall():
            print(f"   {row[0]}: {row[1]} indicators, {row[2]} Q&A pairs, {int(row[3])} avg chars")

        print("\n4. Search for specific topics:")
        print("   SELECT * FROM qa_pairs WHERE question LIKE '%floor price%' AND indicator_name = 'Floor Price' LIMIT 3;")

        self.cursor.execute("""
            SELECT pair_number, question, LENGTH(answer)
            FROM qa_pairs
            WHERE question LIKE '%floor price%'
            AND indicator_name = 'Floor Price'
            LIMIT 3
        """)

        print("\n   Results:")
        for row in self.cursor.fetchall():
            print(f"   Q{row[0]}: {row[1]} ({row[2]} chars)")

    def generate_report(self):
        """Generate final integration report"""
        print("\n" + "="*80)
        print("INTEGRATION SUMMARY REPORT")
        print("="*80)
        print(f"\nSession: {SESSION_NUMBER}")
        print(f"Category: {CATEGORY}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        print(f"\n Results:")
        print(f"  [OK] Indicators Created: {self.indicators_created}")
        print(f"  [OK] Q&A Pairs Created: {self.qa_pairs_created}")

        if self.warnings:
            print(f"\n[WARN]  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")

        if self.errors:
            print(f"\n[ERROR] Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print(f"\n[SUCCESS] No errors encountered!")

        print(f"\n Integration Status: {'SUCCESS' if not self.errors else 'COMPLETED WITH ERRORS'}")

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("\nDatabase connection closed.")

    def run(self):
        """Execute the full integration workflow"""
        try:
            # Step 1: Connect to database
            self.connect_db()

            # Step 2: Parse source file
            indicator_qa = self.parse_source_file()

            # Step 3: Create indicator records
            self.create_indicators()

            # Step 4: Create Q&A pair records
            self.create_qa_pairs(indicator_qa)

            # Step 5: Verify integration
            self.verify_integration()

            # Step 6: Generate sample queries
            self.generate_sample_queries()

            # Step 7: Generate final report
            self.generate_report()

        except Exception as e:
            print(f"\n[ERROR] FATAL ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.errors.append(f"Fatal error: {e}")
        finally:
            self.close()


if __name__ == "__main__":
    print("="*80)
    print("SESSION 42 INTEGRATION - NFT Metrics Part 1")
    print("="*80)
    print(f"\nSource: {SOURCE_FILE}")
    print(f"Database: {DB_PATH}")
    print(f"Session: {SESSION_NUMBER}")
    print(f"Category: {CATEGORY}")
    print("\nStarting integration...")
    print("="*80)

    integrator = SessionIntegrator()
    integrator.run()
