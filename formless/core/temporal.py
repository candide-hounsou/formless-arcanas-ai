from __future__ import annotations

from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field, model_validator


class TemporalValidity(BaseModel):
    """Time-bounded validity of a decision."""

    valid_from: datetime = Field(..., description="When the decision becomes valid")
    expires_at: datetime = Field(..., description="When the decision is no longer valid")

    @model_validator(mode="after")
    def _check_order(self) -> "TemporalValidity":
        if self.expires_at <= self.valid_from:
            raise ValueError("expires_at must be after valid_from")
        # A conservative guardrail: prevent effectively 'forever' decisions by default.
        # Change as needed in real deployments.
        if self.expires_at - self.valid_from > timedelta(days=365):
            raise ValueError("validity window too long (> 365 days); make the expiry explicit")
        return self

    def is_valid(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return self.valid_from <= now < self.expires_at
