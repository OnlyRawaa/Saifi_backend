# services/ai_cache.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List

from scipy.sparse import csr_matrix


@dataclass
class AIState:
    # ====== Model & Encoders ======
    model: Optional[Any] = None
    child_encoder: Optional[Dict[str, int]] = None
    activity_encoder: Optional[Dict[str, int]] = None
    reverse_activity_map: Optional[Dict[int, str]] = None  # ALS idx -> activity_id (UUID str)

    # ====== CF Matrix ======
    matrix: Optional[csr_matrix] = None

    # ====== Metadata Caches ======
    child_meta: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    activity_meta: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # ====== Fallback Helpers ======
    popular_activity_ids: List[str] = field(default_factory=list)

    # ====== Refresh Control ======
    last_refresh_ts: float = 0.0
    refresh_lock: asyncio.Lock = field(default_factory=asyncio.Lock)


STATE = AIState()
