
# Security middleware import
from granger_security_middleware_simple import GrangerSecurity, SecurityConfig

# Initialize security
_security = GrangerSecurity()

"""
Module: pipeline_monitor_interaction.py
Purpose: Comprehensive data pipeline monitoring system with real-time tracking, 
         performance analysis, and automated recovery capabilities.

This module implements a Level 3 (Orchestration) interaction for monitoring
ETL pipelines, tracking data flow, detecting bottlenecks, and ensuring SLA compliance.

External Dependencies:
- None (uses standard library only for core functionality)

Example Usage:
>>> monitor = PipelineMonitor()
>>> monitor.register_pipeline('sales_etl', ['extract', 'transform', 'load'])
>>> monitor.start_monitoring('sales_etl')
>>> status = monitor.get_pipeline_status('sales_etl')
{'pipeline': 'sales_etl', 'status': 'running', 'current_stage': 'transform'}
"""

import time
import json
import threading
from datetime import datetime, timedelta
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import statistics
from pathlib import Path


class PipelineStatus(Enum):
    """Pipeline execution status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"
    RECOVERING = "recovering"


class StageStatus(Enum):
    """Individual stage status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class StageMetrics:
    """Metrics for a pipeline stage."""
    name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: StageStatus = StageStatus.PENDING
    records_processed: int = 0
    errors: int = 0
    memory_usage_mb: float = 0.0
    cpu_usage_percent: float = 0.0
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate stage duration in seconds."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None
    
    @property
    def throughput(self) -> Optional[float]:
        """Calculate records per second."""
        duration = self.duration_seconds
        if duration and duration > 0:
            return self.records_processed / duration
        return None


@dataclass
class PipelineRun:
    """Individual pipeline execution run."""
    run_id: str
    pipeline_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: PipelineStatus = PipelineStatus.RUNNING
    stages: Dict[str, StageMetrics] = field(default_factory=dict)
    alerts: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate total pipeline duration."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        elif self.start_time:
            return (datetime.now() - self.start_time).total_seconds()
        return None
    
    @property
    def total_records(self) -> int:
        """Calculate total records processed."""
        return sum(stage.records_processed for stage in self.stages.values())
    
    @property
    def total_errors(self) -> int:
        """Calculate total errors across all stages."""
        return sum(stage.errors for stage in self.stages.values())


@dataclass
class PipelineConfig:
    """Pipeline configuration."""
    name: str
    stages: List[str]
    dependencies: List[str] = field(default_factory=list)
    sla_minutes: int = 60
    max_retries: int = 3
    alert_thresholds: Dict[str, float] = field(default_factory=dict)
    recovery_actions: List[str] = field(default_factory=list)


