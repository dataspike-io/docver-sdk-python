package dataspike_test

import (
	"bytes"
	"fmt"
	"github.com/dataspike-io/docver-sdk/go/dataspike"
	"github.com/gofrs/uuid"
	"github.com/stretchr/testify/assert"
	"net/http"
	"net/http/httptest"
	"testing"
)

var (
	client = http.DefaultClient
	token  = "test"
)

func Test_dataspikeClient_CancelVerification(t *testing.T) {
	t.Parallel()
	verID, err := uuid.NewV7()
	if err != nil {
		t.Error(err)
	}
	tests := []struct {
		name    string
		handler http.HandlerFunc
		nonUrl  bool
		err     string
	}{
		{
			name: "success",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			err: "",
		},
		{
			name: "status error",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			err: "dataspike error: 400 Bad Request; body:",
		},
		{
			name: "unsupported protocol scheme",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			nonUrl: true,
			err:    `/cancel": unsupported protocol scheme ""`,
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			url := testServer.URL
			if tt.nonUrl {
				url = ""
			}
			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(url), dataspike.WithToken(token))
			err = dc.CancelVerification(verID)

			if err != nil {
				assert.Contains(t, err.Error(), tt.err)
			} else if tt.err != "" {
				t.Errorf("expected %s, but actual nil", tt.err)
			}
		})
	}
}

func Test_dataspikeClient_CreateApplicant(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name      string
		applicant *dataspike.ApplicantCreate
		handler   http.HandlerFunc
		want      string
		err       string
	}{
		{
			name:      "success",
			applicant: &dataspike.ApplicantCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"id":"test"}`))
			}),
			want: "test",
			err:  "",
		},
		{
			name:      "json error",
			applicant: &dataspike.ApplicantCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: "",
			err:  "unexpected end of JSON input",
		},
		{
			name:      "http do error",
			applicant: &dataspike.ApplicantCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: "",
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			tt := tt
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.CreateApplicant(tt.applicant)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_CreateVerification(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name         string
		verification *dataspike.VerificationCreate
		handler      http.HandlerFunc
		want         *dataspike.Verification
		err          string
	}{
		{
			name:         "success",
			verification: &dataspike.VerificationCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"id":"test"}`))
			}),
			want: &dataspike.Verification{Id: "test"},
			err:  "",
		},
		{
			name:         "json error",
			verification: &dataspike.VerificationCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: nil,
			err:  "unexpected end of JSON input",
		},
		{
			name:         "status error",
			verification: &dataspike.VerificationCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: nil,
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.CreateVerification(tt.verification)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_CreateWebhook(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name    string
		webhook *dataspike.WebhookCreate
		handler http.HandlerFunc
		err     error
	}{
		{
			name:    "success",
			webhook: &dataspike.WebhookCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			err: nil,
		},
		{
			name:    "status error",
			webhook: &dataspike.WebhookCreate{},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			err: fmt.Errorf("dataspike error: %d Bad Request; body: ", http.StatusBadRequest),
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			err := dc.CreateWebhook(tt.webhook)
			assert.Equal(t, tt.err, err)
		})
	}
}

