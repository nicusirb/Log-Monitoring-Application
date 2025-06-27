import csv
from datetime import datetime, timedelta

# Variables
LOG_FILE = 'logs.log'
OUTPUT_FILE = 'output.log'
WARN_THRESHOLD = timedelta(minutes=5)
ERROR_THRESHOLD = timedelta(minutes=10)

def parse_logs(file_path):
    events = {}
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            time_str, desc, event_type, pid = row
            event_type = event_type.strip().upper() # Normalize event type
            if event_type not in ['START', 'END']:
                continue
            # Parse time and pid
            time_str = time_str.strip()
            timestamp = datetime.strptime(time_str, '%H:%M:%S') # Adjust format as needed
            pid = int(pid)
            if pid not in events:
                events[pid] = {} # Initialize dictionary for each PID
            events[pid][event_type] = (timestamp, event_type) # Store timestamp and type
    return events

def analyze_events(events):
    logs = [] # Initialize logs list
    for pid, data in events.items():
        start = data.get('START')
        end = data.get('END')
        if start and end:
            duration = end[0] - start[0] # Calculate duration
            duration = duration if duration >= timedelta(0) else timedelta(0) # Ensure non-negative duration
            msg = f"[{pid}] {start[1]} - Duration: {duration}" # Create message with PID and duration
            if duration > ERROR_THRESHOLD:
                logs.append("ERROR: " + msg) # Log error if duration exceeds error threshold
            elif duration > WARN_THRESHOLD:
                logs.append("WARNING: " + msg) # Log warning if duration exceeds warning threshold
            else:
                logs.append("INFO: " + msg) # Log info if duration is within thresholds
        else:
            logs.append(f"INCOMPLETE: Missing START or END for PID {pid}") # Log incomplete events
    logs.sort(reverse=True) # Sort logs alphabetically


    logs.insert(0, "=== Event Analysis Report ===") # Add report header
    logs.append("=== End of Report ===") # Add report footer
    # Add summary of events
    logs.append("=== Summary of Events ===")
    logs.append(f"Total events processed: {len(events)}")
    logs.append(f"Total unique PIDs: {len(events)}")
    logs.append(f"Warnings issued: {sum(1 for log in logs if 'WARNING' in log)}")
    logs.append(f"Errors issued: {sum(1 for log in logs if 'ERROR' in log)}")
    logs.append(f"Info messages: {sum(1 for log in logs if 'INFO' in log)}")
    # Add a summary of durations
    total_duration = sum((data['END'][0] - data['START'][0] for data in events.values() if 'START' in data and 'END' in data), timedelta())
    logs.append(f"Total duration of all events: {total_duration}")
    logs.append(f"Average duration per event: {total_duration / len(events) if events else timedelta(0)}")
    logs.append(f"Max duration of an event: {max((data['END'][0] - data['START'][0] for data in events.values() if 'START' in data and 'END' in data), default=timedelta(0))}")
    logs.append(f"Min duration of an event: {min((data['END'][0] - data['START'][0] for data in events.values() if 'START' in data and 'END' in data), default=timedelta(0))}")
    return logs

def write_output(logs, output_file):
    with open(output_file, 'w') as f:
        for line in logs:
            print(line)
            f.write(line + '\n')

if __name__ == "__main__":
    events = parse_logs(LOG_FILE)
    logs = analyze_events(events)
    write_output(logs, OUTPUT_FILE)