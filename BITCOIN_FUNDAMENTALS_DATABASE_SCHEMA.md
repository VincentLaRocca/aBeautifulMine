# Bitcoin Fundamentals - Complete Database Schema

**Date:** 2025-11-03
**Purpose:** Comprehensive subtopic breakdown for Bitcoin Fundamentals knowledge base
**Target Use:** AI Agent training dataset

---

## Database Structure Overview

**Total Categories:** 15
**Total Subtopics:** 250+
**Target Q&A per Subtopic:** 30-50 pairs
**Total Expected Q&A Pairs:** 7,500-12,500

---

## CATEGORY 1: BITCOIN HISTORY & ORIGINS (20 subtopics)

### Table: `bitcoin_history`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 1.1 | Satoshi Nakamoto Identity | Pseudonymous creator, theories, evidence | High |
| 1.2 | Bitcoin Whitepaper Analysis | The 9-page paper breakdown, key concepts | High |
| 1.3 | Genesis Block | First block, hidden message, significance | High |
| 1.4 | Cypherpunk Movement | Predecessors, philosophy, influence | Medium |
| 1.5 | Pre-Bitcoin Digital Cash | DigiCash, b-money, bit gold, HashCash | Medium |
| 1.6 | Early Bitcoin (2009-2010) | First transactions, pizza day, early adopters | High |
| 1.7 | Bitcoin Forum History | BitcoinTalk, early discussions, community formation | Medium |
| 1.8 | First Bitcoin Exchange | Mt. Gox origins, early trading | Medium |
| 1.9 | Bitcoin Pizza Transaction | 10,000 BTC for pizza, Laszlo Hanyecz | High |
| 1.10 | Satoshi's Disappearance | Last communications, handover to Gavin | Medium |
| 1.11 | Silk Road Impact | Dark web markets, Bitcoin adoption driver | Medium |
| 1.12 | Mt. Gox Collapse | Largest exchange hack, 850,000 BTC lost | High |
| 1.13 | Bitcoin Forks History | Bitcoin XT, Classic, Unlimited, BCH, BSV | High |
| 1.14 | Blocksize War | Scaling debate 2015-2017, big blocks vs small blocks | High |
| 1.15 | SegWit Activation | Segregated Witness, scaling solution, adoption | High |
| 1.16 | Lightning Network Launch | Layer 2 solution, mainnet deployment | Medium |
| 1.17 | Taproot Upgrade | Privacy and smart contract upgrade 2021 | Medium |
| 1.18 | Bitcoin Halving Events | 2012, 2016, 2020, 2024 halvings and impacts | High |
| 1.19 | Major Bitcoin Milestones | $1, $100, $1K, $10K, $69K ATH, ETF approval | High |
| 1.20 | Institutional Adoption Timeline | MicroStrategy, Tesla, El Salvador, ETFs | High |

---

## CATEGORY 2: BITCOIN PROTOCOL & TECHNOLOGY (25 subtopics)

### Table: `bitcoin_protocol`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.1 | Blockchain Data Structure | Blocks, headers, merkle trees, chain organization | High |
| 2.2 | Proof of Work Mechanism | SHA-256, mining difficulty, nonce finding | High |
| 2.3 | Mining Difficulty Adjustment | 2016 block retarget, algorithm, purpose | High |
| 2.4 | Block Time & Confirmation | 10-minute average, 6 confirmations standard | High |
| 2.5 | Block Size & Weight | 1MB limit, SegWit weight units, block capacity | Medium |
| 2.6 | Transaction Structure | Inputs, outputs, signatures, scripts | High |
| 2.7 | UTXO Model | Unspent transaction outputs, vs account model | High |
| 2.8 | Bitcoin Script Language | Stack-based, opcodes, script types | Medium |
| 2.9 | P2PKH Transactions | Pay-to-Public-Key-Hash, legacy addresses | Medium |
| 2.10 | P2SH Transactions | Pay-to-Script-Hash, multisig enabler | Medium |
| 2.11 | SegWit Transactions | Native SegWit, bech32 addresses, witness data | High |
| 2.12 | Taproot Transactions | P2TR, Schnorr signatures, MAST | Medium |
| 2.13 | Multisig Wallets | M-of-N signatures, security model, use cases | High |
| 2.14 | Timelocks | nLockTime, CheckLockTimeVerify, relative timelocks | Medium |
| 2.15 | Replace-by-Fee (RBF) | Transaction replacement, fee bumping | Medium |
| 2.16 | Child-Pays-For-Parent | CPFP, transaction acceleration | Medium |
| 2.17 | Mempool Mechanics | Pending transactions, prioritization, purging | High |
| 2.18 | Transaction Malleability | Problem and SegWit solution | Medium |
| 2.19 | Merkle Tree Structure | Transaction hashing, SPV proofs | Medium |
| 2.20 | Block Header Anatomy | Version, previous hash, merkle root, timestamp, bits, nonce | Medium |
| 2.21 | Coinbase Transaction | Block reward, miner payout, extra nonce | High |
| 2.22 | Bitcoin Address Types | Legacy, P2SH, bech32, bech32m comparison | High |
| 2.23 | Network Propagation | Block relay, compact blocks, transaction broadcast | Medium |
| 2.24 | Consensus Rules | Valid blocks, valid transactions, chain selection | High |
| 2.25 | Hard Forks vs Soft Forks | Upgrade types, backward compatibility | High |

