# Cryptocurrency Fundamentals - Complete Master Database Schema

**Date:** 2025-11-03
**Purpose:** Comprehensive cryptocurrency knowledge base covering Bitcoin, Ethereum, Layer 1s, DeFi, Stablecoins, and emerging projects
**Scope:** ALL major cryptocurrencies and protocols
**Target Use:** AI Agent comprehensive crypto education

---

## Database Structure Overview

**Total Blockchain Categories:** 10 major sections
**Total Cryptocurrencies/Protocols Covered:** 50+
**Total Subtopics:** 800+
**Target Q&A per Subtopic:** 30-50 pairs
**Total Expected Q&A Pairs:** 24,000-40,000

---

## SECTION 1: BITCOIN FUNDAMENTALS (263 subtopics)

### See: `BITCOIN_FUNDAMENTALS_DATABASE_SCHEMA.md`

**Summary:**
- 15 categories (History, Protocol, Mining, Economics, etc.)
- 263 subtopics
- ~7,890-13,150 Q&A pairs

**Note:** Bitcoin section already complete. Reference existing schema.

---

## SECTION 2: ETHEREUM FUNDAMENTALS (120 subtopics)

### Category 2.1: Ethereum History & Origins (15 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.1.1 | Vitalik Buterin & Founding Team | Origins, founding team, early vision | High |
| 2.1.2 | Ethereum Whitepaper | World computer concept, smart contracts | High |
| 2.1.3 | The DAO Hack | 2016 hack, hard fork, Ethereum vs ETC split | High |
| 2.1.4 | Ethereum Classic Split | Immutability vs pragmatism, ETC continuation | Medium |
| 2.1.5 | ICO Boom 2017 | ERC-20 token standard, fundraising explosion | High |
| 2.1.6 | CryptoKitties Congestion | First NFT craze, network scaling issues | Medium |
| 2.1.7 | Ethereum 2.0 Announcement | Proof-of-Stake vision, Beacon Chain roadmap | High |
| 2.1.8 | DeFi Summer 2020 | Yield farming, Uniswap, Compound, explosion | High |
| 2.1.9 | NFT Boom 2021 | BAYC, CryptoPunks, OpenSea, cultural moment | High |
| 2.1.10 | The Merge 2022 | Proof-of-Stake transition, energy reduction | High |
| 2.1.11 | Shanghai Upgrade | Staking withdrawals enabled, impact | High |
| 2.1.12 | Dencun Upgrade | Blob space, EIP-4844, L2 cost reduction | High |
| 2.1.13 | Ethereum Roadmap Evolution | The Surge, Scourge, Verge, Purge, Splurge | Medium |
| 2.1.14 | Major Ethereum Milestones | Price milestones, adoption markers | Medium |
| 2.1.15 | Ethereum Foundation | Governance, funding, research direction | Medium |

### Category 2.2: Ethereum Protocol & Technology (25 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.2.1 | Ethereum Virtual Machine (EVM) | Turing-complete, gas model, execution | High |
| 2.2.2 | Smart Contracts | Solidity, contract deployment, immutability | High |
| 2.2.3 | Account Model | EOA vs Contract Accounts, state management | High |
| 2.2.4 | Gas Mechanism | Gas price, gas limit, gwei, fee market | High |
| 2.2.5 | EIP-1559 Fee Structure | Base fee, priority fee, burn mechanism | High |
| 2.2.6 | Transaction Types | Legacy, EIP-2930, EIP-1559 transactions | Medium |
| 2.2.7 | Block Structure | Block header, receipts, state roots | Medium |
| 2.2.8 | Ethereum State | World state, account state, storage | Medium |
| 2.2.9 | Merkle Patricia Trie | State storage, data structure | Medium |
| 2.2.10 | Ethereum Clients | Geth, Nethermind, Besu, Erigon | Medium |
| 2.2.11 | Execution vs Consensus Layer | Client diversity, dual-layer architecture | High |
| 2.2.12 | Ethereum Nodes | Full nodes, archive nodes, light clients | High |
| 2.2.13 | MEV (Maximal Extractable Value) | Front-running, sandwich attacks, flashbots | High |
| 2.2.14 | Flashbots | MEV mitigation, block building, PBS | Medium |
| 2.2.15 | Account Abstraction (ERC-4337) | Smart contract wallets, gas abstraction | High |
| 2.2.16 | Precompiles | Built-in contracts, elliptic curve operations | Low |
| 2.2.17 | Ethereum Storage | Hot storage, cold storage, state bloat | Medium |
| 2.2.18 | Events & Logs | Event emission, log filtering, indexing | Medium |
| 2.2.19 | ABI (Application Binary Interface) | Contract interaction, encoding/decoding | Medium |
| 2.2.20 | Ethereum JSON-RPC | API specification, node communication | Medium |
| 2.2.21 | Ethereum Improvement Proposals (EIPs) | EIP process, Core, Networking, Interface, ERC | High |
| 2.2.22 | EVM Opcodes | Operation codes, stack operations | Low |
| 2.2.23 | Solidity Language | Contract programming, security patterns | High |
| 2.2.24 | Vyper Language | Alternative to Solidity, Pythonic syntax | Medium |
| 2.2.25 | Ethereum Upgrades Process | Hard forks, network upgrades, coordination | High |

