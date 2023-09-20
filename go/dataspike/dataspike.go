package dataspike

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
)

const tokenHeader = "ds-api-token"

type IDataspikeClient interface {
	GetVerificationByID(string) (*Verification, error)
	GetVerificationByShortID(string) (*Verification, error)
	GetApplicant(string) (*Applicant, error)
	LinkTelegramProfile(string, string) error
	UploadDocument(*DocumentUpload) (*Document, error)
	CancelVerification(string) error
	ProceedVerification(string) error
	GetApplicantByExternal(string) (*Applicant, error)
	CreateApplicant(*ApplicantCreate) (string, error)
	CreateVerification(create *VerificationCreate) (*Verification, error)
	CreateWebhook(webhook *WebhookCreate) error
}

type dataspikeClient struct {
	client *http.Client
	url    string
	token  string
}

func (dc *dataspikeClient) GetVerificationByID(verID string) (*Verification, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/%s", dc.url, verID), nil)
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

func (dc *dataspikeClient) GetVerificationByShortID(shortID string) (*Verification, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/short/%s", dc.url, shortID), nil)
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

func (dc *dataspikeClient) GetApplicant(applicantID string) (*Applicant, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/applicants/%s", dc.url, applicantID), nil)
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

	_, err = dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/applicants/%s/link/tg", dc.url, applicantID), bytes.NewBuffer(b))
	return err
}

func (dc *dataspikeClient) CancelVerification(verificationID string) error {
	_, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/verifications/%s/cancel", dc.url, verificationID), nil)
	return err
}

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

	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/upload/%s", dc.url, doc.ApplicantID), buf)
	if err != nil {
		return nil, err
	}
	req.Header = map[string][]string{
		tokenHeader:    {dc.token},
		"Content-Type": {bw.FormDataContentType()},
	}
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

func (dc *dataspikeClient) CreateWebhook(webhook *WebhookCreate) error {
	b, err := json.Marshal(webhook)
	if err != nil {
		return err
	}

	_, err = dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/organization/webhooks", dc.url), bytes.NewBuffer(b))
	return err
}

func (dc *dataspikeClient) ProceedVerification(shortID string) error {
	_, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/sdk/%s/proceed", dc.url, shortID), nil)
	return err
}

func (dc *dataspikeClient) GetApplicantByExternal(externalID string) (*Applicant, error) {
	body, err := dc.doRequest(http.MethodGet, fmt.Sprintf("%s/api/v3/applicants/by_external_id/%s", dc.url, externalID), nil)
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

func (dc *dataspikeClient) CreateApplicant(applicant *ApplicantCreate) (string, error) {
	b, err := json.Marshal(applicant)
	if err != nil {
		return "", err
	}
	fmt.Println(string(b))

	body, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/applicants", dc.url), bytes.NewBuffer(b))
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

func (dc *dataspikeClient) CreateVerification(verification *VerificationCreate) (*Verification, error) {
	b, err := json.Marshal(verification)
	if err != nil {
		return nil, err
	}

	body, err := dc.doRequest(http.MethodPost, fmt.Sprintf("%s/api/v3/verifications", dc.url), bytes.NewBuffer(b))
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

func (dc *dataspikeClient) doRequest(method, url string, body io.Reader) ([]byte, error) {
	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, err
	}
	req.Header = map[string][]string{
		tokenHeader: {dc.token},
	}

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

func NewClient(client *http.Client, url, token string) IDataspikeClient {
	return &dataspikeClient{
		client: client,
		url:    url,
		token:  token,
	}
}