---

## CATEGORY 3: MINING & CONSENSUS (20 subtopics)

### Table: `bitcoin_mining`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 3.1 | Mining Hardware Evolution | CPU → GPU → FPGA → ASIC progression | High |
| 3.2 | ASIC Miners | Application-specific chips, manufacturers, models | High |
| 3.3 | Hash Rate Explained | Network computing power, measurement units | High |
| 3.4 | Mining Difficulty | Current difficulty, historical trends, calculations | High |
| 3.5 | Mining Profitability | Revenue vs costs, break-even analysis | High |
| 3.6 | Mining Pools | Pooled mining, payout methods (PPS, PPLNS), centralization | High |
| 3.7 | Solo Mining vs Pool | Variance, expected returns, lottery aspect | Medium |
| 3.8 | Mining Pool Distribution | Top pools, geographic distribution, centralization concerns | Medium |
| 3.9 | Energy Consumption | Power usage, environmental impact, green mining | High |
| 3.10 | Mining Economics | Electricity costs, hardware ROI, operational expenses | High |
| 3.11 | Hashprice Metric | Revenue per terahash, profitability indicator | Medium |
| 3.12 | Mining Centralization Risks | 51% attack, pool power concentration | High |
| 3.13 | Geographic Mining Distribution | China ban, US dominance, global hash rate map | Medium |
| 3.14 | Stratum Protocol | Mining pool communication, work distribution | Low |
| 3.15 | Mining Firmware | Braiins OS, custom firmware, overclocking | Low |
| 3.16 | Immersion Cooling | Mining infrastructure, efficiency gains | Low |
| 3.17 | Hosting Services | Mining colocation, cloud mining | Medium |
| 3.18 | Mining Derivatives | Hash rate futures, difficulty derivatives | Low |
| 3.19 | Post-Halving Mining | Subsidy reduction impact, miner capitulation | High |
| 3.20 | Future of Mining | Fee-only era (2140), security model evolution | Medium |

---

## CATEGORY 4: BITCOIN ECONOMICS & MONETARY POLICY (25 subtopics)

