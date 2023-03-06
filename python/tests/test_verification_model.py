from dataspike import Checks, CheckStatus, CheckResult


def test_non_empty_checks():
    checks = Checks(
        document_mrz=CheckResult(status=CheckStatus.Verified, data={"mrz": {"name": "John"}}),
        document_ocr=CheckResult(status=CheckStatus.Verified),
        face_comparison=CheckResult(status=CheckStatus.Verified),
        poa=CheckResult(status=CheckStatus.Verified),
    )
    data = checks.non_empty_checks()
    assert data == [
        ("document_mrz", checks.document_mrz),
        ("document_ocr", checks.document_ocr),
        ("face_comparison", checks.face_comparison),
        ("poa", checks.poa),
    ]
