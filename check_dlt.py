import json
import statistics

# Load the JSON file
with open(r'C:\Users\vlaro\dreamteam\claude\inbox\cursor\dlt_questions_answers.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

answers = data['answers']

# Check for crypto-specific keywords
crypto_keywords = ['bitcoin', 'btc', 'ethereum', 'eth', 'crypto', 'cryptocurrency', 'blockchain', 'altcoin']
crypto_count = sum(1 for a in answers if any(kw in a['answer'].lower() for kw in crypto_keywords))

print(f'Crypto-specific content: {crypto_count}/100 ({crypto_count}%)')
print(f'\nKeyword frequency:')
for kw in crypto_keywords:
    count = sum(1 for a in answers if kw in a['answer'].lower())
    print(f'  {kw}: {count} answers ({count}%)')

# Check markdown structure
print(f'\n\nMarkdown Structure Analysis:')
with_headings = sum(1 for a in answers if '##' in a['answer'])
with_bullets = sum(1 for a in answers if '- ' in a['answer'] or '* ' in a['answer'])
with_bold = sum(1 for a in answers if '**' in a['answer'])

print(f'Answers with markdown headings (##): {with_headings}/100 ({with_headings}%)')
print(f'Answers with bullet points: {with_bullets}/100 ({with_bullets}%)')
print(f'Answers with bold text (**): {with_bold}/100 ({with_bold}%)')

# Check for examples
with_examples = sum(1 for a in answers if 'example' in a['answer'].lower() or 'scenario' in a['answer'].lower())
print(f'Answers with examples/scenarios: {with_examples}/100 ({with_examples}%)')

# Sample first answer structure
print(f'\n\nFirst Answer Structure Preview:')
print(data['answers'][0]['answer'][:800])
print('...\n')
