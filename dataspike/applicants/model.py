from typing import Literal, Optional

from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from uuid import UUID
from ..utils import StrEnum

__all__ = ["ApplicantInfo", "ApplicantVerificationStatus", "Applicant"]


@dataclass
class ApplicantInfo:
    full_name: Optional[str] = Field(default=None)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    dob: Optional[str] = Field(default=None)
    gender: Optional[Literal["M", "F"]] = Field(default=None)
    citizenship: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)


class ApplicantVerificationStatus(StrEnum):
    Initial = "initial"
    Passed = "passed"
    Failed = "failed"


@dataclass
class Applicant:
    applicant_id: UUID
    system_info: ApplicantInfo
    verification_status: ApplicantVerificationStatus = Field(default="initial")
    provided_info: Optional[ApplicantInfo] = Field(default=None)
    external_id: Optional[str] = Field(default=None)
