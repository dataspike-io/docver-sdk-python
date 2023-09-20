package dataspike

import (
	"fmt"
	"io"
	"strings"
	"time"
)

// Verifications

type Verification struct {
	Id          string `json:"id"`
	ApplicantID string `json:"applicant_id"`
	Status      string `json:"status"`
	Documents   []struct {
		DocumentId   string `json:"document_id"`
		DocumentType string `json:"document_type"`
	} `json:"documents"`
	Checks struct {
		DocumentMrz *struct {
			Check
			Data *DataMrz `json:"data"`
		} `json:"document_mrz,omitempty"`
		FaceComparison *Check `json:"face_comparison,omitempty"`
		Poa            *Check `json:"poa,omitempty"`
		Liveness       *Check `json:"liveness,omitempty"`
	} `json:"checks"`
	CreatedAt         time.Time `json:"created_at"`
	CompletedAt       time.Time `json:"completed_at"`
	VerificationUrl   string    `json:"verification_url"`
	VerificationUrlId string    `json:"verification_url_id"`
	CountryCode       string    `json:"country_code"`
	ExpiresAt         time.Time `json:"expires_at"`
	IsSandbox         bool      `json:"is_sandbox"`
	ProfileId         string    `json:"profile_id"`
	Settings          *Settings `json:"settings,omitempty"`
}

type VerificationCreate struct {
	ApplicantId       string   `json:"applicant_id"`
	ChecksRequired    []string `json:"checks_required"`
	ProfileId         *string  `json:"profile_id,omitempty"`
	ApplicantCountry  string   `json:"applicant_country"`
	ExpirationMinutes int      `json:"expiration_minutes"`
}

// Applicants

type Applicant struct {
	ApplicantId                      string         `json:"applicant_id"`
	ExternalId                       string         `json:"external_id"`
	Type                             string         `json:"type"`
	Email                            string         `json:"email"`
	Phone                            string         `json:"phone"`
	SystemInfo                       *ApplicantInfo `json:"system_info,omitempty"`
	ProvidedInfo                     *ApplicantInfo `json:"provided_info,omitempty"`
	LastVerificationId               string         `json:"last_verification_id"`
	VerificationStatus               string         `json:"verification_status"`
	AmlScreeningEnabled              bool           `json:"aml_screening_enabled"`
	LastAmlScreeningId               string         `json:"last_aml_screening_id"`
	LastScreenedAt                   time.Time      `json:"last_screened_at"`
	LastRiskScore                    string         `json:"last_risk_score"`
	LastTags                         []string       `json:"last_tags"`
	TgProfile                        string         `json:"tg_profile"`
	CrossCheckDuplicatedApplicantIds []string       `json:"cross_check_duplicated_applicant_ids"`
}

type ApplicantCreate struct {
	ExternalId          string         `json:"external_id"`
	Email               *string        `json:"email,omitempty"`
	Phone               *string        `json:"phone,omitempty"`
	Info                *ApplicantInfo `json:"info"`
	AmlScreeningEnabled bool           `json:"aml_screening_enabled,omitempty"`
	ApplicantType       string         `json:"applicant_type"`
}

type ApplicantInfo struct {
	FullName    string `json:"full_name"`
	FirstName   string `json:"first_name"`
	LastName    string `json:"last_name"`
	Dob         string `json:"dob"`
	Gender      string `json:"gender"`
	Citizenship string `json:"citizenship"`
	Address     string `json:"address"`
	Addresses   struct {
		Residence Residence `json:"residence"`
	} `json:"addresses"`
}

type Residence struct {
	Country    string `json:"country"`
	City       string `json:"city"`
	PostalCode string `json:"postal_code"`
	Street     string `json:"street"`
}

type Check struct {
	Status           string   `json:"status"`
	PendingDocuments []string `json:"pending_documents,omitempty"`
	Errors           Errors   `json:"errors"`
}

type Error struct {
	Code    int    `json:"code"`
	Message string `json:"message"`
}

type Errors []Error

func (e Errors) String() string {
	errors := make([]string, 0, len(e))
	for _, err := range e {
		errors = append(errors, fmt.Sprintf("Code: %d; Message: %s", err.Code, err.Message))
	}

	return strings.Join(errors, "\n")
}

type DataMrz struct {
	DocumentType string `json:"document_type"`
	Country      string `json:"country"`
	Name         string `json:"name"`
	Surname      string `json:"surname"`
	DocNumber    string `json:"doc_number"`
	Nationality  string `json:"nationality"`
	BirthDate    string `json:"birth_date"`
	Sex          string `json:"sex"`
	ExpiryDate   string `json:"expiry_date"`
}

type Settings struct {
	PoiRequired                         bool     `json:"poi_required"`
	PoiAllowedDocuments                 []string `json:"poi_allowed_documents,omitempty"`
	FaceComparisonRequired              bool     `json:"face_comparison_required"`
	FaceComparisonAllowedDocuments      []string `json:"face_comparison_allowed_documents,omitempty"`
	PoaRequired                         bool     `json:"poa_required"`
	DisableCrossCheckByBio              bool     `json:"disable_cross_check_by_bio"`
	DisableCrossCheckByPhoto            bool     `json:"disable_cross_check_by_photo"`
	DisableVerifyPoaCountryMatchWithPoi bool     `json:"disable_verify_poa_country_match_with_poi"`
	Countries                           []string `json:"countries,omitempty"`
}

// Documents

type DocumentUpload struct {
	DocType       string    `json:"doc_type"`
	FileName      string    `json:"file_name"`
	Side          *string   `json:"side,omitempty"`
	IssuedCountry *string   `json:"issued_country,omitempty"`
	ApplicantID   string    `json:"applicant_id"`
	Reader        io.Reader `json:"Reader"`
}

type Document struct {
	DocumentId              string  `json:"document_id"`
	DetectedDocumentType    *string `json:"detected_document_type,omitempty"`
	DetectedDocumentSide    *string `json:"detected_document_side,omitempty"`
	DetectedTwoSideDocument *bool   `json:"detected_two_side_document,omitempty"`
	Errors                  []struct {
		Code    int    `json:"code"`
		Message string `json:"message"`
	} `json:"errors"`
}

type WebhookCreate struct {
	WebhookUrl string   `json:"webhook_url"`
	EventTypes []string `json:"event_types"`
	Enabled    bool     `json:"enabled"`
}
