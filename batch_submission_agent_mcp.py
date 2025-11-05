"""
Batch Submission Agent - MCP Integrated Version
================================================

Fully automated batch submission agent with MCP Gemini integration.
Handles uploads, batch creation, rate limits, and state persistence.

This script is designed to be run by Claude Code with access to MCP tools.

Usage via Claude Code:
    "Run the batch submission agent to complete all remaining batches"

Manual usage (if MCP client available):
    python batch_submission_agent_mcp.py [start_batch] [end_batch]
"""

import json
import time
from pathlib import Path
from datetime import datetime
import sys

# Configuration
BATCH_DIR = Path('gemini_batch_submissions_proper')
OUTPUT_DIR = Path('gemini_batch_results_proper')
STATE_FILE = Path('batch_submission_state.json')
LOG_FILE = Path('batch_submission_log.jsonl')

class BatchSubmissionAgentMCP:
    """MCP-integrated batch submission agent"""

    def __init__(self, start_batch=1, end_batch=204):
        self.start_batch = start_batch
        self.end_batch = end_batch
        self.state = self.load_state()
        OUTPUT_DIR.mkdir(exist_ok=True)

    def load_state(self):
        """Load previous submission state if exists"""
        if STATE_FILE.exists():
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'last_completed_batch': 0,
            'submitted_jobs': {},
            'uploaded_files': {},
            'failed_batches': [],
            'last_run': None,
            'total_submitted': 0
        }

    def save_state(self):
        """Save current submission state"""
        self.state['last_run'] = datetime.now().isoformat()
        self.state['total_submitted'] = len(self.state['submitted_jobs'])
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2)

    def log_event(self, event_type, batch_num, data):
        """Append event to log file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event_type,
            'batch': batch_num,
            'data': data
        }
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

    def get_remaining_batches(self):
        """Get list of batches that haven't been submitted yet"""
        submitted = set(int(b) for b in self.state['submitted_jobs'].keys())
        all_batches = list(range(self.start_batch, self.end_batch + 1))
        remaining = [b for b in all_batches if b not in submitted]
        return remaining

    def submit_single_batch(self, batch_num, mcp_tools):
        """
        Submit a single batch using MCP tools

        Args:
            batch_num: Batch number to submit
            mcp_tools: Dictionary of MCP tool functions

        Returns:
            (success, job_name, error_message)
        """
        batch_file = BATCH_DIR / f"batch_{batch_num:03d}_proper.jsonl"

        if not batch_file.exists():
            return False, None, f"Batch file not found: {batch_file}"

        try:
            # Step 1: Upload file
            print(f"  Uploading batch {batch_num:03d}...")
            upload_result = mcp_tools['upload_file'](
                filePath=str(batch_file)
            )

            if 'fileUri' not in upload_result:
                return False, None, f"Upload failed: No fileUri in response"

            file_uri = upload_result['fileUri']
            self.state['uploaded_files'][str(batch_num)] = file_uri
            self.log_event('upload_success', batch_num, {'file_uri': file_uri})

            # Step 2: Create batch job
            print(f"  Creating batch job {batch_num:03d}...")
            batch_result = mcp_tools['batch_create'](
                inputFileUri=file_uri,
                model='gemini-2.5-flash',
                displayName=f'refinement_batch_{batch_num:03d}',
                outputLocation=str(OUTPUT_DIR)
            )

            if 'batchName' not in batch_result:
                return False, None, f"Batch creation failed: No batchName in response"

            job_name = batch_result['batchName']
            self.state['submitted_jobs'][str(batch_num)] = {
                'job_name': job_name,
                'file_uri': file_uri,
                'submitted_at': datetime.now().isoformat(),
                'state': batch_result.get('state', 'UNKNOWN')
            }
            self.log_event('batch_created', batch_num, {'job_name': job_name})

            return True, job_name, None

        except Exception as e:
            error_msg = str(e)
            self.log_event('error', batch_num, {'error': error_msg})
            return False, None, error_msg

    def get_progress_stats(self):
        """Calculate current progress statistics"""
        total = self.end_batch - self.start_batch + 1
        submitted = len(self.state['submitted_jobs'])
        remaining = total - submitted
        percentage = (submitted / total) * 100 if total > 0 else 0

        return {
            'total': total,
            'submitted': submitted,
            'remaining': remaining,
            'percentage': percentage,
            'failed': len(self.state['failed_batches'])
        }

    def print_progress(self):
        """Print current progress"""
        stats = self.get_progress_stats()
        print(f"\n{'='*80}")
        print(f"Progress: {stats['submitted']}/{stats['total']} batches")
        print(f"({stats['percentage']:.1f}% complete)")
        print(f"Remaining: {stats['remaining']} | Failed: {stats['failed']}")
        print(f"{'='*80}\n")

    def generate_report(self):
        """Generate comprehensive submission report"""
        stats = self.get_progress_stats()

        report = {
            'report_generated': datetime.now().isoformat(),
            'batch_range': f"{self.start_batch}-{self.end_batch}",
            'statistics': stats,
            'submitted_jobs': self.state['submitted_jobs'],
            'failed_batches': self.state['failed_batches'],
            'last_run': self.state.get('last_run')
        }

        report_file = Path('batch_submission_final_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Full report saved to: {report_file}")
        return report

# This section would be used if running standalone with MCP client
def example_usage_with_claude_code():
    """
    Example of how Claude Code should use this agent:

    1. Import the agent class
    2. Create instance
    3. Pass MCP tool wrappers
    4. Run submission loop with rate limit handling
    """

    agent = BatchSubmissionAgentMCP(start_batch=81, end_batch=204)

    print("="*80)
    print("BATCH SUBMISSION AGENT - MCP VERSION")
    print("="*80)

    remaining = agent.get_remaining_batches()
    print(f"\nRemaining batches: {len(remaining)}")

    if not remaining:
        print("\n✓ All batches already submitted!")
        agent.generate_report()
        return

    # This is where Claude Code would provide actual MCP tool wrappers
    # For demonstration, showing the structure:
    print("""
    This agent is designed to be called by Claude Code with MCP tool access.

    Claude Code should:
    1. Create agent instance
    2. For each remaining batch:
       - Call agent.submit_single_batch(batch_num, mcp_tools)
       - Handle rate limits (429 errors) with 180s wait
       - Save state after each submission
       - Continue until all batches submitted
    3. Call agent.generate_report()

    See batch_submission_agent_claude_executor.md for full instructions.
    """)

if __name__ == "__main__":
    example_usage_with_claude_code()
