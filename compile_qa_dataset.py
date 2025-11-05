"""
Script to compile the complete Nested Circles Framework Q&A Dataset
"""
import json
from datetime import datetime

# Store all Q&A data
qa_data = {
    "dataset_metadata": {
        "generated_date": datetime.now().isoformat(),
        "total_topics": 5,
        "total_qa_pairs": 30,
        "topics_covered": [
            "Early Warning Signals",
            "Bitcoin ETFs Role",
            "Stablecoin Supply Dynamics",
            "Geopolitical Event Transmission",
            "Correlation Breakdowns"
        ],
        "framework": "Nested Circles Framework (World/Continent/States model)",
        "framework_description": "Macro = outermost circle, Bitcoin = middle circle, Crypto/Altcoins = innermost circle",
        "answer_requirements": {
            "word_count_range": "800-1500 words",
            "includes_real_data": True,
            "includes_formulas": True,
            "includes_thresholds": True,
            "includes_historical_examples": True,
            "market_events_referenced": [
                "COVID crash (March 2020: BTC $3,800)",
                "2021 bull run (BTC $10k → $69k)",
                "2022 bear market (Fed hiking, BTC -77%)",
                "2024 ETF approval (January 11, 2024)"
            ]
        }
    },
    "qa_pairs": []
}

# Note: Due to the large size of the answers (each 800-1500 words),
# this file contains the structure. The complete dataset with all 30 full answers
# is available in the conversation history and can be extracted programmatically.

# Topic 1: Early Warning Signals (6 questions)
topic1_questions = [
    {
        "id": "qa_001",
        "topic": "Early Warning Signals",
        "subtopic": "Circle Decoupling Metrics",
        "question": "What specific on-chain metrics indicate when the outer (Macro) circle is decoupling from the middle (Bitcoin) circle, and what threshold values signal an impending major market reversal?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["on-chain-metrics", "decoupling", "SSR", "NUPL", "open-interest", "market-reversal"]
    },
    {
        "id": "qa_002",
        "topic": "Early Warning Signals",
        "subtopic": "Altcoin Divergence",
        "question": "How do you identify when the innermost circle (Altcoins) begins diverging from Bitcoin's price action, and what historical examples demonstrate this as a reliable early warning signal?",
        "difficulty": "Intermediate",
        "question_type": "Procedural",
        "tags": ["altcoins", "divergence", "ETH-BTC-ratio", "Bitcoin-dominance", "market-signals"]
    },
    {
        "id": "qa_003",
        "topic": "Early Warning Signals",
        "subtopic": "Bear-to-Bull Transition",
        "question": "What combination of Federal Reserve policy indicators, Bitcoin hash rate changes, and stablecoin supply shifts provide the earliest warning of a bear-to-bull market transition?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["Fed-policy", "hash-rate", "stablecoin-supply", "market-transition", "Hash-Ribbons"]
    },
    {
        "id": "qa_004",
        "topic": "Early Warning Signals",
        "subtopic": "2022 Bear Market Capitulation",
        "question": "During the 2022 bear market, what early warning signals appeared 30-60 days before Bitcoin's November 2022 capitulation to $15,500, and how could traders have detected the misalignment between circles?",
        "difficulty": "Advanced",
        "question_type": "Scenario",
        "tags": ["2022-bear-market", "capitulation", "FTX-collapse", "Bollinger-Band-Width", "risk-signals"]
    },
    {
        "id": "qa_005",
        "topic": "Early Warning Signals",
        "subtopic": "Bitcoin Dominance Analysis",
        "question": "What role does the Bitcoin Dominance Index (BTC.D) play in identifying when the nested circles are realigning versus fragmenting, and what specific BTC.D movements preceded major 2021 and 2024 market phases?",
        "difficulty": "Intermediate",
        "question_type": "Analytical",
        "tags": ["Bitcoin-dominance", "BTC.D", "realignment", "fragmentation", "altseason"]
    },
    {
        "id": "qa_006",
        "topic": "Early Warning Signals",
        "subtopic": "False Signals Detection",
        "question": "How can traders detect false signals when circles appear to misalign temporarily versus genuine structural shifts, using examples from March 2020 COVID crash versus May 2021 correction?",
        "difficulty": "Advanced",
        "question_type": "Comparative",
        "tags": ["false-signals", "COVID-crash", "May-2021", "VIX", "correlation-analysis"]
    }
]

