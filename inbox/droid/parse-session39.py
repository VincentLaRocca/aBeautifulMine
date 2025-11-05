#!/usr/bin/env python3

"""
Session 39 Parser - Cycle Indicators
Handles parsing of Q&A pairs for crypto cycle analysis indicators
"""

import json
import re
from pathlib import Path
from datetime import datetime

def parse_session39_content(content_text, session_num=39):
    """
    Parse Session 39 (Cycle Indicators) content from research report
    Extracts Q&A pairs for 5 indicators: Pi Cycle Top, MVRV Z-Score, Puell Multiple, 200-Week MA Heatmap, RHODL Ratio
    """
    
    # Initialize indicators storage
    indicators = {
        'pi_cycle_top': [],
        'mvrv_z_score': [],
        'puell_multiple': [],
        '200_week_ma_heatmap': [],
        'rhodl_ratio': []
    }
    
    # Pattern matching for Q&A pairs
    qa_pattern = r'(?:Q\d+\.?\s*|Question\s*\d*\.?\s*:?)([^?]*\?)\s*(?:A\d+\.?\s*|Answer\s*\d*\.?\s*:?\s*)(.*?)(?=Q\d+\.?\s*|Question\s*\d*\.?\s*|$)'
    
    # Extract Q&A pairs
    pairs = re.findall(qa_pattern, content_text, re.DOTALL | re.IGNORECASE)
    
    # Process each Q&A pair
    for question, answer in pairs:
        question = question.strip().replace('\n', ' ').replace('  ', ' ')
        answer = answer.strip().replace('\n', ' ').replace('  ', ' ')
        
        # Skip if too short
        if len(question) < 10 or len(answer) < 20:
            continue
            
        # Categorize based on keywords
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Pi Cycle Top detection
        if any(keyword in question_lower or keyword in answer_lower for keyword in [
            'pi cycle', '111 dma', '350 dma', 'pi cycle top', 'market top', 'cycle indicator',
            'moving average crossover', 'dma', '111 day', '350 day'
        ]):
            indicators['pi_cycle_top'].append({
                'question': question,
                'answer': answer,
                'session': session_num,
                'indicator': 'pi_cycle_top'
            })
            
        # MVRV Z-Score detection  
        elif any(keyword in question_lower or keyword in answer_lower for keyword in [
            'mvrv', 'z-score', 'market value realized value', 'overvalued', 'undervalued',
            'realized value', 'market value', 'standard deviation'
        ]):
            indicators['mvrv_z_score'].append({
                'question': question,
                'answer': answer,
                'session': session_num,
                'indicator': 'mvrv_z_score'
            })
            
        # Puell Multiple detection
        elif any(keyword in question_lower or keyword in answer_lower for keyword in [
            'puell multiple', 'miner revenue', 'daily issuance', 'mining', 'miner capitulation',
            'miner euphoria', 'coinbase transaction', '365 day moving average'
        ]):
            indicators['puell_multiple'].append({
                'question': question,
                'answer': answer,
                'session': session_num,
                'indicator': 'puell_multiple'
            })
            
        # 200-Week MA Heatmap detection
        elif any(keyword in question_lower or keyword in answer_lower for keyword in [
            '200 week', '200w ma', 'weekly moving average', 'heatmap', 'long term support',
            '200 dma', '200 weekly', 'below 200 week', 'above 200 week'
        ]):
            indicators['200_week_ma_heatmap'].append({
                'question': question,
                'answer': answer,
                'session': session_num,
                'indicator': '200_week_ma_heatmap'
            })
            
        # RHODL Ratio detection
        elif any(keyword in question_lower or keyword in answer_lower for keyword in [
            'rhodl', 'realized hodl', 'rhodl ratio', 'coin age bands', 'old coins',
            'new coins', '1w-1m', '1y-2y', 'holder distribution'
        ]):
            indicators['rhodl_ratio'].append({
                'question': question,
                'answer': answer,
                'session': session_num,
                'indicator': 'rhodl_ratio'
            })
        
        # If no specific category, add to most relevant based on context analysis
        else:
            # Simple heuristic - check for multiple keywords to determine best fit
            keyword_scores = {
                'pi_cycle_top': sum(1 for kw in ['pi', 'cycle', 'dma', '111', '350'] if kw in question_lower),
                'mvrv_z_score': sum(1 for kw in ['mvrv', 'z', 'score', 'realized'] if kw in question_lower),
                'puell_multiple': sum(1 for kw in ['puell', 'miner', 'issuance'] if kw in question_lower),
                '200_week_ma_heatmap': sum(1 for kw in ['200', 'week', 'heatmap', 'ma'] if kw in question_lower),
                'rhodl_ratio': sum(1 for kw in ['rhodl', 'hodl', 'age'] if kw in question_lower)
            }
            
            # Assign to indicator with highest keyword score
            if max(keyword_scores.values()) > 0:
                best_indicator = max(keyword_scores, key=keyword_scores.get)
                indicators[best_indicator].append({
                    'question': question,
                    'answer': answer,
                    'session': session_num,
                    'indicator': best_indicator
                })
    
    return indicators

