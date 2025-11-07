"""
WeMineHope Library - Subject Generator
=======================================

Breaks subjects into subtopics for batch mining.

Takes a high-level subject and generates the complete structure
of subtopics needed to mine it exhaustively.

Author: Team Claude
Date: 2025-11-06
For the Greater Good of All
"""

import json
from pathlib import Path
from typing import List, Dict, Optional


class SubjectGenerator:
    """
    Generates complete subtopic structures for subjects.

    This is the bridge between "I want to mine [SUBJECT]" and
    having a complete list of batches to process.
    """

    def __init__(self):
        self.subject_templates = self._load_templates()

    def _load_templates(self) -> Dict:
        """Load pre-defined subject templates"""
        return {
            "crypto_technology": self._crypto_template,
            "blockchain_development": self._blockchain_dev_template,
            "decentralized_finance": self._defi_template,
            "institutional_finance": self._institutional_template,
            "medical_knowledge": self._medical_template,
            "legal_research": self._legal_template,
        }

    def generate_subtopics(self,
                          subject_type: str,
                          custom_subtopics: List[str] = None) -> List[str]:
        """
        Generate exhaustive subtopic list for a subject

        Args:
            subject_type: Type of subject (uses template)
            custom_subtopics: Optional custom subtopic list

        Returns:
            Complete list of subtopics to mine
        """
        if custom_subtopics:
            return custom_subtopics

        if subject_type in self.subject_templates:
            return self.subject_templates[subject_type]()

        raise ValueError(f"Unknown subject type: {subject_type}")

    def _crypto_template(self) -> List[str]:
        """Cryptocurrency technology subtopics"""
        return [
            # Technical Indicators (220 total)
            "Moving Averages", "RSI", "MACD", "Bollinger Bands", "Fibonacci Retracement",
            "Volume Analysis", "OBV", "ADX", "Stochastic Oscillator", "Ichimoku Cloud",
            "Parabolic SAR", "ATR", "CCI", "Williams %R", "ROC",
            "Money Flow Index", "Chaikin Money Flow", "Volume Weighted Average Price",
            "Accumulation/Distribution", "Ease of Movement",
            # ... (expand to 220 indicators)

            # Blockchain Fundamentals
            "Consensus Mechanisms", "Proof of Work", "Proof of Stake", "Byzantine Fault Tolerance",
            "Mining", "Hashing", "Cryptography", "Digital Signatures", "Public Key Infrastructure",

            # Cryptocurrencies
            "Bitcoin", "Ethereum", "Altcoins", "Stablecoins", "CBDCs",

            # DeFi
            "Decentralized Exchanges", "Lending Protocols", "Yield Farming", "Liquidity Pools",
            "Automated Market Makers", "Flash Loans", "Governance Tokens",

            # NFTs & Web3
            "NFT Standards", "NFT Marketplaces", "Digital Art", "Gaming NFTs", "Metaverse",

            # Layer 2 & Scaling
            "Lightning Network", "Rollups", "Sidechains", "State Channels", "Plasma",

            # Security
            "Smart Contract Audits", "Vulnerabilities", "Best Practices", "Cold Storage",

            # Trading
            "Order Types", "Market Making", "Arbitrage", "Risk Management", "Portfolio Management",

            # Regulation & Compliance
            "KYC/AML", "Securities Law", "Tax Implications", "Global Regulations",
        ]

    def _blockchain_dev_template(self) -> List[str]:
        """Blockchain development subtopics"""
        return [
            # Smart Contract Development
            "Solidity Basics", "Solidity Advanced", "Vyper", "Rust (Solana)", "Move (Aptos)",
            "Contract Patterns", "Security Patterns", "Gas Optimization",

            # Development Tools
            "Hardhat", "Truffle", "Foundry", "Remix", "Web3.js", "Ethers.js",
            "Testing Frameworks", "Deployment Strategies",

            # dApp Development
            "Frontend Integration", "Wallet Integration", "IPFS", "The Graph",
            "Oracle Integration", "Event Handling",

            # Protocol Development
            "Tokenomics Design", "Governance Design", "Economic Models",
            "Protocol Security", "Upgradability Patterns",

            # Layer 1 Development
            "Bitcoin Script", "Ethereum EVM", "Solana Programs", "Cosmos SDK",
            "Polkadot Parachains", "Cardano Plutus",

            # Testing & Auditing
            "Unit Testing", "Integration Testing", "Formal Verification",
            "Security Auditing", "Bug Bounties",
        ]

    def _defi_template(self) -> List[str]:
        """Decentralized finance subtopics"""
        return [
            # DEX Protocols
            "Uniswap V2", "Uniswap V3", "Sushiswap", "Curve", "Balancer",
            "1inch", "Pancakeswap", "Trader Joe",

            # Lending Protocols
            "Aave", "Compound", "MakerDAO", "Liquity", "Alchemix",

            # Derivatives
            "Perpetual Protocols", "Options Protocols", "Synthetic Assets",
            "Leveraged Tokens", "Prediction Markets",

            # Yield Strategies
            "Yield Farming", "Liquidity Mining", "Staking", "Auto-compounding",
            "Yield Aggregators", "Vault Strategies",

            # Stablecoins
            "DAI", "USDC", "USDT", "Frax", "UST/Luna", "Algorithmic Stablecoins",

            # Cross-chain
            "Bridges", "Cross-chain DEXs", "Multi-chain Protocols",

            # Risk Management
            "Impermanent Loss", "Smart Contract Risk", "Oracle Risk",
            "Liquidation Risk", "Systemic Risk",
        ]

    def _institutional_template(self) -> List[str]:
        """Institutional finance subtopics"""
        return [
            # Custody Solutions
            "Institutional Custody", "Multi-sig Solutions", "Cold Storage",
            "Insurance Solutions", "Regulatory Compliance",

            # Trading Infrastructure
            "Prime Brokerage", "OTC Trading", "Algorithmic Trading",
            "Market Making", "Liquidity Provision",

            # Derivatives & Hedging
            "Futures", "Options", "Swaps", "Structured Products",
            "Risk Management", "Portfolio Hedging",

            # Asset Management
            "Fund Structures", "Portfolio Construction", "Performance Attribution",
            "Risk Metrics", "Reporting Requirements",

            # Compliance & Regulation
            "AML/KYC", "Best Execution", "Trade Surveillance",
            "Regulatory Reporting", "Audit Requirements",

            # Market Microstructure
            "Order Flow", "Market Impact", "Transaction Cost Analysis",
            "Liquidity Analysis", "Price Discovery",
        ]

    def _medical_template(self) -> List[str]:
        """Medical knowledge subtopics"""
        return [
            # Diagnostics
            "Clinical Examination", "Laboratory Tests", "Imaging Techniques",
            "Differential Diagnosis", "Diagnostic Algorithms",

            # Treatment Protocols
            "Pharmacology", "Surgical Procedures", "Physical Therapy",
            "Rehabilitation", "Preventive Medicine",

            # Medical Specialties
            "Cardiology", "Neurology", "Oncology", "Pediatrics", "Geriatrics",
            "Emergency Medicine", "Psychiatry", "Radiology",

            # Disease Management
            "Chronic Disease Management", "Acute Care", "Pain Management",
            "Palliative Care", "Preventive Care",

            # Medical Ethics
            "Patient Rights", "Informed Consent", "End of Life Care",
            "Resource Allocation", "Medical Research Ethics",
        ]

    def _legal_template(self) -> List[str]:
        """Legal research subtopics"""
        return [
            # Corporate Law
            "Corporate Governance", "Mergers & Acquisitions", "Securities Law",
            "Contract Law", "Employment Law",

            # Intellectual Property
            "Patents", "Trademarks", "Copyright", "Trade Secrets", "Licensing",

            # Litigation
            "Civil Procedure", "Evidence", "Discovery", "Trial Practice", "Appeals",

            # Regulatory Compliance
            "Environmental Law", "Healthcare Compliance", "Financial Regulations",
            "Data Privacy", "Antitrust",

            # International Law
            "International Trade", "Treaty Law", "Jurisdiction", "Arbitration",
        ]

    def create_subject_config(self,
                            subject_id: str,
                            subject_name: str,
                            subject_type: str,
                            description: str,
                            priority: int = 5,
                            target_pairs: int = 30000,
                            category: str = "General",
                            custom_subtopics: List[str] = None) -> Dict:
        """
        Create a complete subject configuration

        Returns:
            Dict ready to add to subject queue
        """
        subtopics = self.generate_subtopics(subject_type, custom_subtopics)

        return {
            "subject_id": subject_id,
            "subject_name": subject_name,
            "description": description,
            "subject_type": subject_type,
            "category": category,
            "priority": priority,
            "subtopics": subtopics,
            "target_pairs": target_pairs,
            "estimated_pairs_per_subtopic": target_pairs // len(subtopics) if subtopics else 0
        }

    def save_config(self, config: Dict, output_path: str):
        """Save subject configuration to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"[SUCCESS] Subject config saved: {output_path}")
        print(f"  Subject: {config['subject_name']}")
        print(f"  Subtopics: {len(config['subtopics'])}")
        print(f"  Target pairs: {config['target_pairs']:,}")


# CLI Interface
def main():
    import sys

    if len(sys.argv) < 2:
        print("WeMineHope Library - Subject Generator")
        print("\nUsage:")
        print("  python subject_generator.py list-templates      # List available templates")
        print("  python subject_generator.py generate <type>     # Generate subtopics")
        print("\nAvailable templates:")
        generator = SubjectGenerator()
        for template in generator.subject_templates.keys():
            print(f"  - {template}")
        return

    generator = SubjectGenerator()
    command = sys.argv[1]

    if command == 'list-templates':
        print("\nAvailable Subject Templates:")
        for template_name in generator.subject_templates.keys():
            print(f"  - {template_name}")

    elif command == 'generate':
        if len(sys.argv) < 3:
            print("Error: Specify subject type")
            return

        subject_type = sys.argv[2]
        try:
            subtopics = generator.generate_subtopics(subject_type)
            print(f"\nSubtopics for '{subject_type}':")
            print(f"Total: {len(subtopics)}")
            print("\nFirst 10 subtopics:")
            for i, topic in enumerate(subtopics[:10], 1):
                print(f"  {i}. {topic}")
            print(f"\n... and {len(subtopics) - 10} more")

        except ValueError as e:
            print(f"Error: {e}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
