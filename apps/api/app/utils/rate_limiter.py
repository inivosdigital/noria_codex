"""Simple in-memory rate limiter for FastAPI endpoints."""
from __future__ import annotations

import asyncio
import time
from collections import deque
from typing import Deque, Dict


class RateLimiter:
    """Token bucket style in-memory limiter.

    Suitable for single-process development environments. Production deployments should
    replace this with a shared store (e.g., Redis) to enforce limits across replicas.
    """

    def __init__(self, limit: int, window_seconds: int) -> None:
        if limit < 1:
            raise ValueError("limit must be >= 1")
        if window_seconds < 1:
            raise ValueError("window_seconds must be >= 1")
        self._limit = limit
        self._window = window_seconds
        self._events: Dict[str, Deque[float]] = {}
        self._lock = asyncio.Lock()

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def window_seconds(self) -> int:
        return self._window

    async def allow(self, key: str) -> bool:
        """Return True if the request is within the rate limit for the provided key."""

        now = time.monotonic()
        async with self._lock:
            queue = self._events.setdefault(key, deque())
            cutoff = now - self._window
            while queue and queue[0] <= cutoff:
                queue.popleft()

            if len(queue) >= self._limit:
                return False

            queue.append(now)
            return True

    async def get_remaining(self, key: str) -> int:
        """Return how many requests remain in the window for the key."""

        now = time.monotonic()
        async with self._lock:
            queue = self._events.get(key)
            if not queue:
                return self._limit

            cutoff = now - self._window
            while queue and queue[0] <= cutoff:
                queue.popleft()

            remaining = self._limit - len(queue)
            return remaining if remaining >= 0 else 0


__all__ = ["RateLimiter"]
