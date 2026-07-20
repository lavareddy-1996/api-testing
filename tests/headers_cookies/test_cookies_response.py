def test_cookies_response(api_context):
    url = "https://www.google.com"
    response = api_context.get(url)

    assert response.ok, "Request was not successful."
    assert (
        response.status == 200
    ), f"Expected status code 200, but got {response.status}"
    assert (
        response.status_text == "OK"
    ), f"Expected status text 'OK', but got '{response.status_text}'"

    cookies = api_context.storage_state()["cookies"]
    for cookie in cookies:
        print(f"{cookie['name']} == {cookie['value']} == {cookie['domain']}")

    aec_cookie = next((c for c in cookies if c["name"] == "AEC"), None)
    assert aec_cookie is not None

    print(aec_cookie["name"])
    print(aec_cookie["value"])
    print(aec_cookie["domain"])
    print(aec_cookie["expires"])
