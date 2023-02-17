from pydantic.dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

__all__ = ["DocumentType", "DocumentSide", "DocumentRef"]


class DocumentType(StrEnum):
    Passport = "passport"
    Visa = "visa"
    IdCard = "id_card"
    IdCardFront = "id_card_front"
    IdCardBack = "id_card_back"
    Liveness = "liveness_photo"
    LivenessUp = "liveness_photo_up"
    LivenessDown = "liveness_photo_down"
    LivenessRight = "liveness_photo_right"
    LivenessLeft = "liveness_photo_left"
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
    Left = "left"
    Up = "up"
    Right = "right"
    Down = "down"


@dataclass
class DocumentRef:
    document_id: UUID
    document_type: DocumentType
