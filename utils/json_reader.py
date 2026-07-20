import json
import os

# Resolve testdata/ relative to the project root, regardless of which
# directory pytest is invoked from or how deeply nested the test file is.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTDATA_DIR = os.path.join(PROJECT_ROOT, "testdata")


def read_json(filename: str) -> dict:
    """Reads and returns a JSON test-data file from the testdata/ folder."""
    path = os.path.join(TESTDATA_DIR, filename)
    with open(path, "r") as f:
        return json.load(f)
