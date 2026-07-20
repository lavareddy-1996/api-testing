import pytest
from playwright.sync_api import Playwright


@pytest.fixture
def api_context(playwright: Playwright):
    """
    Provides a fresh Playwright APIRequestContext for a single test.
    Automatically disposed after the test finishes, so individual
    test files no longer need to create/dispose the context themselves.
    """
    context = playwright.request.new_context()
    yield context
    context.dispose()
