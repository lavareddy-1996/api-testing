"""
Centralized config for the framework.

All secrets/API keys are read from environment variables (populated from
a local .env file via python-dotenv, or from CI secrets in GitHub Actions).
Never hardcode real credentials in test files or commit a real .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Third-party API credentials (see .env.example for required keys) -----
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
WEATHERAPI_KEY = os.environ.get("WEATHERAPI_KEY")

IMGUR_CLIENT_ID = os.environ.get("IMGUR_CLIENT_ID")
IMGUR_CLIENT_SECRET = os.environ.get("IMGUR_CLIENT_SECRET")
IMGUR_REDIRECT_URI = os.environ.get(
    "IMGUR_REDIRECT_URI", "https://www.getpostman.com/oauth2/callback"
)
IMGUR_AUTH_CODE = os.environ.get("IMGUR_AUTH_CODE")

# --- Base URLs --------------------------------------------------------------
RESTFUL_BOOKER_BASE_URL = os.environ.get(
    "RESTFUL_BOOKER_BASE_URL", "https://restful-booker.herokuapp.com"
)
