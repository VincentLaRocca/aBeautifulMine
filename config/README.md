# Domain Configuration Examples

**aBeautifulMine Framework - Domain Configuration Templates**

This directory contains ready-to-use configurations for deploying the knowledge base generation system to different domains.

---

## Available Configurations

### 1. Web Development (`web_development_config.json`)

**Target:** 50 topics, ~5,000 Q&A pairs

**Sessions:** 10 sessions covering:
- Frontend Fundamentals (HTML5, CSS Grid, Flexbox, JavaScript, DOM)
- React Ecosystem (Hooks, Patterns, State, Performance, Testing)
- Backend Development (Express, Auth, Database, API Design, Error Handling)
- Performance & Optimization (Core Web Vitals, Images, Bundling, Caching, PWA)
- Security (XSS, CSRF, SQL Injection, HTTPS, Headers)
- DevOps & Deployment (Docker, CI/CD, Cloud, Monitoring, Backups)
- Testing (Unit, Integration, E2E, Performance, Accessibility)
- TypeScript (Fundamentals, Advanced Patterns, React, Config, Best Practices)
- Modern Frameworks (Next.js App Router, Data Fetching, API Routes, Performance)
- Build Tools (Vite, ESLint, Package Management, Git Workflows, Monorepos)

**Use Case:** Building RAG system for web development questions

**Deploy Command:**
```bash
python tools/generate_assignments.py config/web_development_config.json
```

---

### 2. Database Design (`database_design_config.json`)

**Target:** 40 topics, ~4,000 Q&A pairs

**Sessions:** 8 sessions covering:
- Relational Database Fundamentals (Normalization, Keys, ER Modeling, Data Types, Schemas)
- SQL Optimization (Indexing, Query Optimization, Execution Plans, Stored Procedures, Views)
- Transactions & Concurrency (ACID, Locking, Isolation Levels, Deadlocks, MVCC)
- Database Security (Auth, SQL Injection, Encryption, Auditing, Row-Level Security)
- Backup & Recovery (Backup Strategies, PITR, Disaster Recovery, High Availability, Replication)
- NoSQL Databases (MongoDB, Redis, CAP Theorem, DynamoDB, Graph DBs)
- Data Warehousing (Star Schema, ETL, Columnar DBs, OLAP vs OLTP, Data Lakes)
- Database Administration (Performance Monitoring, Index Maintenance, Migrations, Partitioning, Upgrades)

**Use Case:** Training AI on database design patterns and best practices

**Deploy Command:**
```bash
python tools/generate_assignments.py config/database_design_config.json
```

---

### 3. AI Agents (`ai_agents_config.json`)

**Target:** 60 topics, ~6,000 Q&A pairs

**Sessions:** 10 sessions covering:
- Agent Fundamentals (Architecture, Perception, Action Selection, Communication, Lifecycle)
- LLM-Based Agents (Prompt Engineering, ReAct, Tool Use, Memory, Planning, Self-Reflection)
- Multi-Agent Systems (Coordination, Communication Patterns, Negotiation, Consensus, Emergent Behavior)
- Agent Learning (Q-Learning, Policy Gradient, Multi-Agent RL, Transfer Learning, Curriculum Learning)
- Agent Safety & Alignment (Reward Hacking, Robustness, Explainability, Value Alignment, Monitoring)
- Autonomous Systems (RPA, Autonomous Vehicles, Trading Agents, Game-Playing, Customer Service)
- Agent Frameworks & Tools (LangChain, AutoGPT, Communication Middleware, Simulation, Deployment)
- Advanced Agent Patterns (Hierarchical, Modular, Evolutionary, Hybrid Neural-Symbolic, Meta-Agents)
- Agent Evaluation (Performance Metrics, Benchmarks, Testing Strategies, A/B Testing, Human Evaluation)
- Ethical & Social Considerations (Privacy, Fairness, Transparency, Human Collaboration, Compliance)

**Use Case:** Comprehensive knowledge base for AI agent development

**Deploy Command:**
```bash
python tools/generate_assignments.py config/ai_agents_config.json
```

---

## Configuration Structure

### Domain Metadata

```json
{
  "domain": {
    "name": "Human-readable domain name",
    "id": "slug_identifier",
    "description": "Description of the domain",
    "target_qa_total": 5000
  }
}
```