class PipelineMonitor:
    """Comprehensive pipeline monitoring system."""
    
    def __init__(self, history_size: int = 1000):
        """Initialize pipeline monitor.
        
        Args:
            history_size: Number of historical runs to keep per pipeline
        """
        self.pipelines: Dict[str, PipelineConfig] = {}
        self.active_runs: Dict[str, PipelineRun] = {}
        self.run_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=history_size))
        self.alert_handlers: List[Callable] = []
        self.monitoring_threads: Dict[str, threading.Thread] = {}
        self._lock = threading.Lock()
        self._run_counter = 0
        
        # Performance tracking
        self.stage_performance: Dict[str, List[float]] = defaultdict(list)
        self.pipeline_performance: Dict[str, List[float]] = defaultdict(list)
        
        # Resource utilization tracking
        self.resource_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
    def register_pipeline(self, name: str, stages: List[str], 
                         dependencies: Optional[List[str]] = None,
                         sla_minutes: int = 60,
                         alert_thresholds: Optional[Dict[str, float]] = None) -> None:
        """Register a new pipeline for monitoring.
        
        Args:
            name: Pipeline name
            stages: List of stage names in order
            dependencies: Other pipelines this depends on
            sla_minutes: SLA time in minutes
            alert_thresholds: Alert threshold configuration
        """
        config = PipelineConfig(
            name=name,
            stages=stages,
            dependencies=dependencies or [],
            sla_minutes=sla_minutes,
            alert_thresholds=alert_thresholds or {
                'error_rate': 0.05,  # 5% error rate
                'duration_multiplier': 2.0,  # 2x average duration
                'memory_usage_mb': 1024,  # 1GB
                'cpu_usage_percent': 80  # 80% CPU
            }
        )
        
        with self._lock:
            self.pipelines[name] = config
    
    def start_monitoring(self, pipeline_name: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Start monitoring a pipeline execution.
        
        Args:
            pipeline_name: Name of the pipeline to monitor
            metadata: Optional metadata for this run
            
        Returns:
            Run ID for this execution
        """
        if pipeline_name not in self.pipelines:
            raise ValueError(f"Pipeline '{pipeline_name}' not registered")
        
        with self._lock:
            self._run_counter += 1
            run_id = f"{pipeline_name}_{self._run_counter:06d}"
            
            config = self.pipelines[pipeline_name]
            run = PipelineRun(
                run_id=run_id,
                pipeline_name=pipeline_name,
                start_time=datetime.now(),
                metadata=metadata or {}
            )
            
            # Initialize stage metrics
            for stage in config.stages:
                run.stages[stage] = StageMetrics(name=stage)
            
            self.active_runs[run_id] = run
            
            # Start monitoring thread
            thread = threading.Thread(
                target=self._monitor_pipeline,
                args=(run_id,),
                daemon=True
            )
            thread.start()
            self.monitoring_threads[run_id] = thread
            
        return run_id
    
    def update_stage(self, run_id: str, stage_name: str, 
                    status: Optional[StageStatus] = None,
                    records_processed: Optional[int] = None,
                    errors: Optional[int] = None,
                    memory_usage_mb: Optional[float] = None,
                    cpu_usage_percent: Optional[float] = None) -> None:
        """Update stage metrics.
        
        Args:
            run_id: Pipeline run ID
            stage_name: Stage name to update
            status: New stage status
            records_processed: Number of records processed
            errors: Number of errors
            memory_usage_mb: Memory usage in MB
            cpu_usage_percent: CPU usage percentage
        """
        with self._lock:
            if run_id not in self.active_runs:
                return
            
            run = self.active_runs[run_id]
            if stage_name not in run.stages:
                return
            
            stage = run.stages[stage_name]
            
            # Update status and timestamps
            if status:
                old_status = stage.status
                stage.status = status
                
                if status == StageStatus.RUNNING and old_status == StageStatus.PENDING:
                    stage.start_time = datetime.now()
                elif status in [StageStatus.COMPLETED, StageStatus.FAILED]:
                    stage.end_time = datetime.now()
            
            # Update metrics
            if records_processed is not None:
                stage.records_processed = records_processed
            if errors is not None:
                stage.errors = errors
            if memory_usage_mb is not None:
                stage.memory_usage_mb = memory_usage_mb
            if cpu_usage_percent is not None:
                stage.cpu_usage_percent = cpu_usage_percent
            
            # Check thresholds and generate alerts
            self._check_stage_thresholds(run_id, stage_name)
    
    def complete_pipeline(self, run_id: str, status: PipelineStatus) -> None:
        """Mark pipeline as completed.
        
        Args:
            run_id: Pipeline run ID
            status: Final pipeline status
        """
        with self._lock:
            if run_id not in self.active_runs:
                return
            
            run = self.active_runs[run_id]
            run.end_time = datetime.now()
            run.status = status
            
            # Move to history
            self.run_history[run.pipeline_name].append(run)
            
            # Update performance metrics
            if run.duration_seconds:
                self.pipeline_performance[run.pipeline_name].append(run.duration_seconds)
            
            for stage_name, stage in run.stages.items():
                if stage.duration_seconds:
                    key = f"{run.pipeline_name}.{stage_name}"
                    self.stage_performance[key].append(stage.duration_seconds)
            
            # Check SLA compliance
            self._check_sla_compliance(run_id)
            
            # Clean up
            del self.active_runs[run_id]
            if run_id in self.monitoring_threads:
                del self.monitoring_threads[run_id]
    
    def get_pipeline_status(self, pipeline_name: str) -> Dict[str, Any]:
        """Get current status of a pipeline.
        
        Args:
            pipeline_name: Pipeline name
            
        Returns:
            Current pipeline status information
        """
        with self._lock:
            # Find active run for this pipeline
            active_run = None
            for run in self.active_runs.values():
                if run.pipeline_name == pipeline_name:
                    active_run = run
                    break
            
            if not active_run:
                # Get last run from history
                history = self.run_history.get(pipeline_name, [])
                if history:
                    last_run = history[-1]
                    return {
                        'pipeline': pipeline_name,
                        'status': 'idle',
                        'last_run': {
                            'run_id': last_run.run_id,
                            'status': last_run.status.value,
                            'duration_seconds': last_run.duration_seconds,
                            'total_records': last_run.total_records,
                            'total_errors': last_run.total_errors
                        }
                    }
                return {'pipeline': pipeline_name, 'status': 'idle'}
            
            # Get current stage
            current_stage = None
            for stage_name, stage in active_run.stages.items():
                if stage.status == StageStatus.RUNNING:
                    current_stage = stage_name
                    break
            
            return {
                'pipeline': pipeline_name,
                'status': active_run.status.value,
                'run_id': active_run.run_id,
                'current_stage': current_stage,
                'duration_seconds': active_run.duration_seconds,
                'stages': {
                    name: {
                        'status': stage.status.value,
                        'records_processed': stage.records_processed,
                        'errors': stage.errors,
                        'duration_seconds': stage.duration_seconds
                    }
                    for name, stage in active_run.stages.items()
                }
            }
    
    def get_performance_analysis(self, pipeline_name: str) -> Dict[str, Any]:
        """Analyze pipeline performance.
        
        Args:
            pipeline_name: Pipeline name
            
        Returns:
            Performance analysis results
        """
        with self._lock:
            history = list(self.run_history.get(pipeline_name, []))
            
            if not history:
                return {'pipeline': pipeline_name, 'error': 'No historical data'}
            
            # Calculate statistics
            durations = [run.duration_seconds for run in history if run.duration_seconds]
            success_rate = len([r for r in history if r.status == PipelineStatus.COMPLETED]) / len(history)
            
            # Stage-level analysis
            stage_stats = {}
            for stage_name in self.pipelines[pipeline_name].stages:
                key = f"{pipeline_name}.{stage_name}"
                stage_durations = self.stage_performance.get(key, [])
                if stage_durations:
                    stage_stats[stage_name] = {
                        'avg_duration': statistics.mean(stage_durations),
                        'min_duration': min(stage_durations),
                        'max_duration': max(stage_durations),
                        'p95_duration': self._calculate_percentile(stage_durations, 95)
                    }
            
            # Identify bottlenecks
            bottlenecks = self._identify_bottlenecks(pipeline_name)
            
            return {
                'pipeline': pipeline_name,
                'total_runs': len(history),
                'success_rate': success_rate,
                'performance': {
                    'avg_duration': statistics.mean(durations) if durations else 0,
                    'min_duration': min(durations) if durations else 0,
                    'max_duration': max(durations) if durations else 0,
                    'p95_duration': self._calculate_percentile(durations, 95) if durations else 0
                },
                'stage_stats': stage_stats,
                'bottlenecks': bottlenecks,
                'trends': self._calculate_trends(pipeline_name)
            }
    
    def get_data_lineage(self, pipeline_name: str, run_id: Optional[str] = None) -> Dict[str, Any]:
        """Track data lineage through pipeline stages.
        
        Args:
            pipeline_name: Pipeline name
            run_id: Optional specific run ID
            
        Returns:
            Data lineage information
        """
        with self._lock:
            if run_id:
                run = self.active_runs.get(run_id)
                if not run:
                    history = self.run_history.get(pipeline_name, [])
                    run = next((r for r in history if r.run_id == run_id), None)
                
                if not run:
                    return {'error': f'Run {run_id} not found'}
            else:
                # Get latest run
                history = self.run_history.get(pipeline_name, [])
                if not history:
                    return {'pipeline': pipeline_name, 'error': 'No runs found'}
                run = history[-1]
            
            lineage = {
                'pipeline': pipeline_name,
                'run_id': run.run_id,
                'start_time': run.start_time.isoformat(),
                'stages': []
            }
            
            for stage_name in self.pipelines[pipeline_name].stages:
                stage = run.stages.get(stage_name)
                if stage:
                    lineage['stages'].append({
                        'name': stage_name,
                        'status': stage.status.value,
                        'records_in': stage.records_processed,
                        'records_out': stage.records_processed - stage.errors,
                        'errors': stage.errors,
                        'start_time': stage.start_time.isoformat() if stage.start_time else None,
                        'end_time': stage.end_time.isoformat() if stage.end_time else None
                    })
            
            # Add dependencies
            config = self.pipelines[pipeline_name]
            if config.dependencies:
                lineage['dependencies'] = config.dependencies
            
            return lineage
    
    def configure_alerts(self, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Configure alert handler.
        
        Args:
            handler: Function to handle alerts
        """
        self.alert_handlers.append(handler)
    
    def get_optimization_suggestions(self, pipeline_name: str) -> List[Dict[str, Any]]:
        """Generate optimization suggestions for a pipeline.
        
        Args:
            pipeline_name: Pipeline name
            
        Returns:
            List of optimization suggestions
        """
        suggestions = []
        
        with self._lock:
            history = list(self.run_history.get(pipeline_name, []))
            if len(history) < 5:
                return [{'type': 'info', 'message': 'Need more historical data for suggestions'}]
            
            # Analyze recent performance
            recent_runs = history[-10:]
            
            # Check for increasing duration trend
            durations = [r.duration_seconds for r in recent_runs if r.duration_seconds]
            if durations and self._is_increasing_trend(durations):
                suggestions.append({
                    'type': 'performance',
                    'severity': 'warning',
                    'message': 'Pipeline duration is increasing over time',
                    'suggestion': 'Review recent changes and consider scaling resources'
                })
            
            # Check for high error rates
            error_rates = [r.total_errors / max(r.total_records, 1) for r in recent_runs]
            avg_error_rate = statistics.mean(error_rates)
            if avg_error_rate > 0.05:
                suggestions.append({
                    'type': 'reliability',
                    'severity': 'error',
                    'message': f'High error rate: {avg_error_rate:.1%}',
                    'suggestion': 'Investigate data quality issues and add validation'
                })
            
            # Check for resource bottlenecks
            bottlenecks = self._identify_bottlenecks(pipeline_name)
            for bottleneck in bottlenecks:
                suggestions.append({
                    'type': 'bottleneck',
                    'severity': 'warning',
                    'stage': bottleneck['stage'],
                    'message': f"Stage '{bottleneck['stage']}' is a bottleneck",
                    'suggestion': bottleneck['suggestion']
                })
            
            # Check for underutilized stages
            for stage_name in self.pipelines[pipeline_name].stages:
                key = f"{pipeline_name}.{stage_name}"
                stage_durations = self.stage_performance.get(key, [])
                if stage_durations and statistics.mean(stage_durations) < 1.0:
                    suggestions.append({
                        'type': 'efficiency',
                        'severity': 'info',
                        'stage': stage_name,
                        'message': f"Stage '{stage_name}' completes very quickly",
                        'suggestion': 'Consider merging with adjacent stages'
                    })
        
        return suggestions
    
    def trigger_recovery_action(self, run_id: str, action: str) -> bool:
        """Trigger a recovery action for a failed pipeline.
        
        Args:
            run_id: Pipeline run ID
            action: Recovery action to trigger
            
        Returns:
            True if action was triggered successfully
        """
        with self._lock:
            run = self.active_runs.get(run_id)
            if not run:
                return False
            
            run.status = PipelineStatus.RECOVERING
            self._send_alert({
                'severity': AlertSeverity.INFO.value,
                'pipeline': run.pipeline_name,
                'run_id': run_id,
                'message': f'Recovery action triggered: {action}',
                'timestamp': datetime.now().isoformat()
            })
            
            # Simulate recovery action
            # In real implementation, this would trigger actual recovery
            return True
    
    def export_dashboard_data(self) -> Dict[str, Any]:
        """Export data for dashboard visualization.
        
        Returns:
            Dashboard data including metrics, status, and trends
        """
        with self._lock:
            dashboard = {
                'timestamp': datetime.now().isoformat(),
                'pipelines': [],
                'active_runs': len(self.active_runs),
                'alerts': []
            }
            
            # Aggregate pipeline data
            for pipeline_name, config in self.pipelines.items():
                status = self.get_pipeline_status(pipeline_name)
                perf = self.get_performance_analysis(pipeline_name)
                
                pipeline_data = {
                    'name': pipeline_name,
                    'status': status.get('status', 'idle'),
                    'stages': len(config.stages),
                    'sla_minutes': config.sla_minutes
                }
                
                if 'performance' in perf:
                    pipeline_data['avg_duration'] = perf['performance']['avg_duration']
                    pipeline_data['success_rate'] = perf.get('success_rate', 0)
                
                dashboard['pipelines'].append(pipeline_data)
            
            # Recent alerts
            for run in self.active_runs.values():
                dashboard['alerts'].extend(run.alerts[-5:])  # Last 5 alerts per run
            
            return dashboard
    
    # Private methods
    
    def _monitor_pipeline(self, run_id: str) -> None:
        """Monitor pipeline execution (runs in separate thread).
        
        Args:
            run_id: Pipeline run ID
        """
        while run_id in self.active_runs:
            with self._lock:
                run = self.active_runs.get(run_id)
                if not run:
                    break
                
                # Check for timeouts
                if run.duration_seconds and run.duration_seconds > self.pipelines[run.pipeline_name].sla_minutes * 60:
                    self._send_alert({
                        'severity': AlertSeverity.ERROR.value,
                        'pipeline': run.pipeline_name,
                        'run_id': run_id,
                        'message': 'Pipeline exceeded SLA',
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Monitor resource usage
                total_memory = sum(s.memory_usage_mb for s in run.stages.values())
                avg_cpu = statistics.mean([s.cpu_usage_percent for s in run.stages.values() if s.cpu_usage_percent > 0] or [0])
                
                self.resource_history[run.pipeline_name].append({
                    'timestamp': datetime.now(),
                    'memory_mb': total_memory,
                    'cpu_percent': avg_cpu
                })
            
            time.sleep(5)  # Check every 5 seconds
    
    def _check_stage_thresholds(self, run_id: str, stage_name: str) -> None:
        """Check if stage metrics exceed thresholds.
        
        Args:
            run_id: Pipeline run ID
            stage_name: Stage name
        """
        run = self.active_runs.get(run_id)
        if not run:
            return
        
        stage = run.stages.get(stage_name)
        if not stage:
            return
        
        config = self.pipelines[run.pipeline_name]
        thresholds = config.alert_thresholds
        
        # Check error rate
        if stage.records_processed > 0:
            error_rate = stage.errors / stage.records_processed
            if error_rate > thresholds.get('error_rate', 0.05):
                self._send_alert({
                    'severity': AlertSeverity.WARNING.value,
                    'pipeline': run.pipeline_name,
                    'run_id': run_id,
                    'stage': stage_name,
                    'message': f'High error rate: {error_rate:.1%}',
                    'timestamp': datetime.now().isoformat()
                })
        
        # Check resource usage
        if stage.memory_usage_mb > thresholds.get('memory_usage_mb', 1024):
            self._send_alert({
                'severity': AlertSeverity.WARNING.value,
                'pipeline': run.pipeline_name,
                'run_id': run_id,
                'stage': stage_name,
                'message': f'High memory usage: {stage.memory_usage_mb:.0f}MB',
                'timestamp': datetime.now().isoformat()
            })
        
        if stage.cpu_usage_percent > thresholds.get('cpu_usage_percent', 80):
            self._send_alert({
                'severity': AlertSeverity.WARNING.value,
                'pipeline': run.pipeline_name,
                'run_id': run_id,
                'stage': stage_name,
                'message': f'High CPU usage: {stage.cpu_usage_percent:.0f}%',
                'timestamp': datetime.now().isoformat()
            })
    
    def _check_sla_compliance(self, run_id: str) -> None:
        """Check if pipeline met SLA requirements.
        
        Args:
            run_id: Pipeline run ID
        """
        history = []
        for runs in self.run_history.values():
            for run in runs:
                if run.run_id == run_id:
                    history = runs
                    break
        
        if not history:
            return
        
        run = history[-1]
        config = self.pipelines[run.pipeline_name]
        
        if run.duration_seconds and run.duration_seconds > config.sla_minutes * 60:
            self._send_alert({
                'severity': AlertSeverity.CRITICAL.value,
                'pipeline': run.pipeline_name,
                'run_id': run_id,
                'message': f'SLA violated: {run.duration_seconds/60:.1f} minutes (SLA: {config.sla_minutes} minutes)',
                'timestamp': datetime.now().isoformat()
            })
    
    def _identify_bottlenecks(self, pipeline_name: str) -> List[Dict[str, Any]]:
        """Identify performance bottlenecks in pipeline.
        
        Args:
            pipeline_name: Pipeline name
            
        Returns:
            List of bottlenecks with suggestions
        """
        bottlenecks = []
        
        # Analyze stage durations
        total_duration = sum(
            statistics.mean(self.stage_performance.get(f"{pipeline_name}.{stage}", [0]))
            for stage in self.pipelines[pipeline_name].stages
        )
        
        if total_duration == 0:
            return bottlenecks
        
        for stage_name in self.pipelines[pipeline_name].stages:
            key = f"{pipeline_name}.{stage_name}"
            stage_durations = self.stage_performance.get(key, [])
            
            if not stage_durations:
                continue
            
            avg_duration = statistics.mean(stage_durations)
            percentage = (avg_duration / total_duration) * 100
            
            if percentage > 40:  # Stage takes more than 40% of total time
                bottlenecks.append({
                    'stage': stage_name,
                    'percentage': percentage,
                    'avg_duration': avg_duration,
                    'suggestion': f'Optimize or parallelize {stage_name} stage'
                })
        
        return sorted(bottlenecks, key=lambda x: x['percentage'], reverse=True)
    
    def _calculate_trends(self, pipeline_name: str) -> Dict[str, str]:
        """Calculate performance trends.
        
        Args:
            pipeline_name: Pipeline name
            
        Returns:
            Trend analysis results
        """
        history = list(self.run_history.get(pipeline_name, []))
        if len(history) < 10:
            return {'status': 'insufficient_data'}
        
        recent = history[-5:]
        older = history[-10:-5]
        
        recent_avg = statistics.mean([r.duration_seconds for r in recent if r.duration_seconds] or [0])
        older_avg = statistics.mean([r.duration_seconds for r in older if r.duration_seconds] or [0])
        
        if older_avg == 0:
            return {'status': 'no_baseline'}
        
        change = ((recent_avg - older_avg) / older_avg) * 100
        
        if change > 10:
            return {'status': 'degrading', 'change_percent': change}
        elif change < -10:
            return {'status': 'improving', 'change_percent': change}
        else:
            return {'status': 'stable', 'change_percent': change}
    
    def _calculate_percentile(self, values: List[float], percentile: float) -> float:
        """Calculate percentile value.
        
        Args:
            values: List of values
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not values:
            return 0.0
        
        sorted_values = sorted(values)
        index = int((percentile / 100) * len(sorted_values))
        return sorted_values[min(index, len(sorted_values) - 1)]
    
    def _is_increasing_trend(self, values: List[float]) -> bool:
        """Check if values show increasing trend.
        
        Args:
            values: List of values
            
        Returns:
            True if trend is increasing
        """
        if len(values) < 3:
            return False
        
        # Simple trend detection - compare first half with second half
        mid = len(values) // 2
        first_half_avg = statistics.mean(values[:mid])
        second_half_avg = statistics.mean(values[mid:])
        
        return second_half_avg > first_half_avg * 1.1  # 10% increase
    
    def _send_alert(self, alert: Dict[str, Any]) -> None:
        """Send alert to configured handlers.
        
        Args:
            alert: Alert information
        """
        # Add to run alerts
        run_id = alert.get('run_id')
        if run_id and run_id in self.active_runs:
            self.active_runs[run_id].alerts.append(alert)
        
        # Send to handlers
        for handler in self.alert_handlers:
            try:
                handler(alert)
            except Exception:
                pass  # Don't let handler errors affect monitoring


if __name__ == "__main__":
    # Validation with real-world pipeline simulation
    print("=== Pipeline Monitor Validation ===\n")
    
    # Create monitor
    monitor = PipelineMonitor()
    
    # Register a sample ETL pipeline
    monitor.register_pipeline(
        'sales_etl',
        stages=['extract', 'validate', 'transform', 'load'],
        sla_minutes=30,
        alert_thresholds={
            'error_rate': 0.05,
            'memory_usage_mb': 512,
            'cpu_usage_percent': 75
        }
    )
    
    # Configure alert handler
    alerts_received = []
    monitor.configure_alerts(lambda alert: alerts_received.append(alert))
    
    # Start monitoring
    run_id = monitor.start_monitoring('sales_etl', {'source': 'daily_batch'})
    print(f"Started monitoring run: {run_id}")
    
    # Simulate pipeline execution
    print("\nSimulating pipeline execution...")
    
    # Extract stage
    monitor.update_stage(run_id, 'extract', StageStatus.RUNNING)
    time.sleep(0.5)
    monitor.update_stage(run_id, 'extract', 
                        status=StageStatus.COMPLETED,
                        records_processed=10000,
                        errors=0,
                        memory_usage_mb=128,
                        cpu_usage_percent=45)
    
    # Validate stage
    monitor.update_stage(run_id, 'validate', StageStatus.RUNNING)
    time.sleep(0.3)
    monitor.update_stage(run_id, 'validate',
                        status=StageStatus.COMPLETED,
                        records_processed=10000,
                        errors=150,  # Some validation errors
                        memory_usage_mb=96,
                        cpu_usage_percent=30)
    
    # Transform stage
    monitor.update_stage(run_id, 'transform', StageStatus.RUNNING)
    time.sleep(0.7)
    monitor.update_stage(run_id, 'transform',
                        status=StageStatus.COMPLETED,
                        records_processed=9850,
                        errors=0,
                        memory_usage_mb=256,
                        cpu_usage_percent=65)
    
    # Load stage
    monitor.update_stage(run_id, 'load', StageStatus.RUNNING)
    time.sleep(0.4)
    monitor.update_stage(run_id, 'load',
                        status=StageStatus.COMPLETED,
                        records_processed=9850,
                        errors=0,
                        memory_usage_mb=192,
                        cpu_usage_percent=55)
    
    # Complete pipeline
    monitor.complete_pipeline(run_id, PipelineStatus.COMPLETED)
    
    # Get status
    print("\n=== Pipeline Status ===")
    status = monitor.get_pipeline_status('sales_etl')
    print(f"Status: {json.dumps(status, indent=2)}")
    
    # Run another pipeline for performance analysis
    print("\n\nRunning additional pipelines for analysis...")
    for i in range(3):
        run_id2 = monitor.start_monitoring('sales_etl')
        for stage in ['extract', 'validate', 'transform', 'load']:
            monitor.update_stage(run_id2, stage, StageStatus.RUNNING)
            time.sleep(0.1)
            monitor.update_stage(run_id2, stage,
                               status=StageStatus.COMPLETED,
                               records_processed=10000 + i * 1000,
                               errors=i * 50,
                               memory_usage_mb=200 + i * 50,
                               cpu_usage_percent=50 + i * 10)
        monitor.complete_pipeline(run_id2, PipelineStatus.COMPLETED)
    
    # Get performance analysis
    print("\n=== Performance Analysis ===")
    analysis = monitor.get_performance_analysis('sales_etl')
    print(f"Total runs: {analysis['total_runs']}")
    print(f"Success rate: {analysis['success_rate']:.1%}")
    print(f"Average duration: {analysis['performance']['avg_duration']:.2f}s")
    
    # Get data lineage
    print("\n=== Data Lineage ===")
    lineage = monitor.get_data_lineage('sales_etl')
    print(f"Pipeline: {lineage['pipeline']}")
    print(f"Stages processed: {len(lineage['stages'])}")
    
    # Get optimization suggestions
    print("\n=== Optimization Suggestions ===")
    suggestions = monitor.get_optimization_suggestions('sales_etl')
    for suggestion in suggestions:
        severity = suggestion.get('severity', 'info')
        print(f"- [{severity}] {suggestion['message']}")
        print(f"  Suggestion: {suggestion['suggestion']}")
    
    # Export dashboard data
    print("\n=== Dashboard Data ===")
    dashboard = monitor.export_dashboard_data()
    print(f"Active runs: {dashboard['active_runs']}")
    print(f"Total pipelines: {len(dashboard['pipelines'])}")
    
    # Check alerts
    print(f"\n=== Alerts Received ===")
    print(f"Total alerts: {len(alerts_received)}")
    for alert in alerts_received[:3]:  # Show first 3
        print(f"- [{alert['severity']}] {alert['message']}")
    
    print("\n✅ Pipeline Monitor validation completed successfully!")