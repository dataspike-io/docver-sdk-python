package dataspike

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"

	"github.com/gofrs/uuid"
)

const tokenHeader = "ds-api-token"

type IDataspikeClient interface {
	GetVerificationByID(uuid.UUID) (*Verification, error)
	GetVerificationByShortID(string) (*Verification, error)
	GetApplicantByID(uuid.UUID) (*Applicant, error)
	LinkTelegramProfile(string, string) error
	UploadDocument(*DocumentUpload) (*Document, error)
	CancelVerification(uuid.UUID) error
	ProceedVerification(uuid.UUID) error
	GetApplicantByExternalID(string) (*Applicant, error)
	CreateApplicant(*ApplicantCreate) (string, error)
	CreateVerification(create *VerificationCreate) (*Verification, error)
	CreateWebhook(webhook *WebhookCreate) error
	ListWebhooks() ([]Webhook, error)
	DeleteWebhook(webhookID uuid.UUID) error
}

type Option func(*dataspikeClient)

type dataspikeClient struct {
	client   *http.Client
	endpoint string
	token    string
}

// GetVerificationByID returns a data of verification by received ID
// Documentation: https://docs.dataspike.io/api/#tag/Verifications/operation/get-verification
func (dc *dataspikeClient) GetVerificationByID(verID uuid.UUID) (*Verification, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/%s", dc.endpoint, verID.String()), nil)
	if err != nil {
		return nil, err
	}

	var verification Verification
	err = json.Unmarshal(body, &verification)
	if err != nil {
		return nil, err
	}

	return &verification, nil
}

// GetVerificationByShortID returns a data of verification by received ShortID
// Documentation: https://docs.dataspike.io/api/#tag/Verifications/operation/get-verification-short
func (dc *dataspikeClient) GetVerificationByShortID(shortID string) (*Verification, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/short/%s", dc.endpoint, shortID), nil)
	if err != nil {
		return nil, err
	}

	var verification Verification
	err = json.Unmarshal(body, &verification)
	if err != nil {
		return nil, err
	}

	return &verification, nil
}

// GetApplicantByID returns a data of applicant by received ID
// Documentation: https://docs.dataspike.io/api/#tag/Applicants/operation/get-applicant
func (dc *dataspikeClient) GetApplicantByID(applicantID uuid.UUID) (*Applicant, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/applicants/%s", dc.endpoint, applicantID.String()), nil)
	if err != nil {
		return nil, err
	}

	var applicant Applicant
	err = json.Unmarshal(body, &applicant)
	if err != nil {
		return nil, err
	}

	return &applicant, nil
}

// LinkTelegramProfile links telegram ID to applicant ID
// Documentation: https://docs.dataspike.io/api/#tag/Applicants/operation/link-applicant-tg
func (dc *dataspikeClient) LinkTelegramProfile(applicantID string, tgProfile string) error {
	bodyReq := struct {
		TgProfile string `json:"tg_profile"`
	}{
		TgProfile: tgProfile,
	}
	b, err := json.Marshal(&bodyReq)
	if err != nil {
		return err
	}

	_, err = dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/applicants/%s/link/tg", dc.endpoint, applicantID), bytes.NewBuffer(b))
	return err
}

// CancelVerification receives verification ID and cancels this verification
// Documentation: https://docs.dataspike.io/api/#tag/Verifications/operation/cancel-verification
func (dc *dataspikeClient) CancelVerification(verificationID uuid.UUID) error {
	_, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/%s/cancel", dc.endpoint, verificationID.String()), nil)
	return err
}

