"""
Z.AI Institutional Cryptocurrency Research Generator
For generating high-quality institutional Q&A pairs using Z.AI GLM-4-Plus
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any
import time

class ZaiInstitutionalResearch:
    """
    Z.AI Research Agent for generating institutional cryptocurrency Q&A pairs.
    """

    def __init__(self, api_key: str):
        """Initialize with Z.AI API key."""
        self.api_key = api_key
        self.base_url = "https://api.z.ai/api/paas/v4"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model = "glm-4-plus"  # Confirmed working model

    def test_connection(self) -> Dict[str, Any]:
        """Test API connection with simple query."""
        try:
            response = self._make_request(
                messages=[{"role": "user", "content": "Hello, test connection."}],
                max_tokens=50
            )

            if response.get('choices'):
                return {
                    'status': 'success',
                    'message': 'Z.AI API connection successful',
                    'model': response.get('model'),
                    'response': response['choices'][0]['message']['content'][:100]
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Unexpected response format',
                    'response': response
                }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def _make_request(self, messages: List[Dict], max_tokens: int = 2000,
                     temperature: float = 0.7, retry_count: int = 3) -> Dict:
        """
        Make request to Z.AI API with retry logic.
        """
        url = f"{self.base_url}/chat/completions"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        for attempt in range(retry_count):
            try:
                response = requests.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=60
                )

                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                if attempt == retry_count - 1:
                    raise

                wait_time = (2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                print(f"  Request failed (attempt {attempt+1}/{retry_count}), retrying in {wait_time}s...")
                time.sleep(wait_time)

    def generate_single_qa(self, topic: str, question_focus: str) -> Dict:
        """
        Generate a single high-quality Q&A pair.

        Args:
            topic: Main cryptocurrency topic
            question_focus: Specific aspect to focus on

        Returns:
            Dict with question, answer, and metadata
        """
        system_prompt = """You are an expert institutional cryptocurrency analyst with deep knowledge of:
- Regulatory frameworks and compliance
- Risk management and due diligence
- Market structure and institutional trading
- Custody solutions and security protocols
- Professional investment strategies

Provide detailed, technically accurate answers suitable for institutional investors and professional traders."""

        user_prompt = f"""Generate ONE comprehensive question-answer pair about: {topic}

Focus area: {question_focus}

Requirements:
- Question should be specific and relevant to institutional investors
- Answer should be 1500-3000 characters
- Include technical details, regulatory considerations, and practical implications
- Use professional terminology
- Cite specific frameworks or standards when applicable

Format:
QUESTION: [Your specific question here]

ANSWER: [Your comprehensive answer here]"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        try:
            response = self._make_request(messages, max_tokens=3000, temperature=0.7)
            content = response['choices'][0]['message']['content']

            # Parse question and answer
            qa = self._parse_single_qa(content)

            if qa:
                qa['topic'] = topic
                qa['focus'] = question_focus
                qa['source'] = 'Z.AI GLM-4-Plus'
                qa['generated_at'] = datetime.now().isoformat()
                qa['tokens_used'] = response['usage']['total_tokens']
                return qa
            else:
                return None

        except Exception as e:
            print(f"  Error generating Q&A: {e}")
            return None

    def _parse_single_qa(self, content: str) -> Dict:
        """Parse a single Q&A from generated content."""
        try:
            # Look for QUESTION: and ANSWER: markers
            if 'QUESTION:' in content and 'ANSWER:' in content:
                q_start = content.index('QUESTION:') + len('QUESTION:')
                a_start = content.index('ANSWER:') + len('ANSWER:')

                question = content[q_start:a_start-len('ANSWER:')].strip()
                answer = content[a_start:].strip()

                if len(answer) >= 500:  # Minimum quality threshold
                    return {
                        'question': question,
                        'answer': answer,
                        'answer_length': len(answer)
                    }
        except (ValueError, IndexError):
            pass

        return None

    def generate_topic_research(self, topic: str, focus_areas: List[str]) -> List[Dict]:
        """
        Generate multiple Q&A pairs for a topic with different focus areas.

        Args:
            topic: Main cryptocurrency topic
            focus_areas: List of specific aspects to cover

        Returns:
            List of Q&A dictionaries
        """
        qa_pairs = []

        print(f"\nGenerating research for: {topic}")
        print(f"Focus areas: {len(focus_areas)}")

        for i, focus in enumerate(focus_areas, 1):
            print(f"  [{i}/{len(focus_areas)}] {focus[:60]}...")

            qa = self.generate_single_qa(topic, focus)

            if qa:
                qa_pairs.append(qa)
                print(f"      Generated ({qa['answer_length']} chars, {qa['tokens_used']} tokens)")
            else:
                print(f"      Failed to generate")

            # Rate limiting - small delay between requests
            if i < len(focus_areas):
                time.sleep(1)

        print(f"  Completed: {len(qa_pairs)}/{len(focus_areas)} pairs")
        return qa_pairs

    def generate_institutional_dataset(self, topics_config: List[Dict]) -> Dict:
        """
        Generate comprehensive institutional dataset.

        Args:
            topics_config: List of dicts with 'topic' and 'focus_areas'

        Returns:
            Dict with all Q&A pairs and statistics
        """
        all_pairs = []
        stats = {
            'topics_processed': 0,
            'total_pairs': 0,
            'total_tokens': 0,
            'errors': []
        }

        for topic_config in topics_config:
            topic = topic_config['topic']
            focus_areas = topic_config['focus_areas']

            try:
                pairs = self.generate_topic_research(topic, focus_areas)
                all_pairs.extend(pairs)

                stats['topics_processed'] += 1
                stats['total_pairs'] += len(pairs)
                stats['total_tokens'] += sum(p['tokens_used'] for p in pairs)

            except Exception as e:
                error_msg = f"Failed for topic '{topic}': {str(e)}"
                stats['errors'].append(error_msg)
                print(f"  ERROR: {error_msg}")

        return {
            'qa_pairs': all_pairs,
            'stats': stats,
            'generated_at': datetime.now().isoformat(),
            'model': self.model
        }


