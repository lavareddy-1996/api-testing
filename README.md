# API Test Automation Framework

API test automation built with **Playwright (Python)** and **PyTest**, covering
authentication, headers/cookies, JSON schema validation, and full CRUD
workflows against public practice APIs (Restful Booker, JSONPlaceholder,
GitHub, OpenWeatherMap, WeatherAPI, Imgur).

## Folder structure
api-automation-framework/
├── .github/workflows/api-tests.yml   # CI: runs tests on every push/PR
├── config/
│   └── config.py                     # Reads secrets/URLs from env vars
├── tests/
│   ├── auth/
│   │   └── test_auth.py              # Basic, Bearer, API key, OAuth2
│   ├── booking/
│   │   ├── test_create_booking.py
│   │   ├── test_create_booking_faker.py
│   │   ├── test_create_booking_json.py
│   │   └── test_crud_operations.py   # Full Create→Read→Update→Delete flow
│   ├── headers_cookies/
│   │   ├── test_cookies_response.py
│   │   ├── test_headers.py
│   │   └── test_headers_response.py
│   └── schema/
│       └── test_json_schema_validation.py
├── testdata/                         # JSON payloads used by data-driven tests
├── utils/
│   └── json_reader.py                # Shared helper to load testdata/*.json
├── conftest.py                       # Shared `api_context` fixture
├── pytest.ini
├── requirements.txt
├── .env.example                      # Template - copy to .env, fill in real values
└── .gitignore                        # Excludes .env, caches, reports


## Setup

```bash
# 1. Clone and enter the repo
git clone <your-repo-url>
cd api-automation-framework

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
playwright install

# 4. Set up local secrets
cp .env.example .env
# then edit .env and fill in real values
```

## Running tests

```bash
# Run everything
pytest

# Run one feature folder
pytest tests/booking/

# Run a single file
pytest tests/auth/test_auth.py

# HTML report is generated automatically at reports/report.html
```

## Design notes

- **Secrets are never hardcoded.** All API keys/tokens are loaded from
  environment variables via `config/config.py` and `python-dotenv`. Only
  `.env.example` (placeholders) is committed - the real `.env` is
  gitignored.
- **Shared fixture (`conftest.py`)** provides a fresh `api_context` per
  test, so individual test files don't manage setup/teardown themselves.
- **`tests/booking/test_crud_operations.py`** uses its own module-scoped
  fixture instead of the shared one, since its tests intentionally run in
  sequence and share state (`booking_id`, `token`) across the file.
- **Test data lives in `testdata/*.json`**, loaded via `utils/json_reader.py`
  using a path resolved relative to the project root - so tests work no
  matter which directory `pytest` is run from.
- **CI (`.github/workflows/api-tests.yml`)** runs the full suite on every
  push/PR to `main` and uploads the HTML report as a build artifact. Add
  your real secrets under the repo's Settings → Secrets and variables →
  Actions (names must match the workflow file, e.g. `GH_TOKEN`,
  `OPENWEATHER_API_KEY`, etc.).

## Known limitations / things to note

- `tests/headers_cookies/test_headers_response.py` asserts an exact
  `gzip` content-encoding, which can be flaky since Google may serve
  `br` or `zstd` depending on client/region. Left intentionally as a
  contrast to the more tolerant check in `test_headers.py`.
- The Imgur OAuth2 test requires a fresh, manually-obtained authorization
  code before each run (codes are single-use and short-lived).
- `testdata/*.json` files were reconstructed to match this framework's
  structure - adjust values as needed for your own test scenarios.