### Category 2.3: Proof-of-Stake & Consensus (20 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.3.1 | Ethereum Staking Overview | 32 ETH requirement, validator duties | High |
| 2.3.2 | Beacon Chain | Consensus layer, PoS coordination | High |
| 2.3.3 | Validators | Attestations, proposals, duties, rewards | High |
| 2.3.4 | Staking Rewards & Penalties | APR calculation, slashing conditions | High |
| 2.3.5 | Slashing Mechanism | Double signing, downtime penalties | High |
| 2.3.6 | Inactivity Leak | Long-term offline penalties, finality | Medium |
| 2.3.7 | Epochs & Slots | Time structure, 12-second slots | Medium |
| 2.3.8 | Committees | Random validator selection, attestations | Medium |
| 2.3.9 | Finality | Casper FFG, justified, finalized epochs | Medium |
| 2.3.10 | Sync Committees | Light client support, 512 validators | Medium |
| 2.3.11 | Validator Queue | Activation queue, exit queue, churn limit | High |
| 2.3.12 | Staking Pools | Lido, Rocket Pool, centralized exchanges | High |
| 2.3.13 | Liquid Staking | stETH, rETH, derivatives, DeFi integration | High |
| 2.3.14 | Solo Staking | Running own validator, hardware requirements | High |
| 2.3.15 | Staking-as-a-Service | Coinbase, Kraken, professional validators | Medium |
| 2.3.16 | MEV-Boost | Block building marketplace, relays | Medium |
| 2.3.17 | Proposer-Builder Separation (PBS) | Block construction separation, censorship resistance | Medium |
| 2.3.18 | Validator Effectiveness | Attestation performance, missed duties | Medium |
| 2.3.19 | Withdrawal Credentials | 0x00 vs 0x01, Shanghai upgrade | High |
| 2.3.20 | Staking Economics | Total staked, staking ratio, yield dynamics | High |

### Category 2.4: Ethereum Economics (15 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.4.1 | ETH Supply Dynamics | No cap, issuance, burn, net inflation/deflation | High |
| 2.4.2 | EIP-1559 Burn Mechanism | ETH destruction, deflationary pressure | High |
| 2.4.3 | Ethereum Issuance | Staking rewards, issuance rate, reduction from PoW | High |
| 2.4.4 | Ultra Sound Money Narrative | Deflationary ETH, vs Bitcoin fixed supply | High |
| 2.4.5 | ETH as Money | Ether's monetary properties, store of value | High |
| 2.4.6 | ETH as Gas | Utility token, transaction fees, network access | High |
| 2.4.7 | ETH as Collateral | DeFi usage, MakerDAO, lending protocols | High |
| 2.4.8 | Triple Point Asset | Store of value + utility + yield | Medium |
| 2.4.9 | Minimum Viable Issuance | Optimal staking rate, security economics | Medium |
| 2.4.10 | ETH Valuation Models | Fee revenue, P/F ratio, DCF models | Medium |
| 2.4.11 | ETH/BTC Ratio | Flippening narrative, ratio trading | High |
| 2.4.12 | Network Effects | Developer activity, dApp ecosystem, liquidity | Medium |
| 2.4.13 | Ethereum vs Competitors | L1 competition, market share, TVL | High |
| 2.4.14 | Institutional ETH Adoption | ETH ETFs, corporate treasuries, validators | High |
| 2.4.15 | Ethereum Economic Security | Cost to attack, staked value, security budget | Medium |

