from datetime import datetime, timedelta
from main import analyze_events

def make_event(start_time, end_time, desc="test job", pid=123):
    return {
        pid: {
            'START': (datetime.strptime(start_time, "%H:%M:%S"), desc),
            'END': (datetime.strptime(end_time, "%H:%M:%S"), desc)
        }
    }

def test_normal_info_case():
    events = make_event("10:00:00", "10:03:00")
    logs = analyze_events(events)
    log_lines = [line for line in logs if not line.startswith("===")]
    assert log_lines[0].startswith("INFO")

def test_warning_threshold():
    events = make_event("10:00:00", "10:06:00")
    logs = analyze_events(events)
    log_lines = [line for line in logs if not line.startswith("===")]
    assert log_lines[0].startswith("WARNING")

def test_error_threshold():
    events = make_event("10:00:00", "10:15:00")
    logs = analyze_events(events)
    log_lines = [line for line in logs if not line.startswith("===")]
    assert log_lines[0].startswith("ERROR")

def test_missing_end():
    pid = 999
    events = {
        pid: {
            'START': (datetime.strptime("10:00:00", "%H:%M:%S"), "no end job")
        }
    }
    logs = analyze_events(events)
    log_lines = [line for line in logs if not line.startswith("===")]
    assert "INCOMPLETE" in log_lines[0]

def test_missing_start():
    pid = 888
    events = {
        pid: {
            'END': (datetime.strptime("10:00:00", "%H:%M:%S"), "no start job")
        }
    }
    logs = analyze_events(events)
    log_lines = [line for line in logs if not line.startswith("===")]
    assert "INCOMPLETE" in log_lines[0]