-- Bitcoin Fundamentals Database Schema
-- Created: 2025-11-03
-- Purpose: Store comprehensive Bitcoin fundamentals knowledge base for AI agent training

-- Main categories table
CREATE TABLE IF NOT EXISTS bitcoin_fundamentals_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    priority VARCHAR(20),
    total_subtopics INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Subtopics table
CREATE TABLE IF NOT EXISTS bitcoin_fundamentals_subtopics (
    subtopic_id VARCHAR(10) PRIMARY KEY,
    category_id INTEGER NOT NULL,
    subtopic_name VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) CHECK(priority IN ('High', 'Medium', 'Low')),
    target_qa_pairs INTEGER DEFAULT 30,
    actual_qa_pairs INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES bitcoin_fundamentals_categories(category_id)
);

-- Q&A pairs table
CREATE TABLE IF NOT EXISTS bitcoin_fundamentals_qa_pairs (
    qa_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subtopic_id VARCHAR(10) NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty_level VARCHAR(20) CHECK(difficulty_level IN ('Beginner', 'Intermediate', 'Advanced', 'Expert')),
    question_type VARCHAR(50),
    tags TEXT,
    source_references TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subtopic_id) REFERENCES bitcoin_fundamentals_subtopics(subtopic_id)
);