func Test_dataspikeClient_GetApplicant(t *testing.T) {
	t.Parallel()
	appID, err := uuid.NewV7()
	if err != nil {
		t.Error(err)
	}
	tests := []struct {
		name        string
		applicantID uuid.UUID
		handler     http.HandlerFunc
		want        *dataspike.Applicant
		err         string
	}{
		{
			name:        "success",
			applicantID: appID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"applicant_id":"321"}`))
			}),
			want: &dataspike.Applicant{ApplicantId: "321"},
			err:  "",
		},
		{
			name:        "json error",
			applicantID: appID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: nil,
			err:  "unexpected end of JSON input",
		},
		{
			name:        "status error",
			applicantID: appID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: nil,
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.GetApplicantByID(tt.applicantID)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_GetApplicantByExternal(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name       string
		externalID string
		handler    http.HandlerFunc
		want       *dataspike.Applicant
		err        string
	}{
		{
			name:       "success",
			externalID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"applicant_id":"321"}`))
			}),
			want: &dataspike.Applicant{ApplicantId: "321"},
			err:  "",
		},
		{
			name:       "json error",
			externalID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: nil,
			err:  "unexpected end of JSON input",
		},
		{
			name:       "status error",
			externalID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: nil,
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.GetApplicantByExternalID(tt.externalID)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_GetVerificationByID(t *testing.T) {
	t.Parallel()
	verID, err := uuid.NewV7()
	if err != nil {
		t.Error(err)
	}
	tests := []struct {
		name    string
		verID   uuid.UUID
		handler http.HandlerFunc
		want    *dataspike.Verification
		err     string
	}{
		{
			name:  "success",
			verID: verID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"id":"321"}`))
			}),
			want: &dataspike.Verification{Id: "321"},
			err:  "",
		},
		{
			name:  "json error",
			verID: verID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: nil,
			err:  "unexpected end of JSON input",
		},
		{
			name:  "status error",
			verID: verID,
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: nil,
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.GetVerificationByID(tt.verID)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_GetVerificationByShortID(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name    string
		shortID string
		handler http.HandlerFunc
		want    *dataspike.Verification
		err     string
	}{
		{
			name:    "success",
			shortID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"id":"321"}`))
			}),
			want: &dataspike.Verification{Id: "321"},
			err:  "",
		},
		{
			name:    "json error",
			shortID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			want: nil,
			err:  "unexpected end of JSON input",
		},
		{
			name:    "status error",
			shortID: "123",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusTeapot)
			}),
			want: nil,
			err:  "dataspike error: 418 I'm a teapot; body: ",
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			got, err := dc.GetVerificationByShortID(tt.shortID)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeClient_LinkTelegramProfile(t *testing.T) {
	t.Parallel()
	type args struct {
		applicantID string
		tgProfile   string
	}
	tests := []struct {
		name    string
		args    args
		handler http.HandlerFunc
		err     error
	}{
		{
			name: "success",
			args: args{applicantID: "123", tgProfile: "123"},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			err: nil,
		},
		{
			name: "status error",
			args: args{applicantID: "123", tgProfile: "123"},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			err: fmt.Errorf("dataspike error: %d Bad Request; body: ", http.StatusBadRequest),
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			err := dc.LinkTelegramProfile(tt.args.applicantID, tt.args.tgProfile)
			assert.Equal(t, tt.err, err)
		})
	}
}

func Test_dataspikeClient_ProceedVerification(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name    string
		handler http.HandlerFunc
		err     error
	}{
		{
			name: "success",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
			}),
			err: nil,
		},
		{
			name: "status error",
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			err: fmt.Errorf("dataspike error: %d Bad Request; body: ", http.StatusBadRequest),
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(testServer.URL), dataspike.WithToken(token))
			err := dc.ProceedVerification("test")
			assert.Equal(t, tt.err, err)
		})
	}
}

func Test_dataspikeClient_UploadDocument(t *testing.T) {
	side := "test"
	t.Parallel()
	tests := []struct {
		name    string
		doc     *dataspike.DocumentUpload
		handler http.HandlerFunc
		nonUrl  bool
		want    *dataspike.Document
		err     string
	}{
		{
			name: "success",
			doc:  &dataspike.DocumentUpload{Reader: bytes.NewReader([]byte("test")), Side: &side, IssuedCountry: &side},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"document_id":"321"}`))
			}),
			want: &dataspike.Document{DocumentId: "321"},
			err:  "",
		},
		{
			name: "status error",
			doc:  &dataspike.DocumentUpload{Reader: bytes.NewReader([]byte("test")), Side: &side, IssuedCountry: &side},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusBadRequest)
			}),
			want: nil,
			err:  "dataspike error: 400 Bad Request; body: ",
		},
		{
			name: "json error",
			doc:  &dataspike.DocumentUpload{Reader: bytes.NewReader([]byte("test")), Side: &side, IssuedCountry: &side},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {
				res.WriteHeader(http.StatusOK)
				res.Write([]byte(`{"document_id":321}`))
			}),
			want: nil,
			err:  "json: cannot unmarshal number into Go struct field Document.document_id of type string",
		},
		{
			name:    "unsupported protocol scheme",
			doc:     &dataspike.DocumentUpload{Reader: bytes.NewReader([]byte("test")), Side: &side, IssuedCountry: &side},
			handler: http.HandlerFunc(func(res http.ResponseWriter, req *http.Request) {}),
			nonUrl:  true,
			want:    nil,
			err:     `Post "/api/v3/upload/": unsupported protocol scheme ""`,
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			testServer := httptest.NewServer(tt.handler)
			defer func() { testServer.Close() }()

			url := testServer.URL
			if tt.nonUrl {
				url = ""
			}
			dc := dataspike.NewDataspikeClient(client, dataspike.WithEndpoint(url), dataspike.WithToken(token))
			got, err := dc.UploadDocument(tt.doc)
			if err != nil {
				assert.Equal(t, tt.err, err.Error())
			}
			assert.Equal(t, tt.want, got)
		})
	}
}

func Test_dataspikeModels_Errors(t *testing.T) {
	errs := dataspike.Errors{
		{Code: 123, Message: "test"},
	}
	assert.Equal(t, "Code: 123; Message: test", errs.String())
}
