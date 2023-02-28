from typing import Optional, Union, List
from uuid import UUID

from pydantic.dataclasses import dataclass
from pydantic.fields import Field
from ..utils import StrEnum

__all__ = [
    "EntityTag",
    "EntityTagStr",
    "EntityType",
    "EntityName",
    "EntityInfo",
    "DataSource",
    "DataSourceStr",
    "DateRange",
    "RiskScore",
    "AMLSearchRequest",
    "AMLEntity",
    "AMLResponse",
    "ContactInfo",
    "EntityFields",
    "SourceData",
    "AdverseMedia",
    "GenericData",
    "RegistrationId",
    "LocationData",
    "PoliticalRole",
    "Occupation",
    "Gender",
    "CountryAlpha2",
]

CountryAlpha2 = str


class EntityType(StrEnum):
    Person = "Person"
    Organization = "Organization"
    Vessel = "Vessel"
    Aircraft = "Aircraft"


class EntityTag(StrEnum):
    Unknown = "Unknown"
    Sanctions = "Sanctions"
    Criminal = "Criminal"
    Legal = "Legal"
    PEP = "PEP"
    Finance = "Finance"
    Terrorism = "Terrorism"
    Social = "Social"
    Leaks = "Leaks"

    @classmethod
    def _missing_(cls, value):
        return value


EntityTagStr = Union[EntityTag, str]


class DataSource(StrEnum):
    UK_OFSI = "UK_OFSI"
    US_TRADE = "US_TRADE"
    US_OFAC_SDN = "US_OFAC_SDN"
    UA_NABC = "UA_NABC"
    UA_NSDC = "UA_NSDC"
    CH_SECO = "CH_SECO"
    BE_FOD = "BE_FOD"
    FR_FOA = "FR_FOA"
    EU_FINANCIAL = "EU_FINANCIAL"
    AU_SDN = "AU_SDN"
    EU_TRAVEL = "EU_TRAVEL"
    JP_ECONOMIC = "JP_ECONOMIC"
    KZ_TERROR = "KZ_TERROR"
    KG_NATIONAL = "KG_NATIONAL"
    UN_SCC = "UN_SCC"
    UA_SFMS = "UA_SFMS"
    IL_TERROR = "IL_TERROR"
    AR_REPET = "AR_REPET"
    US_OFAC_CONS = "US_OFAC_CONS"
    US_BIS_DENIED = "US_BIS_DENIED"
    ZA_FINANCIAL = "ZA_FINANCIAL"
    RU_WMD = "RU_WMD"
    EU_MAP = "EU_MAP"
    CA_TERROR = "CA_TERROR"
    PL_CSL = "PL_CSL"
    SG_TERROR = "SG_TERROR"
    CA_SEMA = "CA_SEMA"
    AZ_FIU = "AZ_FIU"
    NL_TERROR = "NL_TERROR"
    BG_OMNIO = "BG_OMNIO"
    NZ_RUS = "NZ_RUS"
    INTERPOL_RED = "INTERPOL_RED"
    US_OCC = "US_OCC"
    WORLDBANK_DP = "WORLDBANK_DP"
    AFDB = "AFDB"
    ADB = "ADB"
    UK_COH = "UK_COH"
    IADB = "IADB"
    EUMOSTWANTED = "EUMOSTWANTED"
    EBRD = "EBRD"
    RANSOMWHERE_WALLETS = "RANSOMWHERE_WALLETS"
    UNOPS = "UNOPS"
    INTERPOL_YELLOW = "INTERPOL_YELLOW"
    PPRCT_LEGIT = "PPRCT_LEGIT"
    PPRCT_LEADERS = "PPRCT_LEADERS"
    EVERYPOLITICIAN = "EVERYPOLITICIAN"
    RUPEP = "RUPEP"
    CIA_LEADERS = "CIA_LEADERS"
    EU_MEPS = "EU_MEPS"
    EU_COR = "EU_COR"
    WIKIDATA = "WIKIDATA"
    RU_ACF = "RU_ACF"
    RU_BILLIONAIRES = "RU_BILLIONAIRES"
    RU_RFM_TERROR = "RU_RFM_TERROR"
    NAVALNY_35 = "NAVALNY_35"
    WD_OLG = "WD_OLG"
    NOMINATIM = "NOMINATIM"
    OPENCORPORATES = "OPENCORPORATES"
    RU_EGRUL = "RU_EGRUL"
    GLEIF = "GLEIF"
    OFFSHORELEAKS = "OFFSHORELEAKS"
    CY_COMPANIES = "CY_COMPANIES"
    UA_EDR = "UA_EDR"
    UK_COH_PSC = "UK_COH_PSC"
    FBI_MOST_WANTED = "FBI_MOST_WANTED"
    RU_ISIN = "RU_ISIN"
    UK_MOST_WANTED = "UK_MOST_WANTED"
    OPENSYR = "OPENSYR"
    LINKEDIN = "LINKEDIN"
    UK_FIND_COMPANY = "UK_FIND_COMPANY"
    QUATAR_UNIFIED = "QUATAR_UNIFIED"
    IN_MHA = "IN_MHA"
    UAE_TERROR = "UAE_TERROR"
    NL_MOST_WANTED = "NL_MOST_WANTED"

    @classmethod
    def _missing_(cls, value):
        return value