### Category 2.5: ERC Token Standards (15 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.5.1 | ERC-20 Fungible Tokens | Standard interface, transfer, approve, allowance | High |
| 2.5.2 | ERC-721 NFTs | Non-fungible tokens, unique IDs, ownership | High |
| 2.5.3 | ERC-1155 Multi-Token | Semi-fungible, gaming, batch operations | High |
| 2.5.4 | ERC-777 Advanced Tokens | Hooks, operators, backward compatible | Low |
| 2.5.5 | ERC-4626 Tokenized Vaults | Yield-bearing token standard, DeFi integration | Medium |
| 2.5.6 | ERC-2981 NFT Royalties | On-chain royalty standard, creator fees | Medium |
| 2.5.7 | ERC-4337 Account Abstraction | Smart contract wallets, gas sponsorship | High |
| 2.5.8 | ERC-5192 Soul-Bound Tokens | Non-transferable NFTs, identity, credentials | Medium |
| 2.5.9 | ERC-6551 Token-Bound Accounts | NFTs owning assets, composability | Medium |
| 2.5.10 | ERC-3525 Semi-Fungible Tokens | Advanced SFT standard, financial instruments | Low |
| 2.5.11 | Token Security | Reentrancy, overflow, approval exploits | High |
| 2.5.12 | Token Upgradability | Proxy patterns, transparent vs UUPS | Medium |
| 2.5.13 | Token Governance | Voting tokens, delegation, governance | High |
| 2.5.14 | Wrapped Tokens | WETH, wrapped assets, cross-chain tokens | High |
| 2.5.15 | Token Launches | Fair launches, airdrops, liquidity bootstrapping | Medium |

### Category 2.6: Ethereum Layer 2 Ecosystem (20 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.6.1 | Layer 2 Scaling Overview | Rollups, sidechains, state channels | High |
| 2.6.2 | Optimistic Rollups | Fraud proofs, 7-day withdrawal, Optimism/Arbitrum | High |
| 2.6.3 | ZK-Rollups | Validity proofs, instant finality, zkSync/Starknet | High |
| 2.6.4 | Arbitrum | Optimistic rollup, ecosystem, Arbitrum One/Nova | High |
| 2.6.5 | Optimism | OP Stack, Superchain, governance, OP token | High |
| 2.6.6 | Base (Coinbase L2) | OP Stack, Coinbase integration, adoption | High |
| 2.6.7 | zkSync | zkEVM, native account abstraction, Era upgrade | High |
| 2.6.8 | Starknet | Cairo language, ZK-STARKs, scalability | Medium |
| 2.6.9 | Polygon zkEVM | Ethereum-equivalent ZK rollup, Polygon 2.0 | High |
| 2.6.10 | Scroll | zkEVM, bytecode-level compatibility | Medium |
| 2.6.11 | Linea | ConsenSys zkEVM, EVM equivalence | Medium |
| 2.6.12 | Mantle | Modular L2, MNT token, BitDAO | Medium |
| 2.6.13 | Blast | Native yield L2, points program | Medium |
| 2.6.14 | Mode Network | OP Stack L2, DeFi focus | Low |
| 2.6.15 | Metis | Decentralized sequencer, hybrid rollup | Low |
| 2.6.16 | EIP-4844 (Proto-Danksharding) | Blob space, L2 cost reduction, data availability | High |
| 2.6.17 | L2 Bridges | Canonical bridges, third-party, security models | High |
| 2.6.18 | L2 Sequencers | Centralization concerns, decentralization roadmaps | Medium |
| 2.6.19 | L2 Data Availability | Blob storage, calldata, off-chain DA | Medium |
| 2.6.20 | Cross-L2 Interoperability | Shared liquidity, cross-rollup messaging | Medium |

### Category 2.7: Ethereum DeFi Ecosystem (10 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 2.7.1 | Uniswap Protocol | AMM model, V2, V3, V4 evolution | High |
| 2.7.2 | Aave Protocol | Lending/borrowing, flash loans, GHO stablecoin | High |
| 2.7.3 | MakerDAO & DAI | Decentralized stablecoin, CDP system, governance | High |
| 2.7.4 | Curve Finance | Stablecoin AMM, veCRV model, yield optimization | High |
| 2.7.5 | Lido Finance | Liquid staking leader, stETH, governance | High |
| 2.7.6 | Compound Finance | Money market, algorithmic interest rates | High |
| 2.7.7 | Balancer | Weighted pools, composable stable pools | Medium |
| 2.7.8 | Convex Finance | Curve yield booster, vlCVX, tokenomics | Medium |
| 2.7.9 | Yearn Finance | Yield aggregator, vaults, strategies | Medium |
| 2.7.10 | 1inch Network | DEX aggregator, routing, limit orders | Medium |

---

## SECTION 3: LAYER 1 BLOCKCHAINS (150 subtopics)

