#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime

def view_logs():
    """View available log files and their contents"""
    
    logs_dir = Path("crypto_questions_logs")
    
    if not logs_dir.exists():
        print("No logs directory found")
        print("Run the generator first to create log files")
        return
    
    # Get all log files sorted by modification time (newest first)
    log_files = sorted(logs_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not log_files:
        print("No log files found in the logs directory")
        return
    
    print("Available Log Files")
    print("=" * 50)
    
    for i, log_file in enumerate(log_files, 1):
        mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
        size_kb = log_file.stat().st_size / 1024
        status = "Running" if i == 1 else "Completed"
        
        print(f"{i}. {log_file.name}")
        print(f"   Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Size: {size_kb:.1f} KB")
        print(f"   Status: {status}")
        print()
    
    # Ask which log to view
    try:
        choice = input("Enter log file number to view (or press Enter to exit): ").strip()
        
        if not choice:
            return
            
        choice_num = int(choice)
        
        if 1 <= choice_num <= len(log_files):
            selected_log = log_files[choice_num - 1]
            print(f"\nViewing: {selected_log.name}")
            print("=" * 80)
            
            with open(selected_log, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
                
        else:
            print("Invalid selection")
            
    except (ValueError, IndexError):
        print("Invalid selection")
    except Exception as e:
        print(f"Error reading log file: {e}")

def monitor_running_process():
    """Monitor the currently running generator process"""
    
    logs_dir = Path("crypto_questions_logs")
    
    if not logs_dir.exists():
        print("No logs directory found")
        return
    
    # Get the most recent log file
    log_files = sorted(logs_dir.glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
    
    if not log_files:
        print("No log files found")
        return
    
    recent_log = log_files[0]
    
    print(f"Monitoring: {recent_log.name}")
    print("Press Ctrl+C to stop monitoring")
    print("=" * 60)
    
    try:
        while True:
            import time
            
            # Read the last few lines of the log
            with open(recent_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Show last 10 lines
                for line in lines[-10:]:
                    print(line.rstrip())
            
            print("-" * 40)
            time.sleep(2)  # Wait 2 seconds before checking again
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    
    except Exception as e:
        print(f"Error monitoring log: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--monitor":
        monitor_running_process()
    else:
        view_logs()