// UploadDocument receives document data with reader and returns uploaded document data with errors
// Documentation: https://docs.dataspike.io/api/#tag/File-management/operation/upload-document
func (dc *dataspikeClient) UploadDocument(doc *DocumentUpload) (*Document, error) {
	buf := new(bytes.Buffer)
	bw := multipart.NewWriter(buf) // body writer

	p1w, _ := bw.CreateFormField("document_type")
	_, err := p1w.Write([]byte(doc.DocType))
	if err != nil {
		return nil, err
	}
	if doc.Side != nil {
		p2w, _ := bw.CreateFormField("side")
		_, err = p2w.Write([]byte(*doc.Side))
		if err != nil {
			return nil, err
		}
	}
	if doc.IssuedCountry != nil {
		p2w, _ := bw.CreateFormField("issued_country")
		_, err = p2w.Write([]byte(*doc.IssuedCountry))
		if err != nil {
			return nil, err
		}
	}

	// file part
	fw1, _ := bw.CreateFormFile("file", doc.FileName)
	_, err = io.Copy(fw1, doc.Reader)
	if err != nil {
		return nil, err
	}

	err = bw.Close() //write the tail boundry
	if err != nil {
		return nil, err
	}

	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/upload/%s", dc.endpoint, doc.ApplicantID), buf)
	if err != nil {
		return nil, err
	}
	req.Header.Set(tokenHeader, dc.token)
	req.Header.Set("Content-Type", bw.FormDataContentType())
	resp, err := dc.client.Do(req)
	if err != nil {
		return nil, err
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated && resp.StatusCode != http.StatusNoContent {
		return nil, fmt.Errorf("dataspike error: %s; body: %s", resp.Status, string(bodyBytes))
	}

	document := &Document{}
	err = json.Unmarshal(bodyBytes, document)
	if err != nil {
		return nil, err
	}

	return document, nil
}

// CreateWebhook creates webhook with received data
// Documentation: https://docs.dataspike.io/api/#tag/Webhooks/operation/create-webhook
func (dc *dataspikeClient) CreateWebhook(webhook *WebhookCreate) error {
	b, err := json.Marshal(webhook)
	if err != nil {
		return err
	}

	_, err = dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/organization/webhooks", dc.endpoint), bytes.NewBuffer(b))
	return err
}

// ListWebhooks returns data of all webhooks
// Documentation: https://docs.dataspike.io/api/#tag/Webhooks/operation/list-webhooks
func (dc *dataspikeClient) ListWebhooks() ([]Webhook, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/organization/webhooks", dc.endpoint), nil)
	if err != nil {
		return nil, err
	}

	var webhooks []Webhook
	err = json.Unmarshal(body, &webhooks)
	if err != nil {
		return nil, err
	}

	return webhooks, nil
}

// DeleteWebhook removes webhook by ID
// Documentation: https://docs.dataspike.io/api/#tag/Webhooks/operation/delete-webhooks
func (dc *dataspikeClient) DeleteWebhook(webhookID uuid.UUID) error {
	_, err := dc.doRequest(http.MethodDelete, fmt.Sprintf("%s/api/v3/organization/webhooks/%s", dc.endpoint, webhookID.String()), nil)
	return err
}

// ProceedVerification proceeds verification by ID. Should be used after all the required documents has been uploaded.
// Documentation: https://docs.dataspike.io/api/#tag/Verifications/operation/proceed-verification
func (dc *dataspikeClient) ProceedVerification(shortID uuid.UUID) error {
	_, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/sdk/%s/proceed", dc.endpoint, shortID.String()), nil)
	return err
}

// GetApplicantByExternalID returns a data of applicant by received external ID
// Documentation: ???
func (dc *dataspikeClient) GetApplicantByExternalID(externalID string) (*Applicant, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/applicants/by_external_id/%s", dc.endpoint, externalID), nil)
	if err != nil {
		return nil, err
	}

	var applicant Applicant
	err = json.Unmarshal(body, &applicant)
	if err != nil {
		return nil, err
	}

	return &applicant, nil
}

// CreateApplicant creates new applicant by received data and returns applicant ID
// Documentation: https://docs.dataspike.io/api/#tag/Applicants/operation/create-applicant
func (dc *dataspikeClient) CreateApplicant(applicant *ApplicantCreate) (string, error) {
	b, err := json.Marshal(applicant)
	if err != nil {
		return "", err
	}

	body, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/applicants", dc.endpoint), bytes.NewBuffer(b))
	if err != nil {
		return "", err
	}

	var resp struct {
		Id string `json:"id"`
	}
	err = json.Unmarshal(body, &resp)
	if err != nil {
		return "", err
	}

	return resp.Id, nil
}

// CreateVerification creates new verification by received data and returns a verification data
// Documentation: https://docs.dataspike.io/api/#tag/Verifications/operation/create-verification
func (dc *dataspikeClient) CreateVerification(verification *VerificationCreate) (*Verification, error) {
	b, err := json.Marshal(verification)
	if err != nil {
		return nil, err
	}

	body, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/verifications", dc.endpoint), bytes.NewBuffer(b))
	if err != nil {
		return nil, err
	}

	var res Verification
	err = json.Unmarshal(body, &res)
	if err != nil {
		return nil, err
	}

	return &res, nil
}

// doRequest makes http request to dataspike api and returns bytes of body
func (dc *dataspikeClient) doRequest(method, url string, body io.Reader) ([]byte, error) {
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, err
	}
	req.Header.Set(tokenHeader, dc.token)

	resp, err := dc.client.Do(req)
	if err != nil {
		return nil, err
	}

	bodyBytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated && resp.StatusCode != http.StatusNoContent {
		return nil, fmt.Errorf("dataspike error: %s; body: %s", resp.Status, string(bodyBytes))
	}

	return bodyBytes, nil
}

// WithToken is a Option that adds dataspike token to client.
func WithToken(token string) Option {
	return func(s *dataspikeClient) {
		s.token = token
	}
}

// WithSandbox is a Option that allows you using sandbox endpoint.
// When this option is nil, the default endpoint is api.dataspike.io.
func WithSandbox() Option {
	return func(s *dataspikeClient) {
		s.endpoint = "https://api.dataspike.dev"
	}
}

// WithEndpoint is a Option that allows you using customizable endpoint.
// When this option is nil, the default endpoint is api.dataspike.io.
func WithEndpoint(endpoint string) Option {
	return func(s *dataspikeClient) {
		s.endpoint = endpoint
	}
}

// NewDataspikeClient makes a new dataspike client with received parameters
func NewDataspikeClient(client *http.Client, options ...Option) IDataspikeClient {
	dsClient := &dataspikeClient{
		client:   client,
		endpoint: "https://api.dataspike.io",
	}
	for _, o := range options {
		o(dsClient)
	}

	return dsClient
}