DataSourceStr = Union[DataSource, str]


@dataclass
class DateRange:
    gte: Optional[str] = Field(default=None)
    lte: Optional[str] = Field(default=None)


class RiskScore(StrEnum):
    High = "High"
    Medium = "Medium"
    Low = "Low"


@dataclass
class AMLSearchRequest:
    full_name: str
    risk_scores: List[RiskScore]
    countries: Optional[List[str]] = Field(default=None)
    cities: Optional[List[str]] = Field(default=None)
    entity_types: Optional[List[EntityType]] = Field(default=None)
    postal_codes: Optional[List[str]] = Field(default=None)
    date_of_birth: Optional[DateRange] = Field(default=None)
    tags: Optional[List[EntityTagStr]] = Field(default=None)
    sources: Optional[List[DataSourceStr]] = Field(default=None)
    registration_ids: Optional[List[str]] = Field(default=None)


@dataclass
class EntityName:
    full_name: str
    first_name: Optional[str] = Field(default=None)
    last_name: str = Field(default=None)
    lang: str = Field(default=None)


@dataclass
class SourceData:
    source_id: DataSourceStr
    name: str
    reason: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    source_url: Optional[str] = Field(default=None)
    risk_score: Optional[RiskScore] = Field(default=None)
    tags: Optional[List[EntityTagStr]] = Field(default=None)  # re-check this


@dataclass
class AdverseMedia:
    source_name: str
    source_url: Optional[str] = Field(default=None)
    headline: Optional[str] = Field(default=None)
    summary: Optional[str] = Field(default=None)
    published_at: Optional[int] = Field(default=None)
    risk_score: Optional[RiskScore] = Field(default=None)


@dataclass
class GenericData:
    description: str
    url: Optional[str] = Field(default=None)


@dataclass
class ContactInfo:
    emails: Optional[List[str]] = Field(default=None)
    phones: Optional[List[str]] = Field(default=None)
    websites: Optional[List[str]] = Field(default=None)


@dataclass
class RegistrationId:
    id: str
    id_type: Optional[str] = Field(default=None)  # typing?
    date: Optional[str] = Field(default=None)  # typing?
    industry: Optional[str] = Field(default=None)
    country: Optional[CountryAlpha2] = Field(default=None)


@dataclass
class LocationData:
    country: Optional[CountryAlpha2] = Field(default=None)
    region: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    postal_code: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)


@dataclass
class PoliticalRole:
    role: str
    country: Optional[CountryAlpha2] = Field(default=None)


@dataclass
class Occupation:
    occupation: str = Field(description="Known occupation")
    country: Optional[CountryAlpha2] = Field(default=None)


@dataclass
class EntityInfo:
    name: str
    ref: Optional[str] = Field(default=None, description="Reference to another entity in the system")
    role: Optional[str] = Field(default=None)
    country: Optional[CountryAlpha2] = Field(default=None)


class Gender(StrEnum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


@dataclass
class EntityFields:
    names: List[EntityName]
    sources: Optional[List[SourceData]] = Field(default=None)
    media: Optional[AdverseMedia] = Field(default=None)  # array or not?
    images: Optional[List[GenericData]] = Field(default=None)
    contact_info: Optional[ContactInfo] = Field(default=None)
    registration_ids: Optional[List[RegistrationId]] = Field(default=None)
    addresses: Optional[List[LocationData]] = Field(default=None)
    genders: Optional[List[Gender]] = Field(default=None)
    dates_of_birth: Optional[List[DateRange]] = Field(default=None)
    places_of_birth: Optional[List[LocationData]] = Field(default=None)
    dates_of_death: Optional[List[DateRange]] = Field(default=None)
    places_of_death: Optional[List[LocationData]] = Field(default=None)
    citizenships: Optional[List[CountryAlpha2]] = Field(default=None)
    nationalities: Optional[List[str]] = Field(default=None)
    political_roles: Optional[List[PoliticalRole]] = Field(default=None)
    occupations: Optional[List[Occupation]] = Field(default=None)
    companies_and_enterprises: Optional[List[EntityInfo]] = Field(default=None)
    owners_and_beneficiaries: Optional[List[EntityInfo]] = Field(default=None)
    updated_at: Optional[int] = Field(default=None)


@dataclass
class AMLEntity:
    uuid: UUID
    type: EntityType
    risk_score: RiskScore
    fields: EntityFields
    tags: Optional[List[EntityTagStr]] = Field(default=None)
    annotation: Optional[str] = Field(default=None)


@dataclass
class AMLResponse:
    requested_name: str
    search_uuid: UUID
    data: List[AMLEntity]