### Category 3.1: Solana (30 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 3.1.1 | Solana Overview & History | Anatoly Yakovenko, founding, vision | High |
| 3.1.2 | Proof of History (PoH) | Timestamp consensus, innovation | High |
| 3.1.3 | Solana Architecture | Tower BFT, Gulf Stream, Turbine, Sealevel | High |
| 3.1.4 | Solana Performance | 65,000 TPS claims, block times, throughput | High |
| 3.1.5 | Solana Programming Model | Rust, programs, accounts, instructions | High |
| 3.1.6 | SPL Token Standard | Solana's token standard, Token-2022 | High |
| 3.1.7 | Solana Validators | Staking, validator economics, requirements | High |
| 3.1.8 | Solana Network Outages | Downtime incidents, causes, fixes | High |
| 3.1.9 | SOL Token Economics | Inflation, staking rewards, burn | High |
| 3.1.10 | Solana DeFi Ecosystem | Jupiter, Raydium, Marinade, Kamino | High |
| 3.1.11 | Solana NFT Ecosystem | Magic Eden, Tensor, compressed NFTs | Medium |
| 3.1.12 | Solana Mobile | Saga phone, dApp Store, mobile-first | Medium |
| 3.1.13 | Solana vs Ethereum | Performance, decentralization trade-offs | High |
| 3.1.14 | Firedancer | Jump Crypto validator client, performance | Medium |
| 3.1.15 | Solana MEV | Jito, block building, MEV on Solana | Medium |
| 3.1.16 | Phantom Wallet | Leading Solana wallet, features | Medium |
| 3.1.17 | Solana RPC Nodes | Infrastructure, Helius, QuickNode | Medium |
| 3.1.18 | Solana State Compression | Compressed NFTs, data efficiency | Medium |
| 3.1.19 | Solana Priority Fees | Fee market, transaction prioritization | Medium |
| 3.1.20 | Solana Developers | Ecosystem growth, Breakpoint conference | Medium |
| 3.1.21 | Jupiter Exchange | DEX aggregator, JUP token, perps | High |
| 3.1.22 | Marinade Finance | Liquid staking, mSOL, DeFi integration | Medium |
| 3.1.23 | Jito | MEV infrastructure, JTO token, liquid staking | Medium |
| 3.1.24 | Solana Blinks & Actions | Transaction links, social integration | Medium |
| 3.1.25 | Solana Pay | Payment standard, merchant adoption | Medium |
| 3.1.26 | Solana's Monolithic Approach | vs Modular blockchains, philosophy | Medium |
| 3.1.27 | Solana Network Upgrades | Major upgrades, SIMD proposals | Medium |
| 3.1.28 | Solana Adoption Metrics | Active users, transaction volume, TVL | High |
| 3.1.29 | Solana Institutional Support | Grayscale, VanEck, ETF prospects | Medium |
| 3.1.30 | Solana Future Roadmap | Scaling plans, upcoming features | Medium |

### Category 3.2: Cardano (20 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 3.2.1 | Cardano Overview | Charles Hoskinson, academic approach, peer review | High |
| 3.2.2 | Ouroboros Proof-of-Stake | Research-based PoS, provably secure | High |
| 3.2.3 | Cardano Development Phases | Byron, Shelley, Goguen, Basho, Voltaire | High |
| 3.2.4 | ADA Token Economics | Max supply, staking rewards, treasury | High |
| 3.2.5 | Cardano Staking | Delegation, stake pools, no lockup | High |
| 3.2.6 | Plutus Smart Contracts | Functional programming, Haskell-based | Medium |
| 3.2.7 | EUTXO Model | Extended UTXO, parallel processing | Medium |
| 3.2.8 | Hydra Scaling | State channels, head protocol | Medium |
| 3.2.9 | Mithril | Stake-based signatures, light clients | Low |
| 3.2.10 | Cardano DeFi | Minswap, SundaeSwap, Liqwid | Medium |
| 3.2.11 | Cardano NFTs | CNFT ecosystem, native tokens | Medium |
| 3.2.12 | Project Catalyst | Decentralized funding, governance | Medium |
| 3.2.13 | IOHK & Cardano Foundation | Development entities, governance | Medium |
| 3.2.14 | Marlowe | Financial contracts DSL, DeFi focus | Low |
| 3.2.15 | Cardano Native Tokens | First-class tokens, no smart contracts needed | Medium |
| 3.2.16 | Cardano vs Ethereum | Philosophical differences, trade-offs | Medium |
| 3.2.17 | Cardano Adoption | Real-world use cases, Africa focus | Medium |
| 3.2.18 | Djed Stablecoin | Algorithmic stablecoin, COTI partnership | Low |
| 3.2.19 | Cardano Upgrades | Hard fork combinator, smooth upgrades | Medium |
| 3.2.20 | Cardano Roadmap | Future developments, scaling plans | Medium |