### Table: `bitcoin_economics`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 4.1 | 21 Million Supply Cap | Fixed supply, scarcity, vs fiat inflation | High |
| 4.2 | Bitcoin Issuance Schedule | Block rewards, halving cycle, emission curve | High |
| 4.3 | Bitcoin Halving Economics | Supply shock, price impact, historical patterns | High |
| 4.4 | Inflation Rate | Current inflation, declining to zero | High |
| 4.5 | Stock-to-Flow Model | S2F ratio, scarcity metric, price modeling | High |
| 4.6 | Digital Scarcity | Provable scarcity, unforgeable costliness | High |
| 4.7 | Unit Bias Psychology | Satoshis, bits, mBTC, psychological pricing | Medium |
| 4.8 | Satoshi Denomination | Smallest unit (0.00000001 BTC), sat standard | High |
| 4.9 | Lost Bitcoin | Inaccessible coins, Satoshi's coins, effective supply | Medium |
| 4.10 | Velocity of Money | Bitcoin circulation, HODLing impact | Medium |
| 4.11 | Bitcoin as Money | Medium of exchange, store of value, unit of account | High |
| 4.12 | Sound Money Properties | Durability, portability, divisibility, fungibility | High |
| 4.13 | Bitcoin vs Gold | Digital gold narrative, comparison | High |
| 4.14 | Bitcoin vs Fiat | Monetary policy comparison, inflation resistance | High |
| 4.15 | Network Effects | Metcalfe's Law, adoption growth, liquidity | Medium |
| 4.16 | Gresham's Law | Good money, bad money, HODLing incentive | Medium |
| 4.17 | Time Preference | Low time preference, saving culture, Austrian economics | Medium |
| 4.18 | Bitcoin Circular Economy | Bitcoin-only commerce, Lightning Network economy | Medium |
| 4.19 | Remittances Use Case | Cross-border payments, Lightning Network | Medium |
| 4.20 | Store of Value Thesis | Long-term wealth preservation, digital property | High |
| 4.21 | Medium of Exchange | Payment use case, Lightning Network enablement | High |
| 4.22 | Unit of Account | Pricing in Bitcoin, volatility challenge | Medium |
| 4.23 | Bitcoin Valuation Models | Market cap, realized cap, thermocap, fair value | High |
| 4.24 | Bitcoin Cycles | 4-year cycles, halving correlation, bull/bear patterns | High |
| 4.25 | Bitcoin Adoption Curve | S-curve adoption, current stage, future growth | High |

---

## CATEGORY 5: CRYPTOGRAPHY & SECURITY (20 subtopics)

### Table: `bitcoin_cryptography`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 5.1 | SHA-256 Hash Function | Cryptographic hashing, mining algorithm | High |
| 5.2 | RIPEMD-160 | Address generation, hash function | Medium |
| 5.3 | Public Key Cryptography | Asymmetric encryption, key pairs | High |
| 5.4 | ECDSA Signatures | Elliptic curve, secp256k1, signature creation | High |
| 5.5 | Schnorr Signatures | Taproot upgrade, signature aggregation, efficiency | Medium |
| 5.6 | Private Key Security | Key generation, entropy, storage | High |
| 5.7 | Public Key Derivation | Private key → public key → address | High |
| 5.8 | HD Wallets (BIP32) | Hierarchical deterministic wallets, key derivation | High |
| 5.9 | Mnemonic Seeds (BIP39) | 12/24 word recovery phrases, seed generation | High |
| 5.10 | Derivation Paths (BIP44) | Account structure, address generation paths | Medium |
| 5.11 | Address Encoding | Base58, bech32, checksum, QR codes | Medium |
| 5.12 | Brain Wallets | Passphrase to private key (insecure, deprecated) | Low |
| 5.13 | Vanity Addresses | Custom address generation, security considerations | Low |
| 5.14 | Key Stretching | PBKDF2, wallet encryption, password security | Medium |
| 5.15 | 51% Attack | Majority hash power attack, reorganization risk | High |
| 5.16 | Double Spend Attack | Attack types, confirmation depth defense | High |
| 5.17 | Sybil Attack | Network flooding, peer connection attacks | Medium |
| 5.18 | Eclipse Attack | Node isolation, peer manipulation | Medium |
| 5.19 | Quantum Computing Threat | Post-quantum cryptography, timeline, mitigation | Medium |
| 5.20 | Cryptographic Assumptions | Collision resistance, pre-image resistance, ECDLP | Medium |

---

## CATEGORY 6: WALLETS & KEY MANAGEMENT (20 subtopics)