-- Session tracking table
CREATE TABLE IF NOT EXISTS bitcoin_fundamentals_sessions (
    session_id INTEGER PRIMARY KEY,
    session_name VARCHAR(200) NOT NULL,
    subtopics_covered TEXT,
    total_qa_pairs INTEGER DEFAULT 0,
    status VARCHAR(50) CHECK(status IN ('pending', 'in_progress', 'completed', 'approved')) DEFAULT 'pending',
    assigned_to VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert Categories
INSERT INTO bitcoin_fundamentals_categories (category_id, category_name, description, priority, total_subtopics) VALUES
(1, 'Bitcoin History & Origins', 'Historical development, key events, and foundational moments', 'High', 20),
(2, 'Bitcoin Protocol & Technology', 'Technical architecture, blockchain mechanics, transaction structure', 'High', 25),
(3, 'Mining & Consensus', 'Mining operations, proof-of-work, hash rate, and network security', 'High', 20),
(4, 'Bitcoin Economics & Monetary Policy', 'Supply mechanics, economic theory, valuation models', 'High', 25),
(5, 'Cryptography & Security', 'Cryptographic foundations, hash functions, key security', 'High', 20),
(6, 'Wallets & Key Management', 'Wallet types, backup strategies, custody solutions', 'High', 20),
(7, 'Network & Node Operations', 'Node types, peer-to-peer network, infrastructure', 'Medium', 18),
(8, 'Privacy & Anonymity', 'Privacy techniques, CoinJoin, chain analysis, anonymity sets', 'High', 18),
(9, 'Lightning Network', 'Layer 2 payment channels, routing, liquidity management', 'High', 22),
(10, 'Governance & Development', 'BIPs, development process, consensus mechanisms', 'Medium', 15),
(11, 'Regulation & Legal', 'Global regulations, tax treatment, legal status', 'High', 20),
(12, 'Use Cases & Adoption', 'Real-world applications, institutional adoption, emerging markets', 'High', 18),
(13, 'Layer 2 Solutions & Sidechains', 'Alternative L2 solutions, sidechains, protocol extensions', 'Medium', 12),
(14, 'Bitcoin Culture & Philosophy', 'Community, philosophy, Austrian economics, social aspects', 'Medium', 15),
(15, 'Advanced Topics & Future', 'Edge cases, future developments, advanced concepts', 'Medium', 15);

-- Insert all 250+ subtopics (Category 1: Bitcoin History & Origins)
INSERT INTO bitcoin_fundamentals_subtopics (subtopic_id, category_id, subtopic_name, description, priority) VALUES
('1.1', 1, 'Satoshi Nakamoto Identity', 'Pseudonymous creator, theories, evidence', 'High'),
('1.2', 1, 'Bitcoin Whitepaper Analysis', 'The 9-page paper breakdown, key concepts', 'High'),
('1.3', 1, 'Genesis Block', 'First block, hidden message, significance', 'High'),
('1.4', 1, 'Cypherpunk Movement', 'Predecessors, philosophy, influence', 'Medium'),
('1.5', 1, 'Pre-Bitcoin Digital Cash', 'DigiCash, b-money, bit gold, HashCash', 'Medium'),
('1.6', 1, 'Early Bitcoin (2009-2010)', 'First transactions, pizza day, early adopters', 'High'),
('1.7', 1, 'Bitcoin Forum History', 'BitcoinTalk, early discussions, community formation', 'Medium'),
('1.8', 1, 'First Bitcoin Exchange', 'Mt. Gox origins, early trading', 'Medium'),
('1.9', 1, 'Bitcoin Pizza Transaction', '10,000 BTC for pizza, Laszlo Hanyecz', 'High'),
('1.10', 1, 'Satoshi''s Disappearance', 'Last communications, handover to Gavin', 'Medium'),
('1.11', 1, 'Silk Road Impact', 'Dark web markets, Bitcoin adoption driver', 'Medium'),
('1.12', 1, 'Mt. Gox Collapse', 'Largest exchange hack, 850,000 BTC lost', 'High'),
('1.13', 1, 'Bitcoin Forks History', 'Bitcoin XT, Classic, Unlimited, BCH, BSV', 'High'),
('1.14', 1, 'Blocksize War', 'Scaling debate 2015-2017, big blocks vs small blocks', 'High'),
('1.15', 1, 'SegWit Activation', 'Segregated Witness, scaling solution, adoption', 'High'),
('1.16', 1, 'Lightning Network Launch', 'Layer 2 solution, mainnet deployment', 'Medium'),
('1.17', 1, 'Taproot Upgrade', 'Privacy and smart contract upgrade 2021', 'Medium'),
('1.18', 1, 'Bitcoin Halving Events', '2012, 2016, 2020, 2024 halvings and impacts', 'High'),
('1.19', 1, 'Major Bitcoin Milestones', '$1, $100, $1K, $10K, $69K ATH, ETF approval', 'High'),
('1.20', 1, 'Institutional Adoption Timeline', 'MicroStrategy, Tesla, El Salvador, ETFs', 'High');

-- Category 2: Bitcoin Protocol & Technology (25 subtopics)
INSERT INTO bitcoin_fundamentals_subtopics (subtopic_id, category_id, subtopic_name, description, priority) VALUES
('2.1', 2, 'Blockchain Data Structure', 'Blocks, headers, merkle trees, chain organization', 'High'),
('2.2', 2, 'Proof of Work Mechanism', 'SHA-256, mining difficulty, nonce finding', 'High'),
('2.3', 2, 'Mining Difficulty Adjustment', '2016 block retarget, algorithm, purpose', 'High'),
('2.4', 2, 'Block Time & Confirmation', '10-minute average, 6 confirmations standard', 'High'),
('2.5', 2, 'Block Size & Weight', '1MB limit, SegWit weight units, block capacity', 'Medium'),
('2.6', 2, 'Transaction Structure', 'Inputs, outputs, signatures, scripts', 'High'),
('2.7', 2, 'UTXO Model', 'Unspent transaction outputs, vs account model', 'High'),
('2.8', 2, 'Bitcoin Script Language', 'Stack-based, opcodes, script types', 'Medium'),
('2.9', 2, 'P2PKH Transactions', 'Pay-to-Public-Key-Hash, legacy addresses', 'Medium'),
('2.10', 2, 'P2SH Transactions', 'Pay-to-Script-Hash, multisig enabler', 'Medium'),
('2.11', 2, 'SegWit Transactions', 'Native SegWit, bech32 addresses, witness data', 'High'),
('2.12', 2, 'Taproot Transactions', 'P2TR, Schnorr signatures, MAST', 'Medium'),
('2.13', 2, 'Multisig Wallets', 'M-of-N signatures, security model, use cases', 'High'),
('2.14', 2, 'Timelocks', 'nLockTime, CheckLockTimeVerify, relative timelocks', 'Medium'),
('2.15', 2, 'Replace-by-Fee (RBF)', 'Transaction replacement, fee bumping', 'Medium'),
('2.16', 2, 'Child-Pays-For-Parent', 'CPFP, transaction acceleration', 'Medium'),
('2.17', 2, 'Mempool Mechanics', 'Pending transactions, prioritization, purging', 'High'),
('2.18', 2, 'Transaction Malleability', 'Problem and SegWit solution', 'Medium'),
('2.19', 2, 'Merkle Tree Structure', 'Transaction hashing, SPV proofs', 'Medium'),
('2.20', 2, 'Block Header Anatomy', 'Version, previous hash, merkle root, timestamp, bits, nonce', 'Medium'),
('2.21', 2, 'Coinbase Transaction', 'Block reward, miner payout, extra nonce', 'High'),
('2.22', 2, 'Bitcoin Address Types', 'Legacy, P2SH, bech32, bech32m comparison', 'High'),
('2.23', 2, 'Network Propagation', 'Block relay, compact blocks, transaction broadcast', 'Medium'),
('2.24', 2, 'Consensus Rules', 'Valid blocks, valid transactions, chain selection', 'High'),
('2.25', 2, 'Hard Forks vs Soft Forks', 'Upgrade types, backward compatibility', 'High');

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_subtopic_category ON bitcoin_fundamentals_subtopics(category_id);
CREATE INDEX IF NOT EXISTS idx_subtopic_priority ON bitcoin_fundamentals_subtopics(priority);
CREATE INDEX IF NOT EXISTS idx_qa_subtopic ON bitcoin_fundamentals_qa_pairs(subtopic_id);
CREATE INDEX IF NOT EXISTS idx_qa_difficulty ON bitcoin_fundamentals_qa_pairs(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_session_status ON bitcoin_fundamentals_sessions(status);

-- Create views for common queries
CREATE VIEW IF NOT EXISTS v_category_progress AS
SELECT
    c.category_id,
    c.category_name,
    c.total_subtopics,
    COUNT(DISTINCT s.subtopic_id) as subtopics_with_data,
    SUM(s.actual_qa_pairs) as total_qa_pairs,
    ROUND(AVG(s.actual_qa_pairs), 2) as avg_qa_per_subtopic,
    ROUND(COUNT(DISTINCT s.subtopic_id) * 100.0 / c.total_subtopics, 2) as completion_percentage
FROM bitcoin_fundamentals_categories c
LEFT JOIN bitcoin_fundamentals_subtopics s ON c.category_id = s.category_id
GROUP BY c.category_id, c.category_name, c.total_subtopics;

CREATE VIEW IF NOT EXISTS v_high_priority_incomplete AS
SELECT
    subtopic_id,
    subtopic_name,
    category_id,
    priority,
    target_qa_pairs,
    actual_qa_pairs,
    (target_qa_pairs - actual_qa_pairs) as remaining_qa_pairs
FROM bitcoin_fundamentals_subtopics
WHERE priority = 'High'
AND actual_qa_pairs < target_qa_pairs
ORDER BY (target_qa_pairs - actual_qa_pairs) DESC;

-- Sample query to get overall progress
-- SELECT * FROM v_category_progress ORDER BY category_id;

-- Sample query to get high priority incomplete subtopics
-- SELECT * FROM v_high_priority_incomplete LIMIT 20;

-- Note: Remaining 225 subtopics from categories 3-15 should be inserted similarly
-- This is a partial schema showing the structure. Full INSERT statements for all 250+ subtopics
-- are defined in the accompanying markdown file: BITCOIN_FUNDAMENTALS_DATABASE_SCHEMA.md
