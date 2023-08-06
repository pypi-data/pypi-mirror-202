import pytest
from labelf_api import LabelfClient

# Replace with your own CLIENT_ID and CLIENT_SECRET
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"


@pytest.fixture
def client():
    return LabelfClient(CLIENT_ID, CLIENT_SECRET)


def test_get_predictions(client):
    model_id = "YOUR_MODEL_ID"
    texts = ["Breakfast was not tasty"]
    result = client.get_predictions(model_id, texts)
    assert isinstance(result, list)
    assert len(result) == 1
    assert "text" in result[0]
    assert "predictions" in result[0]


def test_check_similarity(client):
    top_n = 2
    base_texts = {"example_id1": "This is an example.", "example_id2": "How are you?"}
    compare_to_texts = {
        "example_compare_id1": "This is also an example",
        "example_compare_id2": "Airplanes are cool",
    }
    result = client.check_similarity(top_n, base_texts, compare_to_texts)
    assert isinstance(result, dict)
    assert len(result) == len(compare_to_texts)