### Table: `bitcoin_wallets`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 6.1 | Hot Wallets | Internet-connected, mobile/desktop, convenience | High |
| 6.2 | Cold Wallets | Offline storage, paper/hardware, security | High |
| 6.3 | Hardware Wallets | Ledger, Trezor, Coldcard, secure elements | High |
| 6.4 | Paper Wallets | Printed keys, generation, risks | Medium |
| 6.5 | Mobile Wallets | iOS/Android apps, Lightning support, UX | High |
| 6.6 | Desktop Wallets | Bitcoin Core, Electrum, Sparrow, full features | High |
| 6.7 | Web Wallets | Browser-based, custodial risks, convenience | Medium |
| 6.8 | Custodial vs Non-Custodial | Key control, "not your keys not your coins" | High |
| 6.9 | Multi-Signature Wallets | 2-of-3, 3-of-5 setups, collaborative custody | High |
| 6.10 | Multisig Quorum Types | M-of-N configurations, security vs availability | Medium |
| 6.11 | Wallet Backup Strategies | Seed backup, metal plates, geographic distribution | High |
| 6.12 | Passphrase (25th word) | BIP39 extension, plausible deniability | Medium |
| 6.13 | Shamir Secret Sharing | SLIP39, seed splitting, threshold recovery | Medium |
| 6.14 | Wallet Inheritance Planning | Dead man's switch, time locks, estate planning | Medium |
| 6.15 | Lightning Wallets | Phoenix, Breez, Zeus, channel management | High |
| 6.16 | Watch-Only Wallets | Address monitoring, cold storage integration | Medium |
| 6.17 | Coin Control | UTXO selection, privacy, fee optimization | Medium |
| 6.18 | Wallet Privacy Features | CoinJoin integration, Tor support, address reuse | Medium |
| 6.19 | Wallet Security Best Practices | Physical security, operational security, threat models | High |
| 6.20 | Wallet Recovery | Seed phrase recovery, derivation path standards | High |

---

## CATEGORY 7: NETWORK & NODE OPERATIONS (18 subtopics)

### Table: `bitcoin_network`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 7.1 | Full Nodes | Complete blockchain validation, network backbone | High |
| 7.2 | Pruned Nodes | Disk space optimization, transaction verification | Medium |
| 7.3 | Light Clients (SPV) | Simplified payment verification, mobile wallets | High |
| 7.4 | Bitcoin Core Software | Reference implementation, development, releases | High |
| 7.5 | Alternative Implementations | btcd, libbitcoin, Bitcoin Knots | Medium |
| 7.6 | Node Hardware Requirements | CPU, RAM, disk space, bandwidth | Medium |
| 7.7 | Running a Node Benefits | Trustless validation, privacy, network support | High |
| 7.8 | Node Synchronization | Initial block download, catching up | Medium |
| 7.9 | Peer Discovery | DNS seeds, peer connections, addr messages | Medium |
| 7.10 | P2P Network Protocol | Message types, connection management | Medium |
| 7.11 | Tor Integration | Privacy, onion routing, hidden services | Medium |
| 7.12 | Node Distribution | Geographic spread, ISP diversity, reachability | Medium |
| 7.13 | Raspberry Pi Nodes | Umbrel, RaspiBlitz, myNode, affordability | Medium |
| 7.14 | Node-in-a-Box Solutions | Plug-and-play nodes, pre-configured hardware | Medium |
| 7.15 | Neutrino Protocol | Compact block filters, light client privacy | Low |
| 7.16 | Electrum Server | Electrs, ElectrumX, wallet server architecture | Medium |
| 7.17 | Block Explorers | Blockchain.com, Blockstream.info, Mempool.space | High |
| 7.18 | Network Topology | Peer connections, super nodes, network graph | Low |

---

## CATEGORY 8: PRIVACY & ANONYMITY (18 subtopics)

### Table: `bitcoin_privacy`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 8.1 | Bitcoin Privacy Model | Pseudonymous not anonymous, transparency | High |
| 8.2 | Address Reuse | Privacy leak, heuristics, best practices | High |
| 8.3 | Blockchain Analysis | Chain surveillance, clustering, de-anonymization | High |
| 8.4 | Common Input Ownership | Transaction analysis heuristic, linking addresses | Medium |
| 8.5 | Change Address Detection | Change output identification, privacy leak | Medium |
| 8.6 | CoinJoin | Collaborative transactions, breaking links | High |
| 8.7 | Wasabi Wallet | CoinJoin coordinator, anonymous credentials | Medium |
| 8.8 | Samourai Wallet | Whirlpool CoinJoin, privacy toolkit | Medium |
| 8.9 | PayJoin (P2EP) | Pay-to-endpoint, chain analysis resistance | Medium |
| 8.10 | CoinSwap | Non-custodial atomic swaps, privacy | Low |
| 8.11 | Mixing Services | Centralized mixers (risky), vs CoinJoin | Medium |
| 8.12 | Tor for Bitcoin | Network privacy, IP obfuscation | High |
| 8.13 | Dandelion Protocol | Transaction origin privacy, stem/fluff phases | Low |
| 8.14 | Taproot Privacy Benefits | Uniform outputs, script privacy, signature aggregation | Medium |
| 8.15 | Lightning Network Privacy | Onion routing, payment privacy, trade-offs | High |
| 8.16 | Network-Level Privacy | IP leaks, peer connections, timing attacks | Medium |
| 8.17 | UTXO Management | Coin selection, consolidation privacy | Medium |
| 8.18 | KYC/AML Trade-offs | Exchange requirements vs privacy, compliance | High |