### Category 3.3: Avalanche (20 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 3.3.1 | Avalanche Overview | Emin Gün Sirer, Team Rocket, founding | High |
| 3.3.2 | Avalanche Consensus | Snowman, DAG-based, sub-second finality | High |
| 3.3.3 | Primary Network (3 Chains) | X-Chain, C-Chain, P-Chain architecture | High |
| 3.3.4 | C-Chain (Contract Chain) | EVM-compatible, smart contracts, DeFi | High |
| 3.3.5 | Subnets | Application-specific blockchains, customization | High |
| 3.3.6 | AVAX Token Economics | Capped supply, staking, burning | High |
| 3.3.7 | Avalanche Staking | Validators, delegators, 2000 AVAX minimum | Medium |
| 3.3.8 | Avalanche DeFi | Trader Joe, Benqi, Aave deployment | Medium |
| 3.3.9 | Avalanche Warp Messaging | Native cross-subnet communication | Medium |
| 3.3.10 | Avalanche vs Ethereum | Performance comparison, ecosystem | Medium |
| 3.3.11 | Gaming Subnets | DeFi Kingdoms subnet, gaming focus | Low |
| 3.3.12 | Institutional Subnets | Permissioned subnets, enterprise adoption | Medium |
| 3.3.13 | Avalanche Bridge | Cross-chain bridging, Wormhole integration | Medium |
| 3.3.14 | Core Wallet | Official wallet, subnet management | Low |
| 3.3.15 | Avalanche Rush | Liquidity mining program, ecosystem growth | Low |
| 3.3.16 | Avalanche Multiverse | $290M incentive program, subnet growth | Medium |
| 3.3.17 | Avalanche Adoption | Enterprise partnerships, real-world use | Medium |
| 3.3.18 | Ava Labs Development | Company structure, funding, roadmap | Medium |
| 3.3.19 | HyperSDK | High-performance blockchain framework | Low |
| 3.3.20 | Avalanche Future Vision | Subnet scaling, institutional adoption | Medium |

### Category 3.4: Other Major L1s (80 subtopics - 20 each)

**Polkadot** (20 subtopics):
- Relay Chain, Parachains, DOT economics, Governance, Cross-chain messaging, Substrate framework, etc.

**Cosmos** (20 subtopics):
- IBC protocol, ATOM token, Cosmos SDK, Tendermint, Cosmos Hub, Application-specific chains, etc.

**Near Protocol** (20 subtopics):
- Nightshade sharding, Aurora EVM, NEAR token, Rainbow Bridge, Account model, etc.

**Algorand** (20 subtopics):
- Pure PoS, ALGO economics, Silvio Micali, State proofs, DeFi ecosystem, etc.

---

## SECTION 4: ORACLES & DATA (40 subtopics)

### Category 4.1: Chainlink (25 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 4.1.1 | Chainlink Overview | Decentralized oracles, founding, Sergey Nazarov | High |
| 4.1.2 | Oracle Problem | Off-chain data, trust issues, centralization risks | High |
| 4.1.3 | Chainlink Architecture | Node operators, data aggregation, reputation | High |
| 4.1.4 | LINK Token Economics | Staking, payments, tokenomics 2.0 | High |
| 4.1.5 | Chainlink Price Feeds | Most used oracle, DeFi integration, update mechanisms | High |
| 4.1.6 | Chainlink VRF | Verifiable random function, gaming, NFTs | High |
| 4.1.7 | Chainlink Automation | Keeper network, automated execution | High |
| 4.1.8 | Chainlink Proof of Reserve | Asset backing verification, stablecoin reserves | Medium |
| 4.1.9 | Chainlink Functions | Serverless oracle computations, API calls | Medium |
| 4.1.10 | Chainlink CCIP | Cross-Chain Interoperability Protocol, messaging | High |
| 4.1.11 | Chainlink Staking | v0.2 staking, security guarantees | High |
| 4.1.12 | Chainlink Node Operators | Running nodes, requirements, revenue | Medium |
| 4.1.13 | Chainlink Data Providers | Premium data sources, enterprise partnerships | Medium |
| 4.1.14 | Chainlink in DeFi | Aave, Compound, Synthetix integration | High |
| 4.1.15 | Chainlink Economics 2.0 | Staking v2, incentives, security model | High |
| 4.1.16 | Chainlink vs Competitors | Band, API3, Pyth comparison | Medium |
| 4.1.17 | Chainlink BUILD Program | Early-stage project support, fee sharing | Medium |
| 4.1.18 | Chainlink SCALE Program | Sustainable blockchain support, fee subsidies | Medium |
| 4.1.19 | Off-Chain Reporting (OCR) | Efficient data aggregation, gas optimization | Medium |
| 4.1.20 | Chainlink Data Streams | Low-latency data, high-frequency trading | Medium |
| 4.1.21 | Chainlink Institutional Adoption | SWIFT, banks, traditional finance integration | High |
| 4.1.22 | SmartCon Conference | Annual conference, ecosystem development | Low |
| 4.1.23 | Chainlink Labs | Development company, research, partnerships | Medium |
| 4.1.24 | Chainlink Security Model | Reputation, staking, decentralization | High |
| 4.1.25 | Chainlink Roadmap | Future developments, vision | Medium |

### Category 4.2: Other Oracle Solutions (15 subtopics)

**Band Protocol, Pyth Network, API3, Tellor, UMA, DIA, Chronicle** (covering oracle diversity)

