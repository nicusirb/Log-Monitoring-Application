# 📊 Log Monitoring Application

A lightweight CLI application that reads a CSV-based log file and detects long-running jobs by tracking `START` and `END` events based on PIDs.

---

## Objective

Parse a log file (`logs.log`) to:
- Identify each job by its unique **PID**
- Match `START` and `END` events
- Calculate job duration
- Log:
  - `WARNING` if the job duration exceeds **5 minutes**
  - `ERROR` if the job duration exceeds **10 minutes**
- Print results to both console and `output.log`

---

## Log File Structure
- Each line in `logs.log` follows the format: `HH:MM:SS,<description>,START|END,<PID>`

### Example
```bash
11:35:23,scheduled task 032, START,37980
11:35:56,scheduled task 032, END,37980
```

---

## Features
- Lightweight and dependency-free core
- Highlights long-running jobs with warnings or errors
- Easy-to-read output to both console and file
- Designed with extensibility in mind

---

## How to Run

### ▶️ Run the application

```bash
python3 main.py
```

### Example Output
```
INFO: [37980] scheduled task 032 - Duration: 0:00:33
WARNING: [12345] scheduled task 999 - Duration: 0:07:10
ERROR: [98765] background job xy - Duration: 0:11:02
```

### Output will be written to:
- output.log

### Run Unit Tests
```bash
pip install pytest
pytest test_main.py
```

## Design Decisions
- Handles duplicate PIDs gracefully (ignores extra events beyond first START and END)
- Ignores incomplete jobs (missing either START or END event)
- Uses datetime for safe and accurate time math
- Does not currently support date rollovers (e.g., START before midnight, END after)

## Future Improvements
- Detect and handle logs crossing midnight
- Allow configurable thresholds via CLI (--warn, --error)
- Export results as structured JSON or HTML
- Develop a basic web interface for drag-n-drop allowing to use the application as a service
- Containerize the application for incapsulation