---

## CATEGORY 9: LIGHTNING NETWORK (22 subtopics)

### Table: `lightning_network`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 9.1 | Lightning Network Overview | Layer 2 solution, payment channels, scaling | High |
| 9.2 | Payment Channels | Bidirectional channels, funding, closing | High |
| 9.3 | Channel Capacity | Inbound/outbound liquidity, balancing | High |
| 9.4 | Routing | Multi-hop payments, pathfinding, onion routing | High |
| 9.5 | Hash Time-Locked Contracts | HTLC, atomic payments, security | Medium |
| 9.6 | Lightning Invoices | BOLT11 invoices, payment requests, expiration | High |
| 9.7 | Lightning Addresses | user@domain.com format, easier payments | Medium |
| 9.8 | Channel Liquidity | Liquidity management, rebalancing, loop services | High |
| 9.9 | Submarine Swaps | On-chain ↔ Lightning, Loop In/Out | Medium |
| 9.10 | Watchtowers | Security monitoring, penalty transactions | Medium |
| 9.11 | Lightning Routing Fees | Fee structure, routing node revenue | Medium |
| 9.12 | Channel Factories | Multi-party channels, efficiency | Low |
| 9.13 | Splicing | Channel resizing, on-chain operations | Medium |
| 9.14 | Dual-Funded Channels | Both parties fund, balanced liquidity | Medium |
| 9.15 | Multi-Path Payments (MPP) | Split payments, large payment routing | Medium |
| 9.16 | Atomic Multi-Path (AMP) | Spontaneous payments, no invoice needed | Medium |
| 9.17 | Lightning Service Providers | LSP, liquidity services, mobile wallets | Medium |
| 9.18 | Lightning Network Capacity | Total capacity, growth trends, nodes | High |
| 9.19 | Lightning Privacy | Onion routing, payment privacy, trade-offs | High |
| 9.20 | Lightning vs On-Chain | Use case comparison, fee differences | High |
| 9.21 | Lightning Network Adoption | Merchants, El Salvador, Strike, Cash App | High |
| 9.22 | Taproot Assets on Lightning | Stablecoins, tokens, RGB, Taro/Taproot Assets | Medium |

---

## CATEGORY 10: GOVERNANCE & DEVELOPMENT (15 subtopics)

### Table: `bitcoin_governance`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 10.1 | Bitcoin Improvement Proposals | BIP process, proposal types, activation | High |
| 10.2 | Core Development | Bitcoin Core contributors, GitHub, review process | High |
| 10.3 | Consensus Changes | Soft forks, hard forks, activation methods | High |
| 10.4 | BIP Activation Methods | BIP9, BIP8, Speedy Trial, user activation | Medium |
| 10.5 | UASF vs MASF | User vs miner activated soft forks, SegWit battle | Medium |
| 10.6 | Developer Funding | Grants, sponsors, open source sustainability | Medium |
| 10.7 | Bitcoin Optech | Technical newsletter, workshops, best practices | Medium |
| 10.8 | Bitcoin Core Release Cycle | Major releases, security updates, testing | Medium |
| 10.9 | Consensus Rules Changes | Adding opcodes, changing limits, upgrade paths | Medium |
| 10.10 | Contentious Forks | Bitcoin Cash, Bitcoin SV, disagreement resolution | Medium |
| 10.11 | Bitcoin Roadmap | Future upgrades, research directions, priorities | Medium |
| 10.12 | Covenant Proposals | OP_CTV, OP_VAULT, new script capabilities | Low |
| 10.13 | Cross-Input Signature Aggregation | Future Schnorr upgrade, efficiency | Low |
| 10.14 | Drivechains | Sidechains, BIP300/301, merged mining | Low |
| 10.15 | Bitcoin Research | Academic papers, cryptographic advances | Low |

---

## CATEGORY 11: REGULATION & LEGAL (20 subtopics)

