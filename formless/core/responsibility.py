from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Set

from pydantic import BaseModel, Field, model_validator


class ActorRole(str, Enum):
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
    accountability_role: str | None = Field(default=None, description="Role-specific accountability label for humans")
    authority_level: int = Field(default=0, ge=0, le=10)
    delegated_by: str | None = None
    delegation_valid_from: datetime | None = None
    delegation_expires_at: datetime | None = None


class ResponsibilityEdge(BaseModel):
    """Directed edge representing responsibility transfer or dependency."""

    src: str
    dst: str
    relation: str = Field(..., min_length=3, description="e.g., approved, overrode, depended_on")


class OverrideProvenance(BaseModel):
    override_id: str = Field(..., min_length=3)
    from_actor_id: str
    to_actor_id: str
    reason: str = Field(..., min_length=5)
    liability_transfer: bool = True


class ResponsibilityGraph(BaseModel):
    """Responsibility graph: actors + directed edges + explicit overrides."""

    actors: List[Actor] = Field(default_factory=list)
    edges: List[ResponsibilityEdge] = Field(default_factory=list)
    overrides: List[OverrideProvenance] = Field(default_factory=list)

    def actor_index(self) -> Dict[str, Actor]:
        return {a.actor_id: a for a in self.actors}

    def accountable_actors(self) -> List[Actor]:
        return [a for a in self.actors if a.accountable]

    def validate_connected(self) -> None:
        idx = self.actor_index()
        for e in self.edges:
            if e.src not in idx:
                raise ValueError(f"Responsibility edge src '{e.src}' is not a known actor")
            if e.dst not in idx:
                raise ValueError(f"Responsibility edge dst '{e.dst}' is not a known actor")
        for o in self.overrides:
            if o.from_actor_id not in idx or o.to_actor_id not in idx:
                raise ValueError("Override provenance references unknown actor")
            if not o.liability_transfer:
                raise ValueError("v1 requires liability transfer on overrides")

    def has_human_accountability(self) -> bool:
        return any(
            a.accountable
            and a.role == ActorRole.HUMAN
            and isinstance(a.accountability_role, str)
            and bool(a.accountability_role.strip())
            for a in self.actors
        )

    @model_validator(mode="after")
    def _basic_graph_checks(self) -> "ResponsibilityGraph":
        if not self.actors:
            return self
        self.validate_connected()
        seen: Set[str] = set()
        for a in self.actors:
            if a.actor_id in seen:
                raise ValueError(f"Duplicate actor_id '{a.actor_id}'")
            if a.delegated_by and a.delegated_by == a.actor_id:
                raise ValueError("Actor cannot delegate to self")
            if (a.delegation_valid_from and not a.delegation_expires_at) or (
                a.delegation_expires_at and not a.delegation_valid_from
            ):
                raise ValueError("Delegation windows require both start and end")
            if a.delegation_valid_from and a.delegation_expires_at and a.delegation_expires_at <= a.delegation_valid_from:
                raise ValueError("Delegation window must be positive")
            seen.add(a.actor_id)
        return self
