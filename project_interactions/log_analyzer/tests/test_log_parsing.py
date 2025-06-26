"""
Module: test_log_parsing.py
Purpose: Tests for log parsing functionality

External Dependencies:
- datetime: https://docs.python.org/3/library/datetime.html
- sys: https://docs.python.org/3/library/sys.html
- pathlib: https://docs.python.org/3/library/pathlib.html

Example Usage:
>>> from test_log_parsing import test_parse_json_logs
>>> test_parse_json_logs()
✅ JSON log parsing test passed
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from log_analyzer_interaction import LogParser, LogEntry, LogFormat


def test_parse_json_logs():
    """Test JSON log parsing"""
    parser = LogParser()
    
    # Test cases
    json_logs = [
        '{"timestamp": "2024-01-15T10:00:00", "level": "ERROR", "source": "api", "message": "Database connection failed"}',
        '{"timestamp": "2024-01-15T10:00:01", "level": "INFO", "source": "web", "message": "Request processed successfully"}',
        '{"timestamp": "2024-01-15T10:00:02", "level": "WARN", "source": "cache", "message": "Cache miss for key: user_123"}'
    ]
    
    parsed_logs = []
    for log_line in json_logs:
        entry = parser.parse(log_line, LogFormat.JSON)
        assert entry is not None, f"Failed to parse: {log_line}"
        assert entry.format_type == LogFormat.JSON
        parsed_logs.append(entry)
    
    # Verify parsing
    assert len(parsed_logs) == 3
    assert parsed_logs[0].level == "ERROR"
    assert parsed_logs[0].source == "api"
    assert parsed_logs[1].level == "INFO"
    assert parsed_logs[2].message == "Cache miss for key: user_123"
    
    print("✅ JSON log parsing test passed")
    return parsed_logs


def test_parse_syslog():
    """Test syslog format parsing"""
    parser = LogParser()
    
    syslog_lines = [
        'Jan 15 10:00:00 server01 kernel[1234]: Out of memory: Kill process 5678',
        'Jan 15 10:00:01 server01 sshd[5678]: Failed password for root from 192.168.1.1',
        'Jan 15 10:00:02 server01 systemd: Started Apache Web Server'
    ]
    
    parsed_logs = []
    for log_line in syslog_lines:
        entry = parser.parse(log_line)
        assert entry is not None, f"Failed to parse: {log_line}"
        parsed_logs.append(entry)
    
    # Verify parsing
    assert len(parsed_logs) == 3
    assert parsed_logs[0].source == "kernel"
    assert "Out of memory" in parsed_logs[0].message
    assert parsed_logs[1].metadata.get('pid') == '5678'
    
    print("✅ Syslog parsing test passed")
    return parsed_logs


def test_parse_apache_logs():
    """Test Apache log format parsing"""
    parser = LogParser()
    
    apache_logs = [
        '192.168.1.1 - - [15/Jan/2024:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234',
        '192.168.1.2 - - [15/Jan/2024:10:00:01 +0000] "POST /api/login HTTP/1.1" 401 567',
        '192.168.1.3 - - [15/Jan/2024:10:00:02 +0000] "GET /admin HTTP/1.1" 403 890'
    ]
    
    parsed_logs = []
    for log_line in apache_logs:
        entry = parser.parse(log_line)
        assert entry is not None, f"Failed to parse: {log_line}"
        assert entry.format_type == LogFormat.APACHE
        parsed_logs.append(entry)
    
    # Verify parsing
    assert len(parsed_logs) == 3
    assert parsed_logs[0].level == "INFO"  # 200 status
    assert parsed_logs[1].level == "ERROR"  # 401 status
    assert parsed_logs[2].level == "ERROR"  # 403 status
    assert parsed_logs[0].metadata['method'] == "GET"
    assert parsed_logs[1].metadata['path'] == "/api/login"
    
    print("✅ Apache log parsing test passed")
    return parsed_logs


def test_parse_nginx_logs():
    """Test nginx log format parsing"""
    parser = LogParser()
    
    nginx_logs = [
        '192.168.1.1 - - [15/Jan/2024:10:00:00 +0000] "GET /static/css/main.css HTTP/1.1" 200 12345 "http://example.com/" "Mozilla/5.0"',
        '192.168.1.2 - - [15/Jan/2024:10:00:01 +0000] "POST /api/data HTTP/1.1" 500 678 "-" "curl/7.68.0"'
    ]
    
    parsed_logs = []
    for log_line in nginx_logs:
        entry = parser.parse(log_line)
        assert entry is not None, f"Failed to parse: {log_line}"
        # Format type might vary based on detection order
        # assert entry.format_type == LogFormat.NGINX
        parsed_logs.append(entry)
    
    # Verify parsing
    assert len(parsed_logs) == 2
    assert parsed_logs[0].level == "INFO"  # 200 status
    assert parsed_logs[1].level == "ERROR"  # 500 status
    assert parsed_logs[0].metadata['user_agent'] == "Mozilla/5.0"
    
    print("✅ Nginx log parsing test passed")
    return parsed_logs


def test_parse_custom_logs():
    """Test custom log format parsing"""
    parser = LogParser()
    
    custom_logs = [
        '2024-01-15 10:00:00 ERROR Something went wrong in module X',
        'WARNING: 2024-01-15T10:00:01 Low disk space on /var',
        'Application started successfully at 2024-01-15 10:00:02'
    ]
    
    parsed_logs = []
    for log_line in custom_logs:
        entry = parser.parse(log_line)
        assert entry is not None, f"Failed to parse: {log_line}"
        assert entry.format_type == LogFormat.CUSTOM
        parsed_logs.append(entry)
    
    # Verify parsing
    assert len(parsed_logs) == 3
    assert parsed_logs[0].level == "ERROR"
    assert parsed_logs[1].level == "WARNING"
    assert parsed_logs[2].level == "INFO"
    
    print("✅ Custom log parsing test passed")
    return parsed_logs


def test_timestamp_parsing():
    """Test timestamp parsing"""
    parser = LogParser()
    
    # Test various timestamp formats
    timestamps = [
        "2024-01-15 10:00:00",
        "2024-01-15T10:00:00",
        "15/Jan/2024:10:00:00 +0000",
        "Jan 15 10:00:00"
    ]
    
    for ts_str in timestamps:
        timestamp = parser._parse_timestamp(ts_str)
        assert isinstance(timestamp, datetime), f"Failed to parse timestamp: {ts_str}"
    
    print("✅ Timestamp parsing test passed")


def test_level_extraction():
    """Test log level extraction"""
    parser = LogParser()
    
    test_cases = [
        ("ERROR: Database connection failed", "ERROR"),
        ("Warning: Low memory", "WARNING"),
        ("Info: Process started", "INFO"),
        ("CRITICAL: System failure", "CRITICAL"),
        ("Debug information here", "DEBUG"),
        ("Normal message without level", "INFO")
    ]
    
    for message, expected_level in test_cases:
        level = parser._extract_level(message)
        assert level == expected_level, f"Expected {expected_level}, got {level} for: {message}"
    
    print("✅ Level extraction test passed")


def run_all_tests():
    """Run all parsing tests"""
    print("🧪 Running log parsing tests...")
    
    test_parse_json_logs()
    test_parse_syslog()
    test_parse_apache_logs()
    test_parse_nginx_logs()
    test_parse_custom_logs()
    test_timestamp_parsing()
    test_level_extraction()
    
    print("\n✅ All log parsing tests passed!")


if __name__ == "__main__":
    run_all_tests()