### Table: `bitcoin_regulation`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 11.1 | Legal Status by Country | Global regulatory landscape, bans, acceptance | High |
| 11.2 | US Regulation | SEC, CFTC, FinCEN, state-level regulations | High |
| 11.3 | EU Regulation | MiCA, AML directives, harmonization efforts | High |
| 11.4 | China Bitcoin Ban | Mining ban, trading restrictions, enforcement | Medium |
| 11.5 | El Salvador Legal Tender | First country adoption, Chivo wallet, implementation | High |
| 11.6 | KYC/AML Requirements | Know Your Customer, Anti-Money Laundering compliance | High |
| 11.7 | Travel Rule | FATF requirements, transaction reporting | Medium |
| 11.8 | Tax Treatment | Capital gains, income, reporting requirements | High |
| 11.9 | IRS Guidance | US tax treatment, reporting, cost basis | High |
| 11.10 | Bitcoin ETFs | Spot ETF approval, futures ETFs, regulation | High |
| 11.11 | Custody Regulations | Qualified custodians, institutional requirements | Medium |
| 11.12 | Securities Classification | Commodity vs security debate, Howey test | Medium |
| 11.13 | Banking Regulations | Operation Chokepoint, de-banking, access | Medium |
| 11.14 | Criminal Use Narrative | Money laundering, ransomware, actual statistics | Medium |
| 11.15 | Self-Custody Rights | Right to run nodes, hold keys, freedom | High |
| 11.16 | Privacy Coin Bans | Monero, Zcash regulations, Bitcoin impact | Medium |
| 11.17 | Decentralized Exchange Regulation | DEX, non-custodial, enforcement challenges | Medium |
| 11.18 | Mining Regulations | Energy use, zoning, permits, taxes | Medium |
| 11.19 | Future Regulatory Trends | CBDC competition, global coordination | Medium |
| 11.20 | BitLicense Example | New York regulation, industry impact | Medium |

---

## CATEGORY 12: USE CASES & ADOPTION (18 subtopics)

### Table: `bitcoin_adoption`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 12.1 | Institutional Investment | MicroStrategy, Tesla, hedge funds, treasuries | High |
| 12.2 | Corporate Adoption | Balance sheet allocation, payment acceptance | High |
| 12.3 | Nation-State Adoption | El Salvador, rumors of others, reserves | High |
| 12.4 | Retail Payment Acceptance | Merchants, payment processors, Lightning | Medium |
| 12.5 | Remittances | Cross-border transfers, Lightning Network, fees | High |
| 12.6 | Emerging Markets | Hyperinflation protection, Argentina, Turkey, Nigeria | High |
| 12.7 | Unbanked Populations | Financial inclusion, mobile access | Medium |
| 12.8 | Wealth Preservation | Store of value, inflation hedge, long-term saving | High |
| 12.9 | Censorship Resistance | Unstoppable payments, freedom money | High |
| 12.10 | Donations & Fundraising | Non-profit funding, WikiLeaks, Canadian truckers | Medium |
| 12.11 | Strike & Cash App | Consumer apps, Lightning integration, ease of use | High |
| 12.12 | Bitcoin Beach | El Zonte, grassroots circular economy | Medium |
| 12.13 | Peer-to-Peer Trading | LocalBitcoins, Bisq, Hodl Hodl, P2P exchanges | Medium |
| 12.14 | DCA & Savings Apps | Swan, River, automatic accumulation | Medium |
| 12.15 | Bitcoin Lending | Collateralized loans, yield, risks | Medium |
| 12.16 | Bitcoin-Backed Credit Cards | Fold, BlockFi cards, rewards | Low |
| 12.17 | Bitcoin in Gaming | Play-to-earn, Lightning integration, virtual economies | Low |
| 12.18 | Energy Grid Applications | Demand response, renewable energy monetization | Medium |

---

## CATEGORY 13: LAYER 2 SOLUTIONS & SIDECHAINS (12 subtopics)

