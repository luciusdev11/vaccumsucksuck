"""
Search progress tracking for thread-safe communication between search algorithms and GUI
"""

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchProgress:
    """Thread-safe container for search algorithm progress"""
    
    def __init__(self):
        self.lock = threading.Lock()
        self.nodes_explored = 0
        self.frontier_size = 0
        self.max_frontier_size = 0
        self.time_elapsed = 0.0
        self.algorithm_name = ""
        self.is_active = False
        self.start_time = 0.0
    
    def start(self, algorithm_name: str):
        """Start tracking for a new search"""
        with self.lock:
            self.nodes_explored = 0
            self.frontier_size = 0
            self.max_frontier_size = 0
            self.time_elapsed = 0.0
            self.algorithm_name = algorithm_name
            self.is_active = True
            self.start_time = time.time()
    
    def update(self, nodes_explored: int, frontier_size: int):
        """Update progress (called from search thread)"""
        with self.lock:
            self.nodes_explored = nodes_explored
            self.frontier_size = frontier_size
            self.max_frontier_size = max(self.max_frontier_size, frontier_size)
            self.time_elapsed = time.time() - self.start_time
    
    def stop(self):
        """Mark search as complete"""
        with self.lock:
            self.is_active = False
    
    def get_snapshot(self) -> dict:
        """Get current progress safely (called from GUI thread)"""
        with self.lock:
            return {
                'nodes_explored': self.nodes_explored,
                'frontier_size': self.frontier_size,
                'max_frontier_size': self.max_frontier_size,
                'time_elapsed': self.time_elapsed,
                'algorithm_name': self.algorithm_name,
                'is_active': self.is_active
            }
