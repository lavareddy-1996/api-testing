import base64

from config.config import (
    GITHUB_TOKEN,
    OPENWEATHER_API_KEY,
    WEATHERAPI_KEY,
    IMGUR_CLIENT_ID,
    IMGUR_CLIENT_SECRET,
    IMGUR_REDIRECT_URI,
    IMGUR_AUTH_CODE,
)


def test_basic_authentication(api_context):
    credentials = base64.b64encode(b"user:pass").decode("utf-8")
    response = api_context.get(
        "https://httpbin.org/basic-auth/user/pass",
        headers={"Authorization": f"Basic {credentials}"},
    )

    assert response.ok
    assert response.status == 200
    print("Response body:", response.json())


def test_basic_authentication_herokuapp(api_context):
    credentials = base64.b64encode(b"admin:admin").decode("utf-8")
    response = api_context.get(
        "http://the-internet.herokuapp.com/basic_auth",
        headers={"Authorization": f"Basic {credentials}"},
    )

    assert response.ok
    assert response.status == 200
    print("Response body:", response.text())


def test_bearer_token_auth_github_repos(api_context):
    response = api_context.get(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
    )
    assert response.status == 200
    print("Response Body (Repositories):", response.json())


def test_bearer_token_auth_github_user(api_context):
    response = api_context.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
    )
    assert response.status == 200
    print("Response Body (User details):", response.json())


def test_api_key_auth_open_weather(api_context):
    query_params = {"q": "Delhi", "appid": OPENWEATHER_API_KEY}
    response = api_context.get(
        "https://api.openweathermap.org/data/2.5/weather", params=query_params
    )
    assert response.status == 200
    print("Response body:", response.json())


def test_api_key_auth_weather_api(api_context):
    query_params = {"q": "Bangalore", "key": WEATHERAPI_KEY}
    response = api_context.get(
        "https://api.weatherapi.com/v1/current.json", params=query_params
    )
    assert response.status == 200
    print("Weather info:", response.json())


# ---------------------------------------------------------------------------
# OAuth2 Authentication (Imgur)
#
# Manual steps required before running this test:
# 1. Register an app at https://api.imgur.com/oauth2/addclient to get a
#    Client ID and Client Secret.
# 2. Complete the OAuth2 authorization-code flow in a browser to obtain a
#    fresh authorization code (these are short-lived and single-use).
# 3. Set IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET, and IMGUR_AUTH_CODE in your
#    .env file before running this test.
# ---------------------------------------------------------------------------
def test_oauth2_authentication_imgur(api_context):
    token_response = api_context.post(
        "https://api.imgur.com/oauth2/token",
        form={
            "client_id": IMGUR_CLIENT_ID,
            "client_secret": IMGUR_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": IMGUR_AUTH_CODE,
            "redirect_uri": IMGUR_REDIRECT_URI,
        },
    )
    assert token_response.status == 200
    token_data = token_response.json()
    access_token = token_data.get("access_token")
    print(f"Generated Access Token: {access_token}")
    assert access_token is not None, "Access token not found in response!"

    image_response = api_context.get(
        "https://api.imgur.com/3/account/me/images",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert image_response.status == 200
    print("Response JSON:", image_response.json())
