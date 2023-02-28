# Dataspike python client library

The official wrapper for Dataspike API

## Installation

`pip install dataspike`

## Getting started

Library offers well typed async API powered by pydantic and aiohttp.

```python
from dataspike import *

async with Api("<YOUR_API_TOKEN>") as api:
    verification = await api.verification.create(checks=[CheckType.Passport, CheckType.Selfie])
    await api.document.upload(verification.applicant_id, DocumentType.Passport, open('passport.jpg', 'rb'))
    await api.document.upload(verification.applicant_id, DocumentType.Selfie, open('selfie.jpg', 'rb'))
    await api.verification.proceed(verification.id)
    applicants = await api.applicant.list()
    verifications = await api.verification.list()
```


### Resources

Full reference and documentation about available resources 
can be found at our [official documentation](https://docs.dataspike.io)

Currently library provides following resources
 
- AML `api.aml`
- Applicant `api.applicant`
- Verification `api.verification`
- SDK `api.sdk`
- Documents `api.document`


### Timeouts
Library uses aiohttp ClientSession. 
To pass timeouts use keyword arguments which will passed to ClientSession constructor

Check out [aiohttp client reference](https://docs.aiohttp.org/en/stable/client_reference.html) for details.

Example 
```python
from dataspike import Api
async with Api('<API_TOKEN>', read_timeout=2) as api:
    ...
```

### Errors

- `pydantic.ValidationError` is raised when type parameters not match with expected for API func.
- `asyncio.TimeoutError` is raised if a timeout occurs.
- `dataspike.errors.UnexpectedResponseStatus` is raised whenever dataspike returns unexpected response status.


### Sync API wrapper

We recommend use async api directly. But if you really want to use sync api
library offers `SyncApi` wrapper. Take note it build on top of async API 
and still use asyncio under the hood.

Example
```python
from dataspike import SyncApi
with SyncApi("<API_TOKEN>") as api:
    applicants = api.applicant.list()
```