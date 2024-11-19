import os
import pytest
import shutil
from src.data_extraction import fetch_papers, save_to_csv, CATEGORY_MAP

# Mock environment variables
os.environ["IEEE_API_KEY"] = "mock_api_key"

# Mock data for testing
mock_articles = [
    {
        "title": "Test Paper 1",
        "abstract": "This is a test abstract for DC-DC converter.",
        "authors": ["Author A"],
        "publication_year": 2023,
    },
    {
        "title": "Test Paper 2",
        "abstract": "This is a test abstract for Inverter.",
        "authors": ["Author B"],
        "publication_year": 2024,
    },
]


@pytest.fixture
def setup_tmp_dir():
    """Setup a temporary directory for testing."""
    tmp_dir = os.path.join("./bin", "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    yield tmp_dir  # Provide the temporary directory to the test
    # Teardown: Remove the directory after the test
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_fetch_papers(monkeypatch):
    """Test fetch_papers with a mock response."""

    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {"articles": mock_articles}

        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    query = "(dc-dc converter|dc/dc converter)"
    papers = fetch_papers(query)
    assert len(papers) == 2
    assert papers[0]["title"] == "Test Paper 1"


def test_save_to_csv(setup_tmp_dir):
    """Test save_to_csv creates the correct file in the custom directory."""
    query = "dc-dc converter OR dc/dc converter"
    timestamp = "20231117_120000"

    save_to_csv(mock_articles, query, timestamp, data_dir_path=setup_tmp_dir)

    expected_category = CATEGORY_MAP[query]
    expected_file = os.path.join(setup_tmp_dir, f"{expected_category}_{timestamp}.csv")
    assert os.path.exists(expected_file)