---

## SECTION 5: STABLECOINS (60 subtopics)

### Category 5.1: Centralized Stablecoins (20 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 5.1.1 | USDT (Tether) Overview | Largest stablecoin, history, controversy | High |
| 5.1.2 | Tether Reserves | Backing composition, transparency concerns | High |
| 5.1.3 | USDT Dominance | Market share, trading volume, liquidity | High |
| 5.1.4 | Tether Controversies | Legal issues, audit questions, FUD cycles | High |
| 5.1.5 | USDC (Circle) Overview | Regulated stablecoin, institutional grade | High |
| 5.1.6 | USDC Reserves | 100% cash and treasuries, attestations | High |
| 5.1.7 | Circle Company | Banking partnerships, SPAC, regulation | Medium |
| 5.1.8 | USDC vs USDT | Trust, regulation, use case differences | High |
| 5.1.9 | BUSD (Binance USD) | Paxos-issued, regulatory shutdown | Medium |
| 5.1.10 | PYUSD (PayPal USD) | PayPal stablecoin, mainstream adoption | Medium |
| 5.1.11 | TUSD (TrueUSD) | Real-time attestations, transparency | Low |
| 5.1.12 | USDP (Pax Dollar) | Paxos stablecoin, regulated | Low |
| 5.1.13 | GUSD (Gemini Dollar) | Winklevoss twins, New York regulated | Low |
| 5.1.14 | Stablecoin Regulation | MiCA, stablecoin bills, global landscape | High |
| 5.1.15 | Stablecoin Depegging Events | SVB crisis, USDC depeg, market impacts | High |
| 5.1.16 | Stablecoin Yields | T-bill yields, revenue models, user returns | Medium |
| 5.1.17 | Stablecoin Market Size | Total market cap, growth trends, dominance | High |
| 5.1.18 | Banking Relationships | Partner banks, deposit insurance, risks | Medium |
| 5.1.19 | Stablecoin Transparency | Attestations vs audits, reserve reporting | High |
| 5.1.20 | Cross-Border Payments | Remittances, settlement, speed advantages | High |

### Category 5.2: Decentralized Stablecoins (25 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 5.2.1 | DAI (MakerDAO) Overview | Decentralized, over-collateralized, governance | High |
| 5.2.2 | MakerDAO Vaults | Collateralized Debt Positions, liquidations | High |
| 5.2.3 | MKR Token Governance | Voting, risk parameters, stability fee | High |
| 5.2.4 | DAI Collateral Types | ETH, WBTC, stablecoins, real-world assets | High |
| 5.2.5 | DAI Stability Mechanisms | DSR, PSM, liquidations, peg maintenance | High |
| 5.2.6 | MakerDAO Endgame | SubDAOs, NewStable, governance evolution | Medium |
| 5.2.7 | Real-World Assets in MakerDAO | Centrifuge, loans, treasury bills | Medium |
| 5.2.8 | FRAX Finance | Fractional algorithmic, AMO, v3 roadmap | High |
| 5.2.9 | Liquity & LUSD | Immutable, 0% interest, redemption mechanism | High |
| 5.2.10 | crvUSD (Curve) | LLAMMA, soft liquidations, peg mechanism | High |
| 5.2.11 | GHO (Aave) | Native Aave stablecoin, discount model | High |
| 5.2.12 | sUSD (Synthetix) | Synthetic stablecoin, SNX collateral | Medium |
| 5.2.13 | USDD (Tron) | Algorithmic attempt, over-collateralized | Low |
| 5.2.14 | Ethena USDe | Delta-neutral, synthetic dollar, sUSDe yield | High |
| 5.2.15 | Algorithmic Stablecoin Failures | UST/LUNA, Iron Finance, Empty Set Dollar | High |
| 5.2.16 | UST/LUNA Collapse | Terra ecosystem, Do Kwon, systemic failure | High |
| 5.2.17 | Collateralization Ratios | Over-collateralization requirements, safety | High |
| 5.2.18 | Liquidation Mechanisms | Auction systems, keepers, MEV | Medium |
| 5.2.19 | Peg Stability Modules | Arbitrage mechanisms, trading interfaces | Medium |
| 5.2.20 | Decentralized Stablecoin Risks | Smart contract, governance, oracle risks | High |
| 5.2.21 | Stablecoin Yields | Lending rates, savings rate, protocol revenue | High |
| 5.2.22 | Governance Attacks | Voting power, protocol changes, vulnerabilities | Medium |
| 5.2.23 | Decentralized vs Centralized | Censorship resistance, capital efficiency | High |
| 5.2.24 | Stablecoin Adoption in DeFi | Liquidity pairs, lending markets, integration | High |
| 5.2.25 | Future of Decentralized Stables | Innovation, regulation, market share | Medium |

