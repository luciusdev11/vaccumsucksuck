"""
Fast Greedy Nearest Neighbor algorithm for large boards
"""

import time
from typing import Set
from app.models import State, Action, SearchResult


def greedy_nearest_neighbor(initial_state: State, grid_size: int, progress=None) -> SearchResult:
    """
    Greedy Nearest Neighbor - Fast non-optimal algorithm
    
    Always moves to the nearest dirt cell and sucks it.
    Guaranteed to complete quickly even on large boards.
    Time complexity: O(k²·n²) where k=dirt count, n=grid size.
    """
    start_time = time.time()
    
    current_pos = initial_state.robot_pos
    remaining_dirt = set(initial_state.dirt_set)
    path = []
    nodes_expanded = 0
    
    while remaining_dirt:
        # Find nearest dirt using Manhattan distance
        nearest_dirt = None
        min_distance = float('inf')
        
        for dirt_pos in remaining_dirt:
            distance = abs(current_pos[0] - dirt_pos[0]) + abs(current_pos[1] - dirt_pos[1])
            if distance < min_distance:
                min_distance = distance
                nearest_dirt = dirt_pos
        
        # Move to nearest dirt using simple Manhattan pathfinding
        target_x, target_y = nearest_dirt
        curr_x, curr_y = current_pos
        
        # Move horizontally first, then vertically
        while curr_x != target_x:
            if curr_x < target_x:
                path.append(Action.RIGHT)
                curr_x += 1
            else:
                path.append(Action.LEFT)
                curr_x -= 1
            nodes_expanded += 1
        
        while curr_y != target_y:
            if curr_y < target_y:
                path.append(Action.DOWN)
                curr_y += 1
            else:
                path.append(Action.UP)
                curr_y -= 1
            nodes_expanded += 1
        
        # Suck the dirt
        path.append(Action.SUCK)
        nodes_expanded += 1
        remaining_dirt.remove(nearest_dirt)
        current_pos = (curr_x, curr_y)
        
        # Update progress
        if progress:
            progress.update(nodes_expanded, len(remaining_dirt))
    
    return SearchResult(
        path=path,
        nodes_expanded=nodes_expanded,
        time_taken=time.time() - start_time,
        memory_used=len(initial_state.dirt_set),
        success=True,
        algorithm_name="Greedy NN"
    )
