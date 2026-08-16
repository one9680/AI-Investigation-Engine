import os
import sys

import pytest


project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture(autouse=True)
def disable_live_gemini(monkeypatch):
    """
    Prevent automated tests from making real Gemini API calls.

    AI behavior is tested separately using mocks.
    """
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
