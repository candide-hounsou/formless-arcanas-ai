from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field, model_validator


class ActorRole(str, Enum):
    """Role classes are deliberately coarse; liability rules live in invariants."""

    HUMAN = "human"
    AI_SYSTEM = "ai_system"
    ORG = "org"
    POLICY = "policy"


class Actor(BaseModel):
    """An actor in the responsibility chain."""

    actor_id: str = Field(..., min_length=2)
    role: ActorRole
    display_name: str = Field(..., min_length=1)
    accountable: bool = False


class ResponsibilityEdge(BaseModel):
    """Directed edge representing responsibility transfer or dependency."""

    src: str
    dst: str
    relation: str = Field(..., min_length=3, description="e.g., approved, overrode, depended_on")


class ResponsibilityGraph(BaseModel):
    """A minimal responsibility graph: actors + directed edges."""

    actors: List[Actor] = Field(default_factory=list)
    edges: List[ResponsibilityEdge] = Field(default_factory=list)

    def actor_index(self) -> Dict[str, Actor]:
        return {a.actor_id: a for a in self.actors}

    def accountable_actors(self) -> List[Actor]:
        return [a for a in self.actors if a.accountable]

    def validate_connected(self) -> None:
        """Ensure edges reference existing actors and graph is not disconnected in a trivial way."""
        idx = self.actor_index()
        for e in self.edges:
            if e.src not in idx:
                raise ValueError(f"Responsibility edge src '{e.src}' is not a known actor")
            if e.dst not in idx:
                raise ValueError(f"Responsibility edge dst '{e.dst}' is not a known actor")

    def has_human_accountability(self) -> bool:
        return any(a.accountable and a.role == ActorRole.HUMAN for a in self.actors)

    @model_validator(mode="after")
    def _basic_graph_checks(self) -> "ResponsibilityGraph":
        # Structural checks only. Business invariants are enforced separately.
        if not self.actors:
            # allow empty graph at model level; invariants will fail fast.
            return self
        self.validate_connected()
        # Prevent trivial duplicates
        seen: Set[str] = set()
        for a in self.actors:
            if a.actor_id in seen:
                raise ValueError(f"Duplicate actor_id '{a.actor_id}'")
            seen.add(a.actor_id)
        return self