### Category 5.3: Stablecoin Infrastructure (15 subtopics)

Payment rails, Cross-chain bridges, Liquidity aggregation, Yield optimization, etc.

---

## SECTION 6: DEFI PROTOCOLS (80 subtopics)

### Category 6.1: Decentralized Exchanges (25 subtopics)

**Uniswap V2/V3/V4, SushiSwap, Curve, Balancer, PancakeSwap, Trader Joe, dYdX, GMX, etc.**

### Category 6.2: Lending & Borrowing (25 subtopics)

**Aave V2/V3, Compound, MakerDAO, Euler, Radiant, Venus, Benqi, etc.**

### Category 6.3: Derivatives & Perpetuals (15 subtopics)

**dYdX, GMX, Synthetix, Perpetual Protocol, etc.**

### Category 6.4: Yield & Liquid Staking (15 subtopics)

**Lido, Rocket Pool, Frax Ether, Yearn, Convex, etc.**

---

## SECTION 7: EMERGING & UP-AND-COMING (100 subtopics)

### Category 7.1: Hyperliquid (25 subtopics)

| ID | Subtopic | Description | Priority |
|----|----------|-------------|----------|
| 7.1.1 | Hyperliquid Overview | High-performance DEX, native L1 | High |
| 7.1.2 | Hyperliquid L1 Architecture | HyperBFT consensus, 20k TPS, sub-second finality | High |
| 7.1.3 | HYPE Token | Native token, tokenomics, launch | High |
| 7.1.4 | Perpetuals Trading | Order book DEX, leverage, funding rates | High |
| 7.1.5 | Hyperliquid Vaults | Strategy vaults, HLP liquidity provision | High |
| 7.1.6 | HyperEVM | EVM compatibility layer, smart contracts | High |
| 7.1.7 | Native Token Launches | Spot trading, token listings | Medium |
| 7.1.8 | Hyperliquidity Provider (HLP) | Vault liquidity, revenue sharing | Medium |
| 7.1.9 | Validator Set | Permissioned validators, decentralization roadmap | Medium |
| 7.1.10 | Trading Performance | Latency, throughput, user experience | High |
| 7.1.11 | Points System | Pre-token incentives, airdrop mechanics | Medium |
| 7.1.12 | Hyperliquid vs CEX | Performance comparison, custody model | High |
| 7.1.13 | Hyperliquid vs Other DEXs | dYdX, GMX, Jupiter comparison | High |
| 7.1.14 | API Trading | Programmatic access, market makers | Medium |
| 7.1.15 | Order Types | Limit, market, trigger orders, advanced | Medium |
| 7.1.16 | Fee Structure | Maker/taker fees, volume discounts | Medium |
| 7.1.17 | Risk Engine | Margin requirements, liquidations | Medium |
| 7.1.18 | Hyperliquid Adoption | Volume growth, user metrics, TVL | High |
| 7.1.19 | Builder Program | Developer incentives, ecosystem growth | Medium |
| 7.1.20 | Cross-Margining | Unified margin, capital efficiency | Medium |
| 7.1.21 | Oracle System | Price feeds, funding rate calculation | Medium |
| 7.1.22 | Governance Model | Community governance, protocol upgrades | Medium |
| 7.1.23 | Security Model | Audits, bug bounties, incident response | High |
| 7.1.24 | Market Making | Professional MMs, liquidity depth | Medium |
| 7.1.25 | Future Roadmap | Planned features, scaling, decentralization | High |

### Category 7.2: Modular Blockchains (25 subtopics)

**Celestia** (Data availability)
**EigenLayer** (Restaking)
**AltLayer** (Rollup-as-a-Service)
**Dymension** (RollApps)
**Fuel** (Modular execution)

### Category 7.3: New Layer 1s & 2s (25 subtopics)

**Berachain** (Proof-of-Liquidity)
**Monad** (Parallel EVM)
**Sei** (Optimistic parallelization)
**Aptos** (Move language)
**Sui** (Move language)
**Injective** (Cosmos DeFi)

### Category 7.4: Emerging DeFi & Infrastructure (25 subtopics)

**Pendle** (Yield trading)
**Morpho** (Lending optimization)
**EtherFi** (Restaking)
**Renzo** (Restaking)
**Ethena** (Synthetic dollar)
**Across** (Intent-based bridge)

---

## SECTION 8: NFT & GAMING (40 subtopics)

### Category 8.1: NFT Marketplaces (10 subtopics)

**OpenSea, Blur, Magic Eden, Tensor, LooksRare, X2Y2, etc.**

### Category 8.2: NFT Standards & Infrastructure (15 subtopics)

**ERC-721, ERC-1155, Compressed NFTs, NFT Royalties, etc.**

