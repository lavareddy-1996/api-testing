def test_response_headers_soft_checks(api_context):
    """
    Verify the HTTP response status and response headers
    returned by https://www.google.com.
    """
    url = "https://www.google.com"
    response = api_context.get(url)

    assert response.ok, "Request was not successful."
    assert (
        response.status == 200
    ), f"Expected status code 200, but got {response.status}"
    assert (
        response.status_text == "OK"
    ), f"Expected status text 'OK', but got '{response.status_text}'"

    headers = response.headers

    print("\n========== Response Headers ==========")
    for key, value in headers.items():
        print(f"{key:<25}: {value}")
    print("=" * 40)

    assert "content-type" in headers, "Content-Type header is missing."
    assert "server" in headers, "Server header is missing."
    assert "date" in headers, "Date header is missing."

    content_type = headers["content-type"]
    content_encoding = headers.get("content-encoding")

    assert "text/html" in content_type, f"Unexpected Content-Type: {content_type}"

    # Accepts any of the common compression algorithms, since the server
    # may choose different encodings depending on client/region.
    if content_encoding:
        assert content_encoding in [
            "gzip",
            "br",
            "zstd",
        ], f"Unexpected Content-Encoding: {content_encoding}"
