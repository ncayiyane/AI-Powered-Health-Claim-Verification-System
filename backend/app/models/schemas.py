from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class Verdict(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    PARTIALLY_TRUE = "PARTIALLY_TRUE"
    UNVERIFIED = "UNVERIFIED"


class ClaimRequest(BaseModel):
    claim: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="The health-related claim to verify.",
        examples=["Drinking lemon water cures diabetes."]
    )


class EvidenceItem(BaseModel):
    title: str
    source: str
    url: HttpUrl | None = None
    snippet: str
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )


class VerificationResponse(BaseModel):
    claim: str
    verdict: Verdict
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )
    explanation: str
    evidence: list[EvidenceItem] = Field(default_factory=list)