"""Test configuration and fixtures."""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def sample_pdf_path():
    """Path to a sample PDF file for testing."""
    # This would be a real PDF file in your test assets
    return "tests/assets/sample.pdf"


@pytest.fixture
def mock_credentials_path(temp_dir):
    """Create a mock credentials file."""
    creds_path = temp_dir / "test_gcp.json"
    creds_content = {
        "type": "service_account",
        "project_id": "test-project",
        "private_key_id": "test-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\ntest-key\n-----END PRIVATE KEY-----\n",
        "client_email": "test@test-project.iam.gserviceaccount.com",
        "client_id": "123456789",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }

    import json
    with open(creds_path, 'w') as f:
        json.dump(creds_content, f)

    return str(creds_path)