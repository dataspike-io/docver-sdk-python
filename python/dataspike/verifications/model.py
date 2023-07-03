from typing import Sequence, Optional, List, Tuple
from ..utils import StrEnum
from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from uuid import UUID
from datetime import datetime
from ..documents.model import DocumentType, DocumentRef

__all__ = [
    "Verification",
    "CheckStep",
    "CheckStatus",
    "VerificationStatus",
    "CheckError",
    "CheckResult",
    "Checks",
    "CheckType",
]


class CheckType(StrEnum):
    """

    Basically it's DocumentType without sides
    """

    Passport = "passport"
    Visa = "visa"
    IdCard = "id_card"
    Liveness = "liveness_photo"
    ResidencePermit = "residence_permit"
    Selfie = "selfie"
    DriverLicense = "driver_license"
    Poa = "poa"
    PoaUtilityBill = "poa_utility_bill"
    PoaBankStatement = "poa_bank_statement"
    PoaResidenceRegistration = "poa_residence_registration"


class CheckStep(StrEnum):
    Ocr = "document_ocr"
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
    document_ocr: Optional[CheckResult] = Field(default=None)
    face_comparison: Optional[CheckResult] = Field(default=None)
    liveness: Optional[CheckResult] = Field(default=None)
    document_mrz: Optional[CheckResult] = Field(default=None)
    poa: Optional[CheckResult] = Field(default=None)

    def non_empty_checks(self) -> List[Tuple[str, CheckResult]]:
        return list(  # type: ignore[general-type]
            filter(
                lambda x: x[1] is not None,
                [
                    ("document_mrz", self.document_mrz),
                    ("document_ocr", self.document_ocr),
                    ("face_comparison", self.face_comparison),
                    ("liveness", self.liveness),
                    ("poa", self.poa),
                ],
            )
        )


@dataclass
class Verification:
    id: UUID
    applicant_id: UUID
    status: VerificationStatus
    organization_id: str
    account_id: str
    account_email: str
    created_at: datetime
    checks: Optional[Checks] = Field(default=None)
    document_type: Optional[DocumentType] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    document_ids: List[UUID] = Field(default_factory=list)
    documents: List[DocumentRef] = Field(default_factory=list)
    expires_at: Optional[datetime] = Field(default=None)
    verification_url_id: Optional[str] = Field(default=None)
    verification_url: Optional[str] = Field(default=None)

    @property
    def mrz_data(self) -> Optional[dict]:
        if self.checks and self.checks.document_mrz:
            return self.checks.document_mrz.data