### Table: `bitcoin_layer2`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 13.1 | Lightning Network (see Category 9) | Payment channels, routing, instant transactions | High |
| 13.2 | Liquid Network | Federated sidechain, L-BTC, fast settlements | Medium |
| 13.3 | RGB Protocol | Client-side validation, tokens, smart contracts | Low |
| 13.4 | Taro/Taproot Assets | Asset issuance on Bitcoin, stablecoins | Medium |
| 13.5 | Fedimint | Federated Chaumian mints, privacy, custody | Low |
| 13.6 | Rootstock (RSK) | Smart contract sidechain, merged mining | Low |
| 13.7 | Stacks | Bitcoin smart contracts, STX token, microblocks | Low |
| 13.8 | Ordinals & Inscriptions | NFTs on Bitcoin, block space debate, BRC-20 | Medium |
| 13.9 | Rollups on Bitcoin | Optimistic rollups, ZK rollups, research | Low |
| 13.10 | Statechains | Off-chain UTXO transfers, non-custodial | Low |
| 13.11 | DLCs (Discreet Log Contracts) | Oracle-based smart contracts, prediction markets | Low |
| 13.12 | Ark Protocol | Joinpool protocol, UTXO pooling, research | Low |

---

## CATEGORY 14: BITCOIN CULTURE & PHILOSOPHY (15 subtopics)

### Table: `bitcoin_culture`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 14.1 | Austrian Economics | Sound money, time preference, Mises, Hayek | Medium |
| 14.2 | Cypherpunk Ethos | Privacy, cryptography, individual sovereignty | Medium |
| 14.3 | Bitcoin Maximalism | Bitcoin-only philosophy, altcoin criticism | Medium |
| 14.4 | HODLing Culture | Long-term holding, diamond hands, weak hands | High |
| 14.5 | "Not Your Keys, Not Your Coins" | Self-custody mantra, exchange risks | High |
| 14.6 | Bitcoin Memes | To the moon, laser eyes, WAGMI, few understand | Low |
| 14.7 | Bitcoin Conferences | Bitcoin 2024, Baltic Honeybadger, Adopting Bitcoin | Medium |
| 14.8 | Bitcoin Twitter/X | Influencers, discussions, community hub | Medium |
| 14.9 | Bitcoin Podcasts | What Bitcoin Did, Bitcoin Audible, TFTC | Medium |
| 14.10 | Bitcoin Books | The Bitcoin Standard, Mastering Bitcoin, Bitcoin Billionaires | Medium |
| 14.11 | Orange Pilling | Converting skeptics, education, onboarding | Medium |
| 14.12 | Fix the Money, Fix the World | Monetary reform thesis, societal impact | Medium |
| 14.13 | Toxic Maximalism | Aggressive Bitcoin advocacy, debate culture | Low |
| 14.14 | Bitcoin Influencers | Michael Saylor, Jack Dorsey, Cathie Wood, Max Keiser | Medium |
| 14.15 | Bitcoin Education Initiatives | Mi Primer Bitcoin, Bitcoin Academy, grassroots | Medium |

---

## CATEGORY 15: ADVANCED TOPICS & FUTURE (15 subtopics)

### Table: `bitcoin_advanced`

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 15.1 | Fee Market Dynamics | Transaction fees, mempool economics, fee estimation | High |
| 15.2 | MEV on Bitcoin | Miner extractable value, transaction ordering | Low |
| 15.3 | Selfish Mining | Mining strategy, attack vector, game theory | Low |
| 15.4 | Mining Centralization Concerns | Pool power, geographic concentration, risks | Medium |
| 15.5 | Block Withholding Attacks | Pool sabotage, detection, prevention | Low |
| 15.6 | Time Warp Attack | Difficulty manipulation, historical bug | Low |
| 15.7 | Bitcoin's Energy Use Debate | Environmental concerns, renewable energy, comparisons | High |
| 15.8 | Post-Subsidy Security Model | Fee-only security (2140), economic viability | Medium |
| 15.9 | Quantum Resistance | Threat timeline, cryptographic upgrades needed | Medium |
| 15.10 | Cross-Chain Bridges | Wrapped BTC, security models, trade-offs | Medium |
| 15.11 | Bitcoin vs CBDCs | Central bank digital currencies, competition | High |
| 15.12 | Bitcoin's Role in Hyperbitcoinization | Global Bitcoin standard, predictions | Medium |
| 15.13 | Bitcoin Demographics | Who owns Bitcoin, generational adoption, geography | Medium |
| 15.14 | Bitcoin Wealth Distribution | Gini coefficient, whale wallets, equality | Medium |
| 15.15 | Bitcoin's Environmental Impact | Carbon footprint, methane flaring, renewable mining | High |