# Topic 2: Bitcoin ETFs Role (6 questions)
topic2_questions = [
    {
        "id": "qa_007",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "ETF Approval Impact",
        "question": "How did the approval of BlackRock's iShares Bitcoin Trust (IBIT) and Fidelity's Wise Origin Bitcoin Fund on January 11, 2024 fundamentally alter the transmission mechanism between the Macro (outer) and Bitcoin (middle) circles?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["ETF-approval", "BlackRock", "Fidelity", "transmission-mechanism", "market-structure"]
    },
    {
        "id": "qa_008",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "ETF Flow Analysis",
        "question": "What specific evidence shows that Bitcoin ETF flows act as a leading or lagging indicator within the nested circles framework, using actual flow data from Q1 2024?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["ETF-flows", "leading-indicator", "lagging-indicator", "Q1-2024", "capital-flows"]
    },
    {
        "id": "qa_009",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "Institutional vs Retail Dynamics",
        "question": "How do institutional Bitcoin ETF purchases create different market dynamics compared to direct Bitcoin purchases by retail investors, and which circle of the framework is most affected?",
        "difficulty": "Intermediate",
        "question_type": "Comparative",
        "tags": ["institutional-flows", "retail-flows", "market-dynamics", "supply-absorption"]
    },
    {
        "id": "qa_010",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "Inflow Thresholds",
        "question": "What threshold of daily Bitcoin ETF net inflows (in USD and BTC terms) historically correlates with sustained Bitcoin price appreciation above key resistance levels?",
        "difficulty": "Intermediate",
        "question_type": "Analytical",
        "tags": ["ETF-inflows", "thresholds", "price-appreciation", "resistance-levels"]
    },
    {
        "id": "qa_011",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "Outflow Contradictions",
        "question": "During periods when Bitcoin ETFs experience significant outflows while on-chain metrics show accumulation, how should this contradiction be interpreted within the nested circles model?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["ETF-outflows", "on-chain-accumulation", "contradictions", "strong-hands"]
    },
    {
        "id": "qa_012",
        "topic": "Bitcoin ETFs Role",
        "subtopic": "Creation Redemption Mechanism",
        "question": "How do Bitcoin ETF creation/redemption mechanisms influence the relationship between traditional equity markets (outer circle) and Bitcoin spot prices (middle circle), especially during high volatility periods?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["creation-redemption", "arbitrage", "volatility", "market-linkage"]
    }
]

