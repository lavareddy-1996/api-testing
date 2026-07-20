def test_response_headers_strict_checks(api_context):
    """
    Verify the response headers returned by https://www.google.com
    using Playwright's API Request Context.
    """
    response = api_context.get("https://www.google.com")

    assert response.ok
    assert response.status_text == "OK"
    assert response.status == 200

    headers = response.headers
    for key, value in headers.items():
        print(f"{key}: {value}")

    assert "text/html" in headers.get("content-type")

    # NOTE: this is a strict equality check on encoding. Google can serve
    # "br" or "zstd" instead of "gzip" depending on client/region, so this
    # assertion can be flaky. Kept as-is intentionally for interview
    # discussion on strict vs. tolerant assertions - see test_headers.py
    # for the more tolerant version of this same check.
    assert "gzip" == headers.get("content-encoding")

    assert "server" in headers
    assert "date" in headers