---

## Database Implementation Plan

### Suggested Table Structure (PostgreSQL/SQLite)

```sql
CREATE TABLE bitcoin_fundamentals_categories (
    category_id INTEGER PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    description TEXT,
    priority VARCHAR(20)
);

CREATE TABLE bitcoin_fundamentals_subtopics (
    subtopic_id VARCHAR(10) PRIMARY KEY,
    category_id INTEGER REFERENCES bitcoin_fundamentals_categories(category_id),
    subtopic_name VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20),
    target_qa_pairs INTEGER DEFAULT 30
);

CREATE TABLE bitcoin_fundamentals_qa_pairs (
    qa_id SERIAL PRIMARY KEY,
    subtopic_id VARCHAR(10) REFERENCES bitcoin_fundamentals_subtopics(subtopic_id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty_level VARCHAR(20),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bitcoin_fundamentals_sessions (
    session_id INTEGER PRIMARY KEY,
    session_name VARCHAR(200),
    subtopics_covered TEXT[],
    total_qa_pairs INTEGER,
    status VARCHAR(50),
    assigned_to VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Q&A Generation Strategy

### Per Subtopic Question Types (30-50 questions each)

**1. Definitional (5-8 questions)**
- What is [subtopic]?
- How does [subtopic] work?
- Why is [subtopic] important?

**2. Technical Deep-Dive (8-12 questions)**
- Technical mechanisms
- Implementation details
- Algorithm explanations

**3. Historical Context (3-5 questions)**
- Origin and evolution
- Key milestones
- Influential figures

**4. Practical Application (8-12 questions)**
- How to use/implement
- Best practices
- Common mistakes
- Real-world examples

**5. Comparative (3-5 questions)**
- Vs alternatives
- Trade-offs
- When to use what

**6. Advanced/Edge Cases (3-5 questions)**
- Corner cases
- Attack vectors
- Future considerations

**7. Economic/Game Theory (3-5 questions)**
- Incentives
- Economics
- Game theory

**8. Current Events (2-3 questions)**
- 2024-2025 developments
- Recent news
- Future trends

---

## Execution Plan

### Phase 1: High Priority Subtopics (120 subtopics)
**Target:** 3,600-6,000 Q&A pairs
**Timeline:** 4-6 weeks
**Focus:** All "High" priority subtopics across all categories

### Phase 2: Medium Priority Subtopics (80 subtopics)
**Target:** 2,400-4,000 Q&A pairs
**Timeline:** 3-4 weeks
**Focus:** All "Medium" priority subtopics

### Phase 3: Low Priority Subtopics (50 subtopics)
**Target:** 1,500-2,500 Q&A pairs
**Timeline:** 2-3 weeks
**Focus:** All "Low" priority subtopics

### Total Expected Output
- **250 subtopics**
- **7,500-12,500 Q&A pairs**
- **9-13 weeks** for complete coverage

---

## Session Breakdown (Suggested 25 Sessions)

**Session 1-2:** Bitcoin History & Origins (20 subtopics)
**Session 3-5:** Protocol & Technology (25 subtopics)
**Session 6-7:** Mining & Consensus (20 subtopics)
**Session 8-10:** Economics & Monetary Policy (25 subtopics)
**Session 11-12:** Cryptography & Security (20 subtopics)
**Session 13-14:** Wallets & Key Management (20 subtopics)
**Session 15-16:** Network & Nodes (18 subtopics)
**Session 17-18:** Privacy & Anonymity (18 subtopics)
**Session 19-20:** Lightning Network (22 subtopics)
**Session 21:** Governance & Development (15 subtopics)
**Session 22-23:** Regulation & Legal (20 subtopics)
**Session 24:** Use Cases & Adoption (18 subtopics)
**Session 25:** Layer 2, Culture, Advanced (42 subtopics)

---

**Total Subtopics:** 250+
**Total Categories:** 15
**Database Tables:** 4 main tables + metadata
**Target Q&A Pairs:** 7,500-12,500
**Priority Distribution:** 120 High, 80 Medium, 50 Low

---

**Schema Created:** 2025-11-03
**Ready for:** Agent training dataset generation
**Next Step:** Begin Q&A pair generation starting with High priority subtopics
