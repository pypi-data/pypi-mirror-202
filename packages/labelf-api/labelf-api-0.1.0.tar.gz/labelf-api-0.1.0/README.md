# Labelf API Python Package

A Python package for interacting with the LabelF API.

## Installation

```bash
pip install labelf-api
```

## Usage

```python
from labelf_api import LabelfClient

client = LabelfClient("CLIENT_ID", "CLIENT_SECRET")

# Get predictions
model_id = "YOUR_MODEL_ID"
texts = ["Breakfast was not tasty"]
result = client.get_predictions(model_id, texts)

# Check similarity
top_n = 2
base_texts = {"example_id1": "This is an example.", "example_id2": "How are you?"}
compare_to_texts = {"example_compare_id1": "This is also an example", "example_compare_id2": "Airplanes are cool"}
result = client.check_similarity(top_n, base_texts, compare_to_texts)
```

## Running Tests

```bash
pytest tests/
```


To submit the package to PyPI, follow the instructions in the [Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/).