### Category 8.3: Gaming & Metaverse (15 subtopics)

**Axie Infinity, The Sandbox, Decentraland, Immutable X, Ronin, etc.**

---

## SECTION 9: PRIVACY & ZERO-KNOWLEDGE (30 subtopics)

### Category 9.1: Privacy Coins (10 subtopics)

**Monero, Zcash, DASH, etc.**

### Category 9.2: Zero-Knowledge Technology (20 subtopics)

**zkSNARKs, zkSTARKs, Aztec Network, Tornado Cash, Railgun, etc.**

---

## SECTION 10: CROSS-CUTTING TOPICS (50 subtopics)

### Category 10.1: Tokenomics Models (15 subtopics)

**ve(3,3), Vote-escrowed, Real yield, Points systems, Airdrops, etc.**

### Category 10.2: Governance Mechanisms (15 subtopics)

**On-chain voting, Snapshot, Delegation, Governance attacks, etc.**

### Category 10.3: Security & Auditing (20 subtopics)

**Smart contract audits, Bug bounties, Formal verification, Exploits, etc.**

---

## COMPLETE DATABASE SUMMARY

### Total Scope

| Section | Subtopics | Priority Distribution | Est. Q&A Pairs |
|---------|-----------|----------------------|----------------|
| 1. Bitcoin | 263 | 120 High, 93 Med, 50 Low | 7,890-13,150 |
| 2. Ethereum | 120 | 80 High, 30 Med, 10 Low | 3,600-6,000 |
| 3. Layer 1s | 150 | 70 High, 60 Med, 20 Low | 4,500-7,500 |
| 4. Oracles | 40 | 25 High, 12 Med, 3 Low | 1,200-2,000 |
| 5. Stablecoins | 60 | 40 High, 15 Med, 5 Low | 1,800-3,000 |
| 6. DeFi | 80 | 50 High, 25 Med, 5 Low | 2,400-4,000 |
| 7. Emerging | 100 | 50 High, 40 Med, 10 Low | 3,000-5,000 |
| 8. NFT/Gaming | 40 | 20 High, 15 Med, 5 Low | 1,200-2,000 |
| 9. Privacy/ZK | 30 | 15 High, 12 Med, 3 Low | 900-1,500 |
| 10. Cross-Cutting | 50 | 25 High, 20 Med, 5 Low | 1,500-2,500 |
| **TOTAL** | **933** | **495 High, 322 Med, 116 Low** | **27,990-46,650** |

---

## Database Implementation

### Tables Required

```sql
-- Master categories table
CREATE TABLE crypto_fundamentals_categories (
    category_id VARCHAR(10) PRIMARY KEY,
    section_name VARCHAR(100),
    category_name VARCHAR(200),
    description TEXT,
    priority VARCHAR(20),
    total_subtopics INTEGER
);

-- Subtopics table
CREATE TABLE crypto_fundamentals_subtopics (
    subtopic_id VARCHAR(20) PRIMARY KEY,
    category_id VARCHAR(10) REFERENCES crypto_fundamentals_categories,
    subtopic_name VARCHAR(300),
    description TEXT,
    priority VARCHAR(20),
    target_qa_pairs INTEGER DEFAULT 30,
    actual_qa_pairs INTEGER DEFAULT 0
);

-- Q&A pairs table (same structure as before)
CREATE TABLE crypto_fundamentals_qa_pairs (
    qa_id SERIAL PRIMARY KEY,
    subtopic_id VARCHAR(20) REFERENCES crypto_fundamentals_subtopics,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    difficulty_level VARCHAR(20),
    tags TEXT[],
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Execution Strategy

### Phase 1: Core Foundation (High Priority)
- **Subtopics:** 495 high-priority across all sections
- **Target:** 14,850-24,750 Q&A pairs
- **Timeline:** 12-16 weeks
- **Focus:** Bitcoin, Ethereum, Top L1s, Major DeFi, Stablecoins

### Phase 2: Expansion (Medium Priority)
- **Subtopics:** 322 medium-priority
- **Target:** 9,660-16,100 Q&A pairs
- **Timeline:** 8-12 weeks
- **Focus:** Emerging projects, additional protocols, infrastructure

### Phase 3: Comprehensive Coverage (Low Priority)
- **Subtopics:** 116 low-priority
- **Target:** 3,480-5,800 Q&A pairs
- **Timeline:** 4-6 weeks
- **Focus:** Specialized topics, edge cases, historical projects

**Total Expected Timeline:** 24-34 weeks (6-8.5 months)

---

**Schema Version:** 2.0 - Cryptocurrency Fundamentals (Complete)
**Date:** 2025-11-03
**Scope:** 933 subtopics across 10 sections
**Target:** 28,000-47,000 Q&A pairs
**Status:** ✅ Ready for assignment creation
