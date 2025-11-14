"""
Domain Configuration System
Define domain-specific settings for different subjects
"""

from typing import Dict, Optional

# Domain presets
DOMAIN_PRESETS = {
    "cryptocurrency": {
        "name": "Cryptocurrency & Trading",
        "research_specialization": "cryptocurrency and blockchain technology",
        "research_sources": "established trading education sites, recognized authors, in-depth articles",
        "example_context": "crypto-specific examples (BTC, ETH, SOL, etc.)",
        "example_types": "cryptocurrency examples",
        "practical_context": "crypto trading scenarios",
        "audience": "experienced traders and analysts",
        "domain_characteristics": "24/7 trading, volatility, DeFi, NFT, blockchain-specific considerations"
    },
    
    "medicine": {
        "name": "Medicine & Healthcare",
        "research_specialization": "medical science and healthcare",
        "research_sources": "peer-reviewed medical journals, established medical institutions, recognized medical authorities",
        "example_context": "medical case studies and clinical scenarios",
        "example_types": "medical examples",
        "practical_context": "clinical practice scenarios",
        "audience": "medical professionals and healthcare practitioners",
        "domain_characteristics": "evidence-based medicine, clinical guidelines, patient safety, regulatory compliance"
    },
    
    "law": {
        "name": "Law & Legal",
        "research_specialization": "legal systems and jurisprudence",
        "research_sources": "legal precedents, established legal texts, recognized legal authorities",
        "example_context": "legal case studies and precedents",
        "example_types": "legal examples",
        "practical_context": "legal practice scenarios",
        "audience": "legal professionals and practitioners",
        "domain_characteristics": "jurisdiction-specific, case law, statutes, regulatory frameworks"
    },
    
    "programming": {
        "name": "Programming & Software Development",
        "research_specialization": "software engineering and computer science",
        "research_sources": "technical documentation, established software engineering practices, recognized programming authorities",
        "example_context": "code examples and software development scenarios",
        "example_types": "programming examples",
        "practical_context": "software development scenarios",
        "audience": "software engineers and developers",
        "domain_characteristics": "best practices, design patterns, performance optimization, security considerations"
    },
    
    "finance": {
        "name": "Finance & Investment",
        "research_specialization": "finance and investment management",
        "research_sources": "established financial education sites, recognized financial authors, in-depth financial articles",
        "example_context": "financial market examples and investment scenarios",
        "example_types": "financial examples",
        "practical_context": "investment and trading scenarios",
        "audience": "financial professionals and investors",
        "domain_characteristics": "market analysis, risk management, portfolio optimization, regulatory compliance"
    },
    
    "general": {
        "name": "General Knowledge",
        "research_specialization": "general knowledge and information",
        "research_sources": "authoritative sources, recognized experts, in-depth articles",
        "example_context": "real-world examples and practical scenarios",
        "example_types": "relevant examples",
        "practical_context": "practical application scenarios",
        "audience": "knowledgeable professionals",
        "domain_characteristics": "broad applicability, practical implementation, real-world context"
    }
}


def get_domain_config(domain: str) -> Dict:
    """
    Get domain configuration
    
    Args:
        domain: Domain name (e.g., "cryptocurrency", "medicine", "law")
        
    Returns:
        Domain configuration dictionary
    """
    if domain.lower() in DOMAIN_PRESETS:
        return DOMAIN_PRESETS[domain.lower()].copy()
    else:
        # Return general as default
        return DOMAIN_PRESETS["general"].copy()


def create_custom_domain(
    name: str,
    research_specialization: str,
    research_sources: str,
    example_context: str,
    example_types: str,
    practical_context: str,
    audience: str,
    domain_characteristics: str
) -> Dict:
    """
    Create a custom domain configuration
    
    Args:
        name: Domain name
        research_specialization: What the researcher specializes in
        research_sources: Types of authoritative sources
        example_context: Context for examples
        example_types: Types of examples to use
        practical_context: Context for practical applications
        audience: Target audience
        domain_characteristics: Key characteristics of the domain
        
    Returns:
        Custom domain configuration
    """
    return {
        "name": name,
        "research_specialization": research_specialization,
        "research_sources": research_sources,
        "example_context": example_context,
        "example_types": example_types,
        "practical_context": practical_context,
        "audience": audience,
        "domain_characteristics": domain_characteristics
    }


