from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from ..utils import StrEnum
from uuid import UUID

__all__ = ["DocumentType", "DocumentSide", "DocumentRef", "Document"]


class DocumentType(StrEnum):
    """
    Generic DocumentType with and without sides
    """

    Passport = "passport"
    Visa = "visa"
    IdCard = "id_card"
    IdCardFront = "id_card_front"
    IdCardBack = "id_card_back"
    Liveness = "liveness_photo"
    LivenessExtra = "liveness_photo_extra"
    ResidencePermit = "residence_permit"
    ResidencePermitFront = "residence_permit_front"
    ResidencePermitBack = "residence_permit_back"
    Selfie = "selfie"
    DriverLicense = "driver_license"
    DriverLicenseFront = "driver_license_front"
    DriverLicenseBack = "driver_license_back"
    Poa = "poa"
    PoaUtilityBill = "poa_utility_bill"
    PoaResidenceRegistration = "poa_residence_registration"
    PoaBankStatement = "poa_bank_statement"


class DocumentSide(StrEnum):
    Front = "front"
    Back = "back"


@dataclass
class DocumentRef:
    document_id: UUID
    document_type: DocumentType


@dataclass
class Document:
    content: bytes
    document_type: Optional[DocumentType] = Field(default=None)
    content_type: Optional[str] = Field(default=None)

    def __repr__(self):
        return (
            f"DocumentContent(content_type={self.content_type}, "
            f"document_type={self.document_type}, content=<{len(self.content)} bytes>"
        )
