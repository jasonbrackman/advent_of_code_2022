from __future__ import annotations

from typing import Generic, TypeVar, Optional

T = TypeVar('T')


class Node(Generic[T]):
    """
    This class is compatible with the heapq.heappush/heappop algorithm due to the
    __lt__ implementation detail.
    """
    def __init__(self, state: T, parent: Optional[T], cost: float = 0.0, heuristic: float = 0.0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node) -> bool:
        """Used with a heap / priorityqueue"""
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