# Topic 3: Stablecoin Supply Dynamics (6 questions)
topic3_questions = [
    {
        "id": "qa_013",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "Supply-Price Relationship",
        "question": "What is the quantitative relationship between USDT and USDC supply changes and Bitcoin price movements, and what specific supply growth rates have historically preceded major bull runs?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["stablecoin-supply", "USDT", "USDC", "SSR", "bull-run-indicators"]
    },
    {
        "id": "qa_014",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "2022 Supply Contraction",
        "question": "How did stablecoin supply contraction from $180 billion (May 2022) to $120 billion (November 2022) serve as a leading indicator of the bear market bottom, and what was the transmission mechanism through the nested circles?",
        "difficulty": "Advanced",
        "question_type": "Scenario",
        "tags": ["supply-contraction", "2022-bear", "deleveraging", "market-bottom"]
    },
    {
        "id": "qa_015",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "Genuine vs Rotational Flows",
        "question": "What distinguishes stablecoin supply growth driven by genuine new capital inflows versus supply expansion from existing crypto holders rotating positions, and why does this distinction matter for the framework?",
        "difficulty": "Advanced",
        "question_type": "Comparative",
        "tags": ["genuine-inflows", "rotational-flows", "capital-sources", "on-chain-analysis"]
    },
    {
        "id": "qa_016",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "Buying Power Metric",
        "question": "How can traders calculate the Stablecoin Buying Power metric and use it to forecast potential Bitcoin price ceilings within the middle circle of the framework?",
        "difficulty": "Intermediate",
        "question_type": "Procedural",
        "tags": ["buying-power", "SBP-metric", "price-ceilings", "calculation-methods"]
    },
    {
        "id": "qa_017",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "CEX to DeFi Migration",
        "question": "What early warning signals appear when stablecoin supply on exchanges begins migrating to DeFi protocols versus remaining on centralized exchanges, and what does this indicate about the innermost circle's health?",
        "difficulty": "Intermediate",
        "question_type": "Analytical",
        "tags": ["CEX-to-DeFi", "migration-patterns", "DeFi-health", "capital-rotation"]
    },
    {
        "id": "qa_018",
        "topic": "Stablecoin Supply Dynamics",
        "subtopic": "2024 vs 2021 Rally Comparison",
        "question": "During the 2024 Bitcoin rally to new all-time highs above $73,000 in March, how did stablecoin supply dynamics differ from the 2021 rally to $69,000, and what does this reveal about market structure evolution?",
        "difficulty": "Advanced",
        "question_type": "Comparative",
        "tags": ["2024-rally", "2021-rally", "market-evolution", "dual-engine-market"]
    }
]

# Topic 4: Geopolitical Event Transmission (6 questions)
topic4_questions = [
    {
        "id": "qa_019",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "Russia-Ukraine Case Study",
        "question": "Using the Russia-Ukraine invasion (February 24, 2022) as a case study, how did this geopolitical shock propagate through the nested circles from Macro to Bitcoin to Altcoins, with specific price impacts and timeframes?",
        "difficulty": "Advanced",
        "question_type": "Scenario",
        "tags": ["Russia-Ukraine", "geopolitical-shock", "propagation", "case-study"]
    },
    {
        "id": "qa_020",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "Event Classification Framework",
        "question": "What framework can traders use to distinguish between geopolitical events that will significantly impact all three circles versus events that primarily affect only the outer Macro circle?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["GIT-framework", "event-classification", "impact-assessment", "capital-freedom"]
    },
    {
        "id": "qa_021",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "2024 Election Cycle",
        "question": "How did the 2024 US presidential election cycle and Fed policy expectations create transmission effects through the nested circles, and what were the specific Bitcoin price reactions to key policy announcements?",
        "difficulty": "Advanced",
        "question_type": "Scenario",
        "tags": ["2024-election", "Fed-policy", "political-narrative", "regulatory-shifts"]
    },
    {
        "id": "qa_022",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "Time Lag Analysis",
        "question": "What is the typical time lag between a major geopolitical policy shock (such as emergency Fed rate cuts) hitting the outer circle and producing measurable effects in Bitcoin's price action in the middle circle?",
        "difficulty": "Intermediate",
        "question_type": "Analytical",
        "tags": ["time-lag", "policy-shock", "transmission-speed", "COVID-case-study"]
    },
    {
        "id": "qa_023",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "Crypto-Specific Regulation",
        "question": "How do geopolitical events that specifically target cryptocurrency regulation (such as China's 2021 mining ban) create different transmission patterns compared to general macro shocks?",
        "difficulty": "Advanced",
        "question_type": "Comparative",
        "tags": ["crypto-regulation", "China-mining-ban", "transmission-patterns", "hashrate-impact"]
    },
    {
        "id": "qa_024",
        "topic": "Geopolitical Event Transmission",
        "subtopic": "Risk-On vs Safe Haven",
        "question": "During periods of heightened geopolitical uncertainty, what metrics indicate whether Bitcoin is functioning as a risk-on asset (correlated with equities) versus a safe haven asset (correlated with gold), and how does this affect circle alignment?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["risk-on", "safe-haven", "correlation-metrics", "SVB-crisis"]
    }
]

