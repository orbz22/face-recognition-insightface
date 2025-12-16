"""
Performance Monitor untuk Face Recognition System
Track CPU, Memory, FPS, dan inference time
"""

import time
import psutil
import threading
from typing import Dict, List, Optional
from collections import deque


class PerformanceMonitor:
    """Monitor performa sistem real-time"""
    
    def __init__(self, window_size: int = 30):
        """
        Args:
            window_size: Jumlah sample untuk moving average (default: 30)
        """
        self.window_size = window_size
        
        # Metrics storage (moving window)
        self.fps_samples = deque(maxlen=window_size)
        self.inference_times = deque(maxlen=window_size)
        self.frame_times = deque(maxlen=window_size)
        
        # Timestamps
        self.last_frame_time = None
        self.start_time = time.time()
        
        # Process info
        self.process = psutil.Process()
        
        # Stats
        self.total_frames = 0
        self.total_inferences = 0
        
    def start_frame(self):
        """Mark start of frame processing"""
        self.last_frame_time = time.time()
        
    def end_frame(self):
        """Mark end of frame processing and calculate FPS"""
        if self.last_frame_time is not None:
            frame_time = time.time() - self.last_frame_time
            self.frame_times.append(frame_time)
            
            # Calculate FPS
            if frame_time > 0:
                fps = 1.0 / frame_time
                self.fps_samples.append(fps)
            
            self.total_frames += 1
            
    def record_inference_time(self, inference_time: float):
        """Record inference time (in seconds)"""
        self.inference_times.append(inference_time)
        self.total_inferences += 1
        
    def get_cpu_usage(self) -> float:
        """Get current CPU usage (%)"""
        try:
            return self.process.cpu_percent(interval=0.1)
        except:
            return 0.0
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get current memory usage"""
        try:
            mem_info = self.process.memory_info()
            return {
                'rss_mb': mem_info.rss / 1024 / 1024,  # Resident Set Size in MB
                'vms_mb': mem_info.vms / 1024 / 1024,  # Virtual Memory Size in MB
                'percent': self.process.memory_percent()
            }
        except:
            return {'rss_mb': 0, 'vms_mb': 0, 'percent': 0}
    
    def get_fps(self) -> float:
        """Get average FPS"""
        if len(self.fps_samples) == 0:
            return 0.0
        return sum(self.fps_samples) / len(self.fps_samples)
    
    def get_avg_inference_time(self) -> float:
        """Get average inference time (ms)"""
        if len(self.inference_times) == 0:
            return 0.0
        return (sum(self.inference_times) / len(self.inference_times)) * 1000  # Convert to ms
    
    def get_avg_frame_time(self) -> float:
        """Get average frame processing time (ms)"""
        if len(self.frame_times) == 0:
            return 0.0
        return (sum(self.frame_times) / len(self.frame_times)) * 1000  # Convert to ms
    
    def get_uptime(self) -> float:
        """Get uptime in seconds"""
        return time.time() - self.start_time
    
    def get_stats(self) -> Dict:
        """Get all performance stats"""
        mem = self.get_memory_usage()
        uptime = self.get_uptime()
        
        return {
            'fps': round(self.get_fps(), 2),
            'avg_inference_ms': round(self.get_avg_inference_time(), 2),
            'avg_frame_ms': round(self.get_avg_frame_time(), 2),
            'cpu_percent': round(self.get_cpu_usage(), 2),
            'memory_mb': round(mem['rss_mb'], 2),
            'memory_percent': round(mem['percent'], 2),
            'total_frames': self.total_frames,
            'total_inferences': self.total_inferences,
            'uptime_seconds': round(uptime, 2),
            'uptime_formatted': self._format_uptime(uptime)
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """Format uptime as HH:MM:SS"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def print_stats(self):
        """Print current stats to console"""
        stats = self.get_stats()
        
        print("\n" + "="*50)
        print("  PERFORMANCE MONITOR")
        print("="*50)
        print(f"FPS:              {stats['fps']:.2f}")
        print(f"Frame Time:       {stats['avg_frame_ms']:.2f} ms")
        print(f"Inference Time:   {stats['avg_inference_ms']:.2f} ms")
        print(f"CPU Usage:        {stats['cpu_percent']:.2f}%")
        print(f"Memory Usage:     {stats['memory_mb']:.2f} MB ({stats['memory_percent']:.2f}%)")
        print(f"Total Frames:     {stats['total_frames']}")
        print(f"Total Inferences: {stats['total_inferences']}")
        print(f"Uptime:           {stats['uptime_formatted']}")
        print("="*50)
    
    def get_stats_string(self) -> str:
        """Get stats as formatted string for overlay"""
        stats = self.get_stats()
        
        lines = [
            f"FPS: {stats['fps']:.1f}",
            f"Frame: {stats['avg_frame_ms']:.1f}ms",
            f"Inference: {stats['avg_inference_ms']:.1f}ms",
            f"CPU: {stats['cpu_percent']:.1f}%",
            f"RAM: {stats['memory_mb']:.0f}MB"
        ]
        
        return " | ".join(lines)
    
    def reset(self):
        """Reset all metrics"""
        self.fps_samples.clear()
        self.inference_times.clear()
        self.frame_times.clear()
        self.total_frames = 0
        self.total_inferences = 0
        self.start_time = time.time()


class PerformanceLogger:
    """Log performance metrics to file"""
    
    def __init__(self, log_file: str = "logs/performance.log"):
        """
        Args:
            log_file: Path to performance log file
        """
        self.log_file = log_file
        self._ensure_log_dir()
        
        # Write header
        with open(self.log_file, 'w') as f:
            f.write("timestamp,fps,frame_ms,inference_ms,cpu_percent,memory_mb,memory_percent\n")
    
    def _ensure_log_dir(self):
        """Ensure log directory exists"""
        import os
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def log(self, monitor: PerformanceMonitor):
        """Log current stats"""
        stats = monitor.get_stats()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        line = f"{timestamp},{stats['fps']},{stats['avg_frame_ms']},{stats['avg_inference_ms']}," \
               f"{stats['cpu_percent']},{stats['memory_mb']},{stats['memory_percent']}\n"
        
        with open(self.log_file, 'a') as f:
            f.write(line)


# Example usage
if __name__ == "__main__":
    import cv2
    
    # Create monitor
    monitor = PerformanceMonitor()
    
    # Simulate processing
    print("Simulating face recognition processing...")
    print("Press Ctrl+C to stop\n")
    
    try:
        for i in range(100):
            # Start frame
            monitor.start_frame()
            
            # Simulate inference
            inference_start = time.time()
            time.sleep(0.03)  # Simulate 30ms inference
            inference_time = time.time() - inference_start
            monitor.record_inference_time(inference_time)
            
            # Simulate frame processing
            time.sleep(0.01)  # Simulate 10ms other processing
            
            # End frame
            monitor.end_frame()
            
            # Print stats every 30 frames
            if (i + 1) % 30 == 0:
                monitor.print_stats()
        
        print("\nFinal stats:")
        monitor.print_stats()
        
    except KeyboardInterrupt:
        print("\n\nStopped by user")
        monitor.print_stats()
