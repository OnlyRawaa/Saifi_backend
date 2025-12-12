# services/ai_cache.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, Optional, List, Tuple

from scipy.sparse import csr_matrix


@dataclass
class AIState:
    model: Optional[Any] = None
    child_encoder: Optional[Dict[str, int]] = None
    activity_encoder: Optional[Dict[str, int]] = None
    reverse_activity_map: Optional[Dict[int, str]] = None  # ALS idx -> activity_id (UUID str)

    matrix: Optional[csr_matrix] = None

    # metadata caches
    child_meta: Dict[str, Dict[str, Any]] = None
    activity_meta: Dict[str, Dict[str, Any]] = None

    # fallback helpers
    popular_activity_ids: List[str] = None  # ordered best -> worst

    last_refresh_ts: float = 0.0
    refresh_lock: asyncio.Lock = asyncio.Lock()


STATE = AIState(
    child_meta={},
    activity_meta={},
    popular_activity_ids=[],
)
