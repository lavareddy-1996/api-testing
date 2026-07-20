"""
Authentication API Tests

This module demonstrates the following authentication mechanisms:

1. Basic Authentication
2. Bearer Token Authentication (GitHub)
3. API Key Authentication
4. OAuth2 Authentication (Imgur)

Credentials are loaded from config/config.py.
Tests that require secrets are skipped automatically if the secrets
are not configured. This makes the framework CI/CD friendly.
"""

import base64

import pytest

from config.config import (
    GITHUB_TOKEN,
    OPENWEATHER_API_KEY,
    WEATHERAPI_KEY,
    IMGUR_CLIENT_ID,
    IMGUR_CLIENT_SECRET,
    IMGUR_REDIRECT_URI,
    IMGUR_AUTH_CODE,
)


# =============================================================================
# Helper Function
# =============================================================================
def require_secret(secret: str, secret_name: str):
    """
    Skip the test if the required secret is not configured.

    Args:
        secret: Secret value.
        secret_name: Secret/environment variable name.
    """
    if not secret:
        pytest.skip(f"{secret_name} is not configured.")


# =============================================================================
# Basic Authentication
# =============================================================================
def test_basic_authentication(api_context):
    """
    Verify Basic Authentication using httpbin.
    """

    credentials = base64.b64encode(b"user:pass").decode("utf-8")

    response = api_context.get(
        "https://httpbin.org/basic-auth/user/pass",
        headers={"Authorization": f"Basic {credentials}"},
        timeout=30000,
    )

    # httpbin occasionally returns 503.
    if response.status == 503:
        pytest.skip("httpbin.org is temporarily unavailable.")

    assert (
        response.status == 200
    ), f"Expected 200 but received {response.status}"

    print("Response JSON:", response.json())


def test_basic_authentication_herokuapp(api_context):
    """
    Verify Basic Authentication using the-internet.herokuapp.com.
    """

    credentials = base64.b64encode(b"admin:admin").decode("utf-8")

    response = api_context.get(
        "https://the-internet.herokuapp.com/basic_auth",
        headers={"Authorization": f"Basic {credentials}"},
        timeout=30000,
    )

    assert (
        response.status == 200
    ), f"Expected 200 but received {response.status}"

    print("Response Body:", response.text())


# =============================================================================
# Bearer Token Authentication (GitHub)
# =============================================================================
def test_bearer_token_auth_github_repos(api_context):
    """
    Verify GitHub repository retrieval using a Personal Access Token.
    """

    require_secret(GITHUB_TOKEN, "GITHUB_TOKEN")

    response = api_context.get(
        "https://api.github.com/user/repos",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout=30000,
    )

    assert (
        response.status == 200
    ), f"GitHub API returned {response.status}"

    print("Repository Count:", len(response.json()))


def test_bearer_token_auth_github_user(api_context):
    """
    Verify authenticated GitHub user details.
    """

    require_secret(GITHUB_TOKEN, "GITHUB_TOKEN")

    response = api_context.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {GITHUB_TOKEN}"},
        timeout=30000,
    )

    assert (
        response.status == 200
    ), f"GitHub API returned {response.status}"

    print("Authenticated User:", response.json()["login"])


# =============================================================================
# API Key Authentication
# =============================================================================
def test_api_key_auth_open_weather(api_context):
    """
    Verify OpenWeather API authentication.
    """

    require_secret(OPENWEATHER_API_KEY, "OPENWEATHER_API_KEY")

    response = api_context.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "q": "Delhi",
            "appid": OPENWEATHER_API_KEY,
        },
        timeout=30000,
    )

    assert (
        response.status == 200
    ), f"OpenWeather returned {response.status}"

    print("City:", response.json()["name"])


def test_api_key_auth_weather_api(api_context):
    """
    Verify WeatherAPI authentication.
    """

    require_secret(WEATHERAPI_KEY, "WEATHERAPI_KEY")

    response = api_context.get(
        "https://api.weatherapi.com/v1/current.json",
        params={
            "q": "Bangalore",
            "key": WEATHERAPI_KEY,
        },
        timeout=30000,
    )

    assert (
        response.status == 200
    ), f"WeatherAPI returned {response.status}"

    print("Location:", response.json()["location"]["name"])


# =============================================================================
# OAuth2 Authentication (Imgur)
# =============================================================================
def test_oauth2_authentication_imgur(api_context):
    """
    Verify OAuth2 Authorization Code Flow using Imgur.

    NOTE:
    Imgur authorization codes are single-use and expire quickly.
    If this test fails with HTTP 400, generate a fresh authorization code.
    """

    require_secret(IMGUR_CLIENT_ID, "IMGUR_CLIENT_ID")
    require_secret(IMGUR_CLIENT_SECRET, "IMGUR_CLIENT_SECRET")
    require_secret(IMGUR_AUTH_CODE, "IMGUR_AUTH_CODE")

    token_response = api_context.post(
        "https://api.imgur.com/oauth2/token",
        form={
            "client_id": IMGUR_CLIENT_ID,
            "client_secret": IMGUR_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": IMGUR_AUTH_CODE,
            "redirect_uri": IMGUR_REDIRECT_URI,
        },
        timeout=30000,
    )

    assert (
        token_response.status == 200
    ), f"Token request failed with status {token_response.status}"

    token_data = token_response.json()

    access_token = token_data.get("access_token")

    assert access_token, "Access token not found."

    print("Access Token generated successfully.")

    image_response = api_context.get(
        "https://api.imgur.com/3/account/me/images",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30000,
    )

    assert (
        image_response.status == 200
    ), f"Image request failed with status {image_response.status}"

    print("Image Count:", len(image_response.json()["data"]))