def get_research_prompt(domain_config: Dict) -> str:
    """
    Generate research agent prompt from domain config
    
    Args:
        domain_config: Domain configuration dictionary
        
    Returns:
        Research system prompt
    """
    return f"""You are an expert researcher specializing in {domain_config['research_specialization']}.

Your role is to conduct thorough research on questions by:
1. Identifying key concepts and search terms
2. Synthesizing information from multiple authoritative sources
3. Organizing research findings logically
4. Identifying gaps or areas needing deeper investigation
5. Preparing research context for answer generation

Research Guidelines:
- Focus on authoritative sources ({domain_config['research_sources']})
- Synthesize information from multiple sources
- Identify key facts, concepts, and examples
- Note any conflicting information or different perspectives
- Highlight practical applications and real-world examples
- Identify risks, limitations, and considerations"""


def get_research_user_prompt_template(domain_config: Dict) -> str:
    """
    Generate research user prompt template
    
    Args:
        domain_config: Domain configuration dictionary
        
    Returns:
        Research user prompt template (use .format(question=question))
    """
    return """Conduct deep research on the following question:

QUESTION: {question}

Please provide:
1. Key concepts and terminology to understand
2. Main points and facts from authoritative sources
3. Practical examples and applications (especially {example_context})
4. Different perspectives or approaches
5. Risks, limitations, and considerations
6. Areas that need deeper investigation

Format your research as structured notes that can be used to generate a comprehensive answer.""".format(
        example_context=domain_config['example_context']
    )


def get_answer_prompt_template(domain_config: Dict) -> str:
    """
    Generate answer prompt template from domain config
    
    Args:
        domain_config: Domain configuration dictionary
        
    Returns:
        Answer prompt template
    """
    # This would replace the crypto-specific parts in the answer prompt
    # For now, return a template that can be customized
    base_template = """Core Task:

Your mission is to create a comprehensive, expert-level answer optimized for training AI agents. This answer will be used to train models to provide high-quality responses to {domain_name} questions.

CRITICAL: This is for ONE QUESTION ONLY. Answer each question individually with a complete, standalone response of 3,000+ characters.

---

## Quality Standards for AI Training Data

### 5. Domain-Specific Focus
- Always use {example_types}
- Reference {domain_name}-specific platforms, tools, and contexts
- Address {domain_name} characteristics ({domain_characteristics})
- Use realistic examples and scenarios relevant to {domain_name}

### 4. Educational Value
- Write as if teaching a {audience} who wants to understand deeply
- Use progressive disclosure: simple concepts first, then build complexity
- Include "why" explanations: don't just state facts, explain reasoning
- Use analogies and comparisons to clarify complex concepts
- Provide context: how this fits into broader {domain_name} strategies/practices

[Rest of prompt structure remains the same...]"""
    
    return base_template.format(
        domain_name=domain_config['name'],
        example_types=domain_config['example_types'],
        domain_characteristics=domain_config['domain_characteristics'],
        audience=domain_config['audience']
    )


# Example usage
if __name__ == "__main__":
    # Test with different domains
    crypto_config = get_domain_config("cryptocurrency")
    print("Cryptocurrency Domain:")
    print(f"  Name: {crypto_config['name']}")
    print(f"  Specialization: {crypto_config['research_specialization']}")
    
    medicine_config = get_domain_config("medicine")
    print("\nMedicine Domain:")
    print(f"  Name: {medicine_config['name']}")
    print(f"  Specialization: {medicine_config['research_specialization']}")
    
    # Custom domain
    custom = create_custom_domain(
        name="Machine Learning",
        research_specialization="machine learning and artificial intelligence",
        research_sources="peer-reviewed papers, established ML frameworks, recognized ML researchers",
        example_context="ML model examples and training scenarios",
        example_types="machine learning examples",
        practical_context="ML development scenarios",
        audience="ML engineers and data scientists",
        domain_characteristics="model training, hyperparameter tuning, data preprocessing, evaluation metrics"
    )
    print("\nCustom Domain (ML):")
    print(f"  Name: {custom['name']}")
    print(f"  Specialization: {custom['research_specialization']}")

