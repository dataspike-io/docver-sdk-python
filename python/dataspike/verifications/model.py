from typing import Sequence, Optional
from enum import StrEnum
from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from uuid import UUID
from datetime import datetime
from ..documents.model import DocumentType, DocumentRef


class CheckStep(StrEnum):
    Ocr = "document_cr"
    FaceComparison = "face_comparison"
    Liveness = "liveness"
    Mrz = "document_mrz"
    Poa = "poa"


class CheckStatus(StrEnum):
    InProgress = "in_progress"
    Pending = "pending"
    Verified = "verified"
    Failed = "failed"


class VerificationStatus(StrEnum):
    Failed = "failed"
    Pending = "pending"
    InProgress = "in_progress"
    Initial = "initial"
    Verified = "verified"


@dataclass
class CheckError:
    code: int
    message: str


@dataclass
class CheckResult:
    status: CheckStatus
    errors: Sequence[CheckError] = Field(default_factory=list)
    pending_documents: Sequence[DocumentType] = Field(default_factory=list)
    data: Optional[dict] = Field(default=None)  # json


@dataclass
class Checks:
    document_ocr: CheckResult | None = Field(default=None)
    face_comparison: CheckResult | None = Field(default=None)
    liveness: CheckResult | None = Field(default=None)
    document_mrz: CheckResult | None = Field(default=None)
    poa: CheckResult | None = Field(default=None)


@dataclass
class Verification:
    id: UUID
    applicant_id: UUID
    status: VerificationStatus
    organization_id: str
    account_id: str
    account_email: str
    created_at: datetime
    checks: Checks | None = Field(default=None)
    document_type: Optional[DocumentType] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    document_ids: Sequence[UUID] = Field(default_factory=list)
    documents: Sequence[DocumentRef] = Field(default_factory=list)

    @property
    def mrz_data(self) -> None | dict:
        if self.checks and self.checks.document_mrz:
            return self.checks.document_mrz.data