**Fields:**
- `name`: Display name (e.g., "Web Development Best Practices")
- `id`: Slug for file naming (e.g., "web_development")
- `description`: Brief description of domain scope
- `target_qa_total`: Total Q&A pairs target across all sessions

---

### Session Structure

```json
{
  "sessions": [
    {
      "session_number": 1,
      "category": "Category Name",
      "subcategory": "Optional Subcategory",
      "target_qa": 100,
      "topics": [...]
    }
  ]
}
```

**Fields:**
- `session_number`: Numeric identifier (1, 2, 3, ...)
- `category`: High-level grouping (e.g., "Frontend Fundamentals")
- `subcategory`: Optional sub-grouping (e.g., "Core Technologies")
- `target_qa`: Q&A pairs per topic in this session (default: 100)
- `topics`: Array of topic objects

---

### Topic Structure

```json
{
  "name": "Topic Name",
  "description": "Brief description",
  "target_qa": 100,
  "focus_areas": [
    "Focus area 1",
    "Focus area 2"
  ],
  "example_questions": [
    "Example question 1?",
    "Example question 2?"
  ]
}
```

**Fields:**
- `name`: Topic name (e.g., "React Hooks")
- `description`: What this topic covers
- `target_qa`: Q&A pairs target (default: 100)
- `focus_areas`: Specific areas to cover (guides Droid's research)
- `example_questions`: Sample questions (helps Droid understand scope)

**Best Practices:**
- 4-6 focus areas per topic
- 3-5 example questions per topic
- Clear, specific topic names
- Avoid overlap between topics

---

## Creating Custom Configurations

### Step 1: Choose a Template

Copy the most similar domain:
```bash
cp config/web_development_config.json config/my_domain_config.json
```

### Step 2: Update Domain Metadata

```json
{
  "domain": {
    "name": "My Domain Name",
    "id": "my_domain",
    "description": "Description of what this covers",
    "target_qa_total": 3000  // Estimate: topics × 100
  }
}
```

### Step 3: Define Sessions

**Organize by logical groupings:**
```json
{
  "session_number": 1,
  "category": "Fundamentals",
  "subcategory": "Core Concepts",
  "target_qa": 100,
  "topics": [...]
}
```

**Session organization strategies:**
- **Difficulty:** Beginner → Intermediate → Advanced
- **Category:** Frontend → Backend → DevOps
- **Scope:** Core → Extended → Specialized
- **Workflow:** Design → Implementation → Testing

### Step 4: Define Topics

**Each topic should:**
- Be focused on one concept
- Have 4-6 clear focus areas
- Include example questions
- Target 100 Q&A pairs

**Example:**
```json
{
  "name": "React useEffect Hook",
  "description": "Understanding side effects in React",
  "target_qa": 100,
  "focus_areas": [
    "Dependency arrays",
    "Cleanup functions",
    "Execution timing",
    "Common pitfalls"
  ],
  "example_questions": [
    "When does useEffect run?",
    "What is a cleanup function?",
    "How do dependency arrays work?"
  ]
}
```

### Step 5: Validate Configuration

```bash
# Check configuration summary
python tools/generate_assignments.py --summary config/my_domain_config.json

# Review output:
# - Total topics
# - Total Q&A target
# - Session breakdown
```

### Step 6: Generate Assignments

```bash
python tools/generate_assignments.py config/my_domain_config.json
```

---

## Configuration Best Practices

### Topic Sizing

**Optimal:**
- 5-7 topics per session
- 100 Q&A per topic (Droid's sweet spot)
- 500-700 Q&A per session

**Avoid:**
- ❌ Too broad: "Web Development" (1 topic)
- ❌ Too narrow: "useState with arrays" (too specific)
- ✅ Just right: "React Hooks" (covers useState, useEffect, custom hooks)

### Focus Areas

**Good focus areas:**
- Specific enough to guide research
- Broad enough to allow depth
- Cover different aspects of topic

**Example:**
```json
"focus_areas": [
  "Core syntax and usage",
  "Common patterns",
  "Best practices",
  "Performance considerations",
  "Common mistakes"
]
```

### Example Questions

**Good example questions:**
- Show the depth expected
- Cover different difficulty levels
- Highlight key concepts

**Example:**
```json
"example_questions": [
  "What is X and when should it be used?",  // Foundational
  "How does X differ from Y?",              // Comparative
  "What are best practices for X?",         // Advanced
  "How do you debug X issues?"              // Practical
]
```

---

## Domain-Specific Considerations

### Technical Domains (Programming, Databases, etc.)

**Focus on:**
- Syntax and usage
- Design patterns
- Best practices
- Common pitfalls
- Performance considerations

**Example Topics:**
- React Hooks
- SQL Optimization
- Docker Configuration

---

### Theoretical Domains (Algorithms, Math, etc.)

**Focus on:**
- Definitions and concepts
- Proofs and derivations
- Applications
- Visual explanations

**Example Topics:**
- Graph Algorithms
- Probability Theory
- Linear Algebra

---

### Business Domains (Marketing, Finance, etc.)

**Focus on:**
- Strategies and frameworks
- Case studies
- Metrics and KPIs
- Best practices
- Tools and resources

**Example Topics:**
- SEO Strategies
- Financial Modeling
- Customer Acquisition

---

## Configuration Templates

### Minimal Configuration (10 Topics)

```json
{
  "domain": {
    "name": "Quick Test Domain",
    "id": "test_domain",
    "target_qa_total": 1000
  },
  "sessions": [
    {
      "session_number": 1,
      "category": "Core Concepts",
      "target_qa": 100,
      "topics": [
        {"name": "Topic 1", "target_qa": 100},
        {"name": "Topic 2", "target_qa": 100},
        ...
      ]
    }
  ]
}
```

**Use case:** Testing, proof of concept

---

### Medium Configuration (40-60 Topics)

**See:** `web_development_config.json`, `database_design_config.json`

**Use case:** Comprehensive domain coverage

---

### Large Configuration (100+ Topics)

```json
{
  "domain": {
    "name": "Computer Science Fundamentals",
    "id": "cs_fundamentals",
    "target_qa_total": 10000
  },
  "sessions": [
    // 20+ sessions
    // 5-7 topics each
    // 10,000+ Q&A total
  ]
}
```

**Use case:** Complete curriculum, textbook replacement

---

## Calculating Target Q&A

### Formula

```
Total Q&A = Topics × Q&A per Topic
```

**Examples:**
- 50 topics × 100 Q&A = 5,000 total
- 40 topics × 100 Q&A = 4,000 total
- 100 topics × 100 Q&A = 10,000 total

### Adjusting Per Topic

**High-complexity topics:** 120-150 Q&A
- Broad topics (e.g., "JavaScript ES6+")
- Multi-faceted topics (e.g., "Database Security")

**Medium-complexity topics:** 100 Q&A (default)
- Focused topics (e.g., "React Hooks")
- Standard topics (e.g., "CSS Grid")

**Low-complexity topics:** 70-80 Q&A
- Narrow topics (e.g., "CSS Flexbox")
- Specific topics (e.g., "Git Rebase")

---

## Next Steps

### 1. Choose or Create Config

- Use existing: `web_development_config.json`
- Create custom: Follow steps above

### 2. Generate Assignments

```bash
python tools/generate_assignments.py config/your_config.json
```

### 3. Review Assignments

```bash
# Check generated files
ls inbox/droid/your_domain/
```

### 4. Give to Droid

- Copy assignments to Droid's inbox
- Droid conducts ultra deep research
- Wait for completion

### 5. Process Results

```bash
# Parse research reports
python tools/parse_domain_research.py --batch inbox/droid your_domain

# Import to database
python tools/import_domain_batch.py --batch \
  parsed_qa_data/your_domain \
  domains/your_domain/knowledge.db \
  "Your Domain" \
  your_domain
```

---

## Questions?

See comprehensive documentation:
- `tools/README.md` - Tool usage guide
- `UNIVERSAL_FRAMEWORK.md` - Complete methodology
- `THE_SYNTHESIS_PRINCIPLE.md` - Strategic insights

---

**These configs turn domain expertise into training data.**

**Plug and play for ANY domain.** 🔌

---

**Created:** 2025-11-02
**Part of:** aBeautifulMine Framework
**Status:** Production-ready
