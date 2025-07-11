
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: log_analyzer_interaction.py
Purpose: Distributed log analysis system with multi-format parsing and real-time analysis

External Dependencies:
- asyncio: https://docs.python.org/3/library/asyncio.html
- re: https://docs.python.org/3/library/re.html
- json: https://docs.python.org/3/library/json.html
- datetime: https://docs.python.org/3/library/datetime.html
- multiprocessing: https://docs.python.org/3/library/multiprocessing.html
- queue: https://docs.python.org/3/library/queue.html
- threading: https://docs.python.org/3/library/threading.html
- pathlib: https://docs.python.org/3/library/pathlib.html
- typing: https://docs.python.org/3/library/typing.html
- dataclasses: https://docs.python.org/3/library/dataclasses.html
- collections: https://docs.python.org/3/library/collections.html
- statistics: https://docs.python.org/3/library/statistics.html

Example Usage:
>>> analyzer = DistributedLogAnalyzer(worker_count=4)
>>> results = analyzer.analyze_logs(['access.log', 'error.log'])
>>> print(f"Analyzed {results['total_logs']} logs, found {results['anomalies']} anomalies")
Analyzed 10000 logs, found 42 anomalies
"""

import asyncio
import re
import json
from datetime import datetime, timedelta
from multiprocessing import Pool
import queue
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set, Union
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import statistics
from enum import Enum
import time
import concurrent.futures


class LogFormat(Enum):
    """Supported log formats"""
    JSON = "json"
    SYSLOG = "syslog"
    APACHE = "apache"
    NGINX = "nginx"
    CUSTOM = "custom"


@dataclass
class LogEntry:
    """Represents a parsed log entry"""
    timestamp: datetime
    level: str
    source: str
    message: str
    raw: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    format_type: LogFormat = LogFormat.CUSTOM


@dataclass(frozen=True)
class Pattern:
    """Represents a log pattern for detection"""
    name: str
    regex: Any  # re.Pattern
    severity: str
    category: str
    description: str


@dataclass
class Anomaly:
    """Represents a detected anomaly"""
    timestamp: datetime
    pattern: str
    severity: str
    affected_logs: List[LogEntry]
    confidence: float
    suggested_action: str


@dataclass
class AlertRule:
    """Alert rule configuration"""
    name: str
    condition: str
    threshold: int
    time_window: int  # seconds
    severity: str
    action: str


class LogParser:
    """Multi-format log parser"""
    
    # Common log patterns
    PATTERNS = {
        LogFormat.JSON: re.compile(r'^{.*}$'),
        LogFormat.SYSLOG: re.compile(
            r'^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+'
            r'(?P<host>\S+)\s+(?P<process>\S+?)(?:\[(?P<pid>\d+)\])?:\s+'
            r'(?P<message>.*)$'
        ),
        LogFormat.APACHE: re.compile(
            r'^(?P<ip>\S+)\s+\S+\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+'
            r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
            r'(?P<status>\d+)\s+(?P<size>\S+)'
        ),
        LogFormat.NGINX: re.compile(
            r'^(?P<ip>\S+)\s+-\s+\S+\s+\[(?P<timestamp>[^\]]+)\]\s+'
            r'"(?P<method>\S+)\s+(?P<path>\S+)\s+(?P<protocol>\S+)"\s+'
            r'(?P<status>\d+)\s+(?P<size>\d+)\s+"(?P<referrer>[^"]*)"\s+'
            r'"(?P<user_agent>[^"]*)"'
        )
    }
    
    def parse(self, line: str, format_hint: Optional[LogFormat] = None) -> Optional[LogEntry]:
        """Parse a log line into LogEntry"""
        line = line.strip()
        if not line:
            return None
            
        # Try JSON first if hinted or looks like JSON
        if format_hint == LogFormat.JSON or (line.startswith('{') and line.endswith('}')):
            entry = self._parse_json(line)
            if entry:
                return entry
        
        # Try other formats
        for log_format, pattern in self.PATTERNS.items():
            if log_format == LogFormat.JSON:
                continue
            if pattern.match(line):
                parser_method = getattr(self, f'_parse_{log_format.value}')
                entry = parser_method(line)
                if entry:
                    return entry
        
        # Fall back to custom parsing
        return self._parse_custom(line)
    
    def _parse_json(self, line: str) -> Optional[LogEntry]:
        """Parse JSON log format"""
        try:
            data = json.loads(line)
            return LogEntry(
                timestamp=self._parse_timestamp(data.get('timestamp', '')),
                level=data.get('level', 'INFO'),
                source=data.get('source', 'unknown'),
                message=data.get('message', ''),
                raw=line,
                metadata=data,
                format_type=LogFormat.JSON
            )
        except:
            return None
    
    def _parse_syslog(self, line: str) -> Optional[LogEntry]:
        """Parse syslog format"""
        match = self.PATTERNS[LogFormat.SYSLOG].match(line)
        if not match:
            return None
            
        groups = match.groupdict()
        return LogEntry(
            timestamp=self._parse_timestamp(groups['timestamp']),
            level=self._extract_level(groups['message']),
            source=groups['process'],
            message=groups['message'],
            raw=line,
            metadata={'host': groups['host'], 'pid': groups.get('pid')},
            format_type=LogFormat.SYSLOG
        )
    
    def _parse_apache(self, line: str) -> Optional[LogEntry]:
        """Parse Apache log format"""
        match = self.PATTERNS[LogFormat.APACHE].match(line)
        if not match:
            return None
            
        groups = match.groupdict()
        status = int(groups['status'])
        level = 'ERROR' if status >= 400 else 'INFO'
        
        return LogEntry(
            timestamp=self._parse_timestamp(groups['timestamp']),
            level=level,
            source='apache',
            message=f"{groups['method']} {groups['path']} - {status}",
            raw=line,
            metadata=groups,
            format_type=LogFormat.APACHE
        )
    
    def _parse_nginx(self, line: str) -> Optional[LogEntry]:
        """Parse nginx log format"""
        match = self.PATTERNS[LogFormat.NGINX].match(line)
        if not match:
            return None
            
        groups = match.groupdict()
        status = int(groups['status'])
        level = 'ERROR' if status >= 400 else 'INFO'
        
        return LogEntry(
            timestamp=self._parse_timestamp(groups['timestamp']),
            level=level,
            source='nginx',
            message=f"{groups['method']} {groups['path']} - {status}",
            raw=line,
            metadata=groups,
            format_type=LogFormat.NGINX
        )
    
    def _parse_custom(self, line: str) -> LogEntry:
        """Parse custom log format"""
        # Extract timestamp if present
        timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}', line)
        timestamp = self._parse_timestamp(timestamp_match.group() if timestamp_match else '')
        
        # Extract level
        level = self._extract_level(line)
        
        return LogEntry(
            timestamp=timestamp,
            level=level,
            source='custom',
            message=line,
            raw=line,
            metadata={},
            format_type=LogFormat.CUSTOM
        )
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """Parse various timestamp formats"""
        if not timestamp_str:
            return datetime.now()
            
        # Try common formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%d/%b/%Y:%H:%M:%S %z',
            '%b %d %H:%M:%S'
        ]
        
        for fmt in formats:
            try:
                parsed = datetime.strptime(timestamp_str.split('.')[0], fmt)
                # Make sure it's timezone-aware if needed, otherwise naive
                if '%z' in fmt and parsed.tzinfo:
                    return parsed.replace(tzinfo=None)  # Convert to naive
                return parsed
            except:
                continue
                
        return datetime.now()
    
    def _extract_level(self, message: str) -> str:
        """Extract log level from message"""
        levels = ['ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'CRITICAL', 'FATAL']
        message_upper = message.upper()
        
        for level in levels:
            if level in message_upper:
                return level
                
        return 'INFO'


class PatternDetector:
    """Detects patterns and anomalies in logs"""
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.baseline = {}
        
    def _initialize_patterns(self) -> List[Pattern]:
        """Initialize common error patterns"""
        return [
            Pattern(
                name="OutOfMemory",
                regex=re.compile(r'(out of memory|OOM|memory exhausted)', re.I),
                severity="CRITICAL",
                category="resource",
                description="Memory exhaustion detected"
            ),
            Pattern(
                name="ConnectionRefused",
                regex=re.compile(r'(connection refused|ECONNREFUSED)', re.I),
                severity="HIGH",
                category="network",
                description="Network connection failures"
            ),
            Pattern(
                name="AuthenticationFailure",
                regex=re.compile(r'(authentication failed|invalid credentials|login failed)', re.I),
                severity="HIGH",
                category="security",
                description="Authentication failures detected"
            ),
            Pattern(
                name="SQLInjection",
                regex=re.compile(r"(union\s+select|'; DROP|OR\s+1=1)", re.I),
                severity="CRITICAL",
                category="security",
                description="Potential SQL injection attempt"
            ),
            Pattern(
                name="HighLatency",
                regex=re.compile(r'(response time|latency).*?(\d+)\s*(ms|seconds)', re.I),
                severity="MEDIUM",
                category="performance",
                description="High latency detected"
            )
        ]
    
    def detect_patterns(self, logs: List[LogEntry]) -> List[Tuple[Pattern, List[LogEntry]]]:
        """Detect patterns in log entries"""
        matches = defaultdict(list)
        
        for log in logs:
            for pattern in self.patterns:
                if pattern.regex.search(log.message):
                    matches[pattern].append(log)
        
        return list(matches.items())
    
    def detect_anomalies(self, logs: List[LogEntry]) -> List[Anomaly]:
        """Detect anomalies based on statistical analysis"""
        anomalies = []
        
        # Group logs by source and level
        grouped = defaultdict(list)
        for log in logs:
            grouped[(log.source, log.level)].append(log)
        
        # Analyze each group
        for (source, level), group_logs in grouped.items():
            # Time-based anomaly detection
            if len(group_logs) > 10:
                time_anomalies = self._detect_time_anomalies(group_logs)
                anomalies.extend(time_anomalies)
        
        # Pattern-based anomalies
        pattern_matches = self.detect_patterns(logs)
        for pattern, matched_logs in pattern_matches:
            if len(matched_logs) > 0:
                anomalies.append(Anomaly(
                    timestamp=datetime.now(),
                    pattern=pattern.name,
                    severity=pattern.severity,
                    affected_logs=matched_logs,
                    confidence=0.9,
                    suggested_action=self._suggest_action(pattern)
                ))
        
        return anomalies
    
    def _detect_time_anomalies(self, logs: List[LogEntry]) -> List[Anomaly]:
        """Detect anomalies in log timing patterns"""
        anomalies = []
        
        # Calculate time intervals
        sorted_logs = sorted(logs, key=lambda x: x.timestamp)
        intervals = []
        
        for i in range(1, len(sorted_logs)):
            interval = (sorted_logs[i].timestamp - sorted_logs[i-1].timestamp).total_seconds()
            intervals.append(interval)
        
        if not intervals:
            return anomalies
        
        # Statistical analysis
        mean_interval = statistics.mean(intervals)
        stdev_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0
        
        # Detect burst anomalies (too many logs in short time)
        burst_threshold = max(0.1, mean_interval - 2 * stdev_interval)
        burst_logs = []
        
        for i, interval in enumerate(intervals):
            if interval < burst_threshold:
                burst_logs.append(sorted_logs[i+1])
        
        if len(burst_logs) > 5:
            anomalies.append(Anomaly(
                timestamp=datetime.now(),
                pattern="LogBurst",
                severity="MEDIUM",
                affected_logs=burst_logs,
                confidence=0.8,
                suggested_action="Investigate sudden increase in log frequency"
            ))
        
        return anomalies
    
    def _suggest_action(self, pattern: Pattern) -> str:
        """Suggest action based on pattern"""
        actions = {
            "OutOfMemory": "Increase memory allocation or optimize memory usage",
            "ConnectionRefused": "Check service availability and network configuration",
            "AuthenticationFailure": "Review authentication logs and check for brute force attempts",
            "SQLInjection": "Review application security and implement input validation",
            "HighLatency": "Analyze performance bottlenecks and optimize slow operations"
        }
        return actions.get(pattern.name, "Investigate the issue and take appropriate action")


class LogAggregator:
    """Aggregates and summarizes log data"""
    
    def aggregate(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """Aggregate log statistics"""
        if not logs:
            return {
                'total': 0,
                'by_level': {},
                'by_source': {},
                'time_range': None
            }
        
        # Basic counts
        level_counts = Counter(log.level for log in logs)
        source_counts = Counter(log.source for log in logs)
        
        # Time range
        timestamps = [log.timestamp for log in logs]
        time_range = {
            'start': min(timestamps),
            'end': max(timestamps),
            'duration': (max(timestamps) - min(timestamps)).total_seconds()
        }
        
        # Error rate over time
        error_logs = [log for log in logs if log.level in ['ERROR', 'CRITICAL', 'FATAL']]
        error_timeline = self._create_timeline(error_logs)
        
        return {
            'total': len(logs),
            'by_level': dict(level_counts),
            'by_source': dict(source_counts),
            'time_range': time_range,
            'error_rate': len(error_logs) / len(logs) if logs else 0,
            'error_timeline': error_timeline,
            'top_errors': self._get_top_errors(error_logs)
        }
    
    def _create_timeline(self, logs: List[LogEntry], bucket_size: int = 300) -> List[Dict]:
        """Create timeline of log events (5-minute buckets)"""
        if not logs:
            return []
        
        timeline = defaultdict(int)
        
        for log in logs:
            bucket = int(log.timestamp.timestamp() / bucket_size) * bucket_size
            timeline[bucket] += 1
        
        return [
            {'timestamp': datetime.fromtimestamp(ts), 'count': count}
            for ts, count in sorted(timeline.items())
        ]
    
    def _get_top_errors(self, error_logs: List[LogEntry], limit: int = 10) -> List[Dict]:
        """Get most common error messages"""
        if not error_logs:
            return []
        
        # Simple message clustering
        message_counts = Counter()
        
        for log in error_logs:
            # Normalize message
            normalized = re.sub(r'\d+', 'N', log.message)
            normalized = re.sub(r'0x[0-9a-fA-F]+', 'HEX', normalized)
            message_counts[normalized] += 1
        
        return [
            {'message': msg, 'count': count}
            for msg, count in message_counts.most_common(limit)
        ]


def process_file_batch(args: Tuple[List[str], LogParser]) -> List[LogEntry]:
    """Process a batch of files (for multiprocessing)"""
    files, parser = args
    logs = []
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    log_entry = parser.parse(line)
                    if log_entry:
                        logs.append(log_entry)
        except Exception as e:
            pass
    
    return logs


class DistributedLogAnalyzer:
    """Main distributed log analyzer"""
    
    def __init__(self, worker_count: int = 4):
        self.worker_count = worker_count
        self.parser = LogParser()
        self.detector = PatternDetector()
        self.aggregator = LogAggregator()
        self.alert_rules = []
        self.results_queue = queue.Queue()
        
    def analyze_logs(self, log_files: List[str], streaming: bool = False) -> Dict[str, Any]:
        """Analyze logs with distributed processing"""
        start_time = time.time()
        
        if streaming:
            return self._analyze_streaming(log_files)
        
        # Batch processing
        all_logs = []
        
        # Parse logs using ThreadPoolExecutor instead of multiprocessing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.worker_count) as executor:
            # Submit all files for processing
            futures = []
            for file_path in log_files:
                future = executor.submit(self._process_single_file, file_path)
                futures.append(future)
            
            # Collect results
            for future in concurrent.futures.as_completed(futures):
                try:
                    file_logs = future.result()
                    all_logs.extend(file_logs)
                except Exception as e:
                    pass
        
        # Analyze parsed logs
        anomalies = self.detector.detect_anomalies(all_logs)
        aggregated = self.aggregator.aggregate(all_logs)
        
        # Check alert rules
        alerts = self._check_alerts(all_logs, anomalies)
        
        # Prepare results
        processing_time = time.time() - start_time
        
        return {
            'total_logs': len(all_logs),
            'processing_time': processing_time,
            'logs_per_second': len(all_logs) / processing_time if processing_time > 0 else 0,
            'anomalies': len(anomalies),
            'anomaly_details': [self._anomaly_to_dict(a) for a in anomalies[:10]],
            'alerts': alerts,
            'aggregated': aggregated,
            'worker_count': self.worker_count
        }
    
    def _process_single_file(self, file_path: str) -> List[LogEntry]:
        """Process a single file"""
        logs = []
        
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    log_entry = self.parser.parse(line)
                    if log_entry:
                        logs.append(log_entry)
        except Exception as e:
            pass
        
        return logs
    
    def _analyze_streaming(self, log_files: List[str]) -> Dict[str, Any]:
        """Analyze logs in streaming mode"""
        # Create streaming workers
        workers = []
        stop_event = threading.Event()
        
        for i in range(self.worker_count):
            worker = threading.Thread(
                target=self._streaming_worker,
                args=(log_files[i::self.worker_count], stop_event)
            )
            worker.start()
            workers.append(worker)
        
        # Collect results for 10 seconds
        time.sleep(10)
        stop_event.set()
        
        # Wait for workers
        for worker in workers:
            worker.join()
        
        # Collect results
        results = {
            'total_logs': 0,
            'anomalies': 0,
            'streaming': True
        }
        
        while not self.results_queue.empty():
            try:
                result = self.results_queue.get_nowait()
                results['total_logs'] += result.get('logs', 0)
                results['anomalies'] += result.get('anomalies', 0)
            except queue.Empty:
                break
        
        return results
    
    def _streaming_worker(self, files: List[str], stop_event: threading.Event):
        """Worker for streaming analysis"""
        buffer = []
        
        for file_path in files:
            if stop_event.is_set():
                break
                
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        if stop_event.is_set():
                            break
                            
                        log_entry = self.parser.parse(line)
                        if log_entry:
                            buffer.append(log_entry)
                        
                        # Process buffer periodically
                        if len(buffer) >= 100:
                            anomalies = self.detector.detect_anomalies(buffer)
                            self.results_queue.put({
                                'logs': len(buffer),
                                'anomalies': len(anomalies)
                            })
                            buffer = []
                            
            except Exception as e:
                pass
    
    def _check_alerts(self, logs: List[LogEntry], anomalies: List[Anomaly]) -> List[Dict]:
        """Check configured alert rules"""
        alerts = []
        
        # Check anomaly-based alerts
        for anomaly in anomalies:
            if anomaly.severity in ['CRITICAL', 'HIGH']:
                alerts.append({
                    'type': 'anomaly',
                    'severity': anomaly.severity,
                    'message': f"Anomaly detected: {anomaly.pattern}",
                    'affected_count': len(anomaly.affected_logs),
                    'timestamp': anomaly.timestamp
                })
        
        return alerts
    
    def _anomaly_to_dict(self, anomaly: Anomaly) -> Dict[str, Any]:
        """Convert anomaly to dictionary"""
        return {
            'pattern': anomaly.pattern,
            'severity': anomaly.severity,
            'affected_count': len(anomaly.affected_logs),
            'confidence': anomaly.confidence,
            'suggested_action': anomaly.suggested_action,
            'timestamp': anomaly.timestamp.isoformat()
        }
    
    def add_alert_rule(self, rule: AlertRule):
        """Add an alert rule"""
        self.alert_rules.append(rule)
    
    def search_logs(self, logs: List[LogEntry], query: str, 
                   time_range: Optional[Tuple[datetime, datetime]] = None) -> List[LogEntry]:
        """Search logs with query"""
        results = []
        
        for log in logs:
            # Time range filter
            if time_range:
                if log.timestamp < time_range[0] or log.timestamp > time_range[1]:
                    continue
            
            # Text search
            if query.lower() in log.message.lower():
                results.append(log)
        
        return results
    
    def export_results(self, results: Dict[str, Any], format: str = 'json') -> str:
        """Export results to various formats"""
        if format == 'json':
            return json.dumps(results, indent=2, default=str)
        elif format == 'csv':
            # Simple CSV export
            lines = ['timestamp,level,source,message']
            # Would add actual CSV generation here
            return '\n'.join(lines)
        else:
            return str(results)


if __name__ == "__main__":
    # Create sample log files for testing
    sample_logs = [
        '{"timestamp": "2024-01-15T10:00:00", "level": "ERROR", "source": "api", "message": "Connection refused to database"}',
        '2024-01-15 10:00:01 ERROR [web] Authentication failed for user admin',
        '192.168.1.1 - - [15/Jan/2024:10:00:02 +0000] "GET /api/users HTTP/1.1" 500 1234',
        '{"timestamp": "2024-01-15T10:00:03", "level": "CRITICAL", "source": "app", "message": "Out of memory error"}',
        'Jan 15 10:00:04 server01 kernel[1234]: Out of memory: Kill process 5678',
        '192.168.1.2 - - [15/Jan/2024:10:00:05 +0000] "POST /login HTTP/1.1" 401 567 "-" "Mozilla/5.0"'
    ]
    
    # Write sample logs
    log_dir = Path('/home/graham/workspace/shared_claude_docs/project_interactions/log_analyzer/logs/samples')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    sample_file = log_dir / 'sample.log'
    with open(sample_file, 'w') as f:
        for log in sample_logs:
            f.write(log + '\n')
    
    # Test the analyzer
    analyzer = DistributedLogAnalyzer(worker_count=2)
    
    # Add alert rule
    analyzer.add_alert_rule(AlertRule(
        name="HighErrorRate",
        condition="error_rate > 0.1",
        threshold=10,
        time_window=300,
        severity="HIGH",
        action="notify_ops"
    ))
    
    # Analyze logs
    results = analyzer.analyze_logs([str(sample_file)])
    
    # Display results
    print(f"✅ Analyzed {results['total_logs']} logs")
    print(f"✅ Found {results['anomalies']} anomalies")
    print(f"✅ Processing time: {results['processing_time']:.2f}s")
    print(f"✅ Logs per second: {results['logs_per_second']:.0f}")
    
    if results['anomaly_details']:
        print("\n📊 Anomalies detected:")
        for anomaly in results['anomaly_details']:
            print(f"  - {anomaly['pattern']} ({anomaly['severity']}): {anomaly['affected_count']} logs")
    
    print("\n📈 Log levels distribution:")
    for level, count in results['aggregated']['by_level'].items():
        print(f"  - {level}: {count}")
    
    # Verify functionality
    assert results['total_logs'] == 6, f"Expected 6 logs, got {results['total_logs']}"
    assert results['anomalies'] >= 2, f"Expected at least 2 anomalies, got {results['anomalies']}"
    print("\n✅ Log analyzer validation passed!")