def create_qa_pairs_file(indicator_data, indicator_name, session_num=39):
    """
    Create JSON file with formatted Q&A pairs for a specific indicator
    """
    
    # Ensure at least 100 pairs
    pairs_needed = 100
    current_pairs = len(indicator_data)
    
    if current_pairs < pairs_needed:
        print(f"Warning: {indicator_name} has only {current_pairs} pairs (need {pairs_needed})")
    
    # Standardize Q&A pairs
    qa_pairs = {
        'session': session_num,
        'indicator': indicator_name,
        'category': 'Cycle Indicators',
        'total_pairs': len(indicator_data),
        'generated_date': datetime.now().isoformat(),
        'pairs': []
    }
    
    for i, pair in enumerate(indicator_data[:pairs_needed], 1):
        qa_pairs['pairs'].append({
            'id': f"session{session_num}_{indicator_name}_{i:03d}",
            'question': pair['question'],
            'answer': pair['answer'],
            'session': session_num,
            'indicator': indicator_name,
            'category': 'Cycle Indicators',
            'sequence': i
        })
    
    return qa_pairs

def main():
    """
    Main function to parse Session 39 content and create Q&A pair files
    """
    
    # Look for Session 39 research report file
    session_pattern = "research_report_session-39-cycle-indicators-batch.txt"
    
    # Check for the file in the ultra_deep_research directory
    research_dir = Path("ultra_deep_research/research_reports/2025/11")
    session_file = None
    
    for file_path in research_dir.glob("*session-39*"):
        session_file = file_path
        break
    
    if not session_file:
        # Try alternative pattern
        for file_path in research_dir.glob("*cycle*"):
            if "39" in file_path.name or "cycle" in file_path.name.lower():
                session_file = file_path
                break
    
    if not session_file:
        print(f"Error: Could not find Session 39 research file")
        return
    
    print(f"Processing: {session_file}")
    
    # Read the content
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Parse Q&A pairs
    indicators = parse_session39_content(content)
    
    # Create individual JSON files for each indicator
    indicator_files = []
    
    for indicator_name, pairs in indicators.items():
        if pairs:  # Only if we have pairs for this indicator
            qa_pairs = create_qa_pairs_file(pairs, indicator_name)
            
            # Generate filename
            filename = f"session{39}_{indicator_name}_qa_pairs.json"
            filepath = Path(filename)
            
            # Save to file
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Created: {filename}")
                print(f"   Pairs: {len(pairs)}")
                
                indicator_files.append(filename)
                
            except Exception as e:
                print(f"Error saving {filename}: {e}")
    
    # Create summary
    print(f"\n=== SESSION 39 COMPLETE ===")
    print(f"Indicators processed: {len(indicator_files)}")
    print(f"Total Q&A pairs: {sum(len(indicators[ind]) for ind in indicators)}")
    print(f"Files created: {', '.join(indicator_files)}")
    
    return indicator_files

if __name__ == "__main__":
    main()