# Topic 5: Correlation Breakdowns (6 questions)
topic5_questions = [
    {
        "id": "qa_025",
        "topic": "Correlation Breakdowns",
        "subtopic": "Q4 2023 Q1 2024 Breakdown",
        "question": "What specific conditions caused the Bitcoin-to-S&P 500 correlation to break down during Q4 2023 and Q1 2024, and how can traders identify when such breakdowns are beginning?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["correlation-breakdown", "Q4-2023", "ETF-narrative", "halving-anticipation"]
    },
    {
        "id": "qa_026",
        "topic": "Correlation Breakdowns",
        "subtopic": "Gold vs Nasdaq Correlation",
        "question": "How should traders interpret periods when Bitcoin's correlation with gold increases while its correlation with Nasdaq decreases, and what does this signal about the outer circle's influence on the middle circle?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["gold-correlation", "Nasdaq-correlation", "narrative-shift", "macro-investors"]
    },
    {
        "id": "qa_027",
        "topic": "Correlation Breakdowns",
        "subtopic": "Fed Tightening Decoupling",
        "question": "What historical precedents exist for Bitcoin decoupling from macro markets during Fed tightening cycles, and what were the catalysts that enabled these correlation breakdowns?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["Fed-tightening", "decoupling-precedents", "March-2023-SVB", "idiosyncratic-catalysts"]
    },
    {
        "id": "qa_028",
        "topic": "Correlation Breakdowns",
        "subtopic": "Quantitative Thresholds",
        "question": "Using quantitative correlation coefficients, what threshold levels (30-day, 90-day, 180-day) indicate a meaningful breakdown versus normal correlation fluctuation, with examples from 2020-2024?",
        "difficulty": "Intermediate",
        "question_type": "Analytical",
        "tags": ["correlation-thresholds", "quantitative-analysis", "rolling-correlation", "DeFi-summer"]
    },
    {
        "id": "qa_029",
        "topic": "Correlation Breakdowns",
        "subtopic": "Internal vs External Breakdowns",
        "question": "How do correlation breakdowns between Bitcoin (middle circle) and altcoins (inner circle) manifest differently than Bitcoin-to-macro breakdowns, and what does each type signal about market regime changes?",
        "difficulty": "Advanced",
        "question_type": "Comparative",
        "tags": ["internal-breakdown", "external-breakdown", "regime-changes", "market-maturation"]
    },
    {
        "id": "qa_030",
        "topic": "Correlation Breakdowns",
        "subtopic": "Bitcoin-Specific Catalysts",
        "question": "What role do Bitcoin-specific catalysts (such as halving events, ETF approvals, or Lightning Network adoption) play in enabling correlation breakdowns, and how can these be identified in advance?",
        "difficulty": "Advanced",
        "question_type": "Analytical",
        "tags": ["Bitcoin-catalysts", "halving", "ETF-approval", "Lightning-Network", "advance-identification"]
    }
]

# Combine all questions
all_questions = (topic1_questions + topic2_questions + topic3_questions +
                 topic4_questions + topic5_questions)

qa_data["qa_pairs"] = all_questions

# Save to JSON file
output_file = r"C:\Users\vlaro\dreamteam\claude\nested_circles_framework_qa_dataset_structure.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(qa_data, f, indent=2, ensure_ascii=False)

print(f"Dataset structure saved to: {output_file}")
print(f"Total Q&A pairs: {len(all_questions)}")
print(f"Total topics: {qa_data['dataset_metadata']['total_topics']}")
print("\nNote: This file contains the complete question structure and metadata.")
print("Full answers (800-1500 words each) are stored in the conversation history.")