def main():
    """Main execution function."""

    print("="*80)
    print("Z.AI INSTITUTIONAL CRYPTOCURRENCY RESEARCH GENERATOR")
    print("="*80)

    # API Key
    api_key = "1799f7bc0add4cd8abd83343b32a4e33.EJhs1tr4OUXi0zyA"

    # Initialize agent
    agent = ZaiInstitutionalResearch(api_key)

    # Test connection
    print("\nTesting Z.AI API connection...")
    test_result = agent.test_connection()

    if test_result['status'] == 'success':
        print(f"SUCCESS: {test_result['message']}")
        print(f"Model: {test_result['model']}")
        print(f"Test response: {test_result['response']}...")
    else:
        print(f"ERROR: {test_result['message']}")
        return

    # Define research topics with specific focus areas
    topics_config = [
        {
            'topic': 'Bitcoin ETF Approval and Institutional Access',
            'focus_areas': [
                'SEC approval criteria for spot Bitcoin ETFs',
                'Custody requirements for ETF providers',
                'Market surveillance mechanisms',
                'Impact on institutional adoption rates',
                'Comparison with futures-based ETFs',
                'Tax implications for institutional ETF investors',
                'Liquidity considerations for large institutional positions'
            ]
        },
        {
            'topic': 'Cryptocurrency Custody Solutions',
            'focus_areas': [
                'Multi-signature wallet architecture',
                'Cold storage security protocols',
                'Insurance coverage for institutional custody',
                'Regulatory compliance requirements',
                'Key management best practices',
                'Disaster recovery procedures',
                'Third-party custody vs self-custody trade-offs'
            ]
        },
        {
            'topic': 'Regulatory Compliance for Crypto Trading Desks',
            'focus_areas': [
                'Registration requirements by jurisdiction',
                'AML/KYC implementation frameworks',
                'Trade reporting obligations',
                'Market manipulation prevention',
                'Cross-border compliance challenges',
                'Audit and record-keeping requirements',
                'Sanctions screening protocols'
            ]
        },
        {
            'topic': 'Stablecoin Infrastructure and Risk Management',
            'focus_areas': [
                'Reserve composition and transparency',
                'Third-party attestation requirements',
                'Redemption mechanisms and liquidity',
                'Regulatory status across jurisdictions',
                'Counterparty risk assessment',
                'Integration with banking systems',
                'Operational risk controls'
            ]
        },
        {
            'topic': 'Institutional Cryptocurrency Tax Frameworks',
            'focus_areas': [
                'Capital gains treatment across jurisdictions',
                'Staking and yield income classification',
                'Transfer pricing for cross-border transactions',
                'Tax loss harvesting strategies',
                'Reporting requirements for large positions',
                'DeFi protocol interaction tax implications',
                'Accounting standards for digital assets'
            ]
        }
    ]

    print(f"\n{'='*80}")
    print(f"GENERATING INSTITUTIONAL RESEARCH DATASET")
    print(f"{'='*80}")
    print(f"Topics: {len(topics_config)}")

    total_focus_areas = sum(len(t['focus_areas']) for t in topics_config)
    print(f"Total focus areas: {total_focus_areas}")
    print(f"Expected Q&A pairs: {total_focus_areas}")
    print(f"{'='*80}\n")

    # Generate dataset
    start_time = time.time()
    results = agent.generate_institutional_dataset(topics_config)
    elapsed_time = time.time() - start_time

    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"zai_institutional_qa_{timestamp}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Final report
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"Topics processed: {results['stats']['topics_processed']}/{len(topics_config)}")
    print(f"Q&A pairs generated: {results['stats']['total_pairs']}")
    print(f"Total tokens used: {results['stats']['total_tokens']:,}")
    print(f"Average tokens per pair: {results['stats']['total_tokens'] / max(results['stats']['total_pairs'], 1):.0f}")
    print(f"Time elapsed: {elapsed_time:.1f} seconds")
    print(f"Rate: {results['stats']['total_pairs'] / (elapsed_time / 60):.1f} pairs/minute")
    print(f"\nOutput file: {output_file}")

    if results['stats']['errors']:
        print(f"\nErrors encountered: {len(results['stats']['errors'])}")
        for error in results['stats']['errors']:
            print(f"  - {error}")

    # Quality metrics
    if results['qa_pairs']:
        avg_length = sum(p['answer_length'] for p in results['qa_pairs']) / len(results['qa_pairs'])
        print(f"\nQuality Metrics:")
        print(f"  Average answer length: {avg_length:.0f} characters")
        print(f"  Shortest answer: {min(p['answer_length'] for p in results['qa_pairs'])} characters")
        print(f"  Longest answer: {max(p['answer_length'] for p in results['qa_pairs'])} characters")

    print(f"\n{'='*80}")
    print("READY FOR INTEGRATION INTO PRODUCTION DATABASE")
    print(f"{'='*80}")

    return output_file


if __name__ == "__main__":
    output_file = main()
    print(f"\nTo integrate into production:")
    print(f"  python integrate_zai_data.py {output_file}")
