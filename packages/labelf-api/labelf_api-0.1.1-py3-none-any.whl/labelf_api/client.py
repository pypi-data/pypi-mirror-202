import requests
import logging

from typing import Dict, List, Union
import time
from .exceptions import LabelfError, LabelfAPIError

logger = logging.getLogger(__name__)


class LabelfClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires_in = None
        self._get_bearer_token()

    def _get_bearer_token(self):
        """Obtain a bearer token for authentication."""
        data = {"grant_type": "client_credentials"}
        response = requests.post(
            "https://auth.app.labelf.ai/oauth2/token",
            data=data,
            auth=(self.client_id, self.client_secret),
        )
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            self.token_expires_in = token_data["expires_in"]
        else:
            raise LabelfAPIError(f"Error obtaining bearer token: {response.text}")

    def _validate_input(
        self, input_value, input_name, input_type, input_condition=None
    ):
        """Validate input parameters."""
        if not isinstance(input_value, input_type) or (
            input_condition is not None and not input_condition(input_value)
        ):
            raise ValueError(
                f"{input_name} must be a {input_type.__name__} and meet the specified condition"
            )
        return input_value

    def _request_with_retry(
        self,
        method: str,
        url: str,
        headers: Dict[str, str] = None,
        json: Dict = None,
        retries: int = 3,
    ) -> requests.Response:
        """
        Make an API request with retries for specific errors.
        Retries if the bearer token has expired or if the server returns a 5xx error.
        """
        for attempt in range(retries):
            try:
                response = requests.request(method, url, headers=headers, json=json)
                response.raise_for_status()
                return response
            except requests.exceptions.HTTPError as e:
                if (
                    response.status_code == 401
                ):  # Unauthorized, token might have expired
                    self._get_bearer_token()
                elif 500 <= response.status_code < 600:  # Server errors (5xx)
                    logger.warning(f"Server error, retrying ({attempt + 1}/{retries})")
                    time.sleep(10)
                else:
                    raise LabelfAPIError(
                        f"Error in API request: {response.text}"
                    ) from e
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error: {e}")
                raise LabelfError("Request error") from e
        raise LabelfError("Max retries exceeded")

    def get_predictions(
        self, model_id: str, texts: List[str], max_predictions: int = 2
    ) -> List[Dict[str, Union[str, List[Dict[str, float]]]]]:
        """
        Get predictions for the given texts using the specified model.

        Args:
            model_id (str): The ID of the model to use for predictions.
            texts (List[str]): A list of texts to get predictions for.
            max_predictions (int, optional): The maximum number of predictions to return for each text. Defaults to 2.

        Returns:
            List[Dict[str, Union[str, List[Dict[str, float]]]]]: A list of dictionaries containing the input text and its predictions.

        Example:
            Input:
                model_id = "YOUR_MODEL_ID"
                texts = ["Breakfast was not tasty"]
            Output:
                [
                    {
                        "text": "Breakfast was not tasty",
                        "predictions": [
                            {"label": "positive", "score": 0.93},
                            {"label": "neutral", "score": 0.03}
                        ]
                    }
                ]
        """
        self._validate_input(model_id, "model_id", str, lambda x: bool(x))
        self._validate_input(
            texts,
            "texts",
            list,
            lambda x: bool(x) and all(isinstance(text, str) for text in x),
        )
        self._validate_input(max_predictions, "max_predictions", int, lambda x: x > 0)

        headers = {"Authorization": f"Bearer {self.token}"}
        json_data = {"texts": texts, "max_predictions": max_predictions}
        response = self._request_with_retry(
            "POST",
            f"https://api.app.labelf.ai/v2/models/{model_id}/inference",
            headers=headers,
            json=json_data,
        )
        return response.json()

    def check_similarity(
        self, top_n: int, base_texts: Dict[str, str], compare_to_texts: Dict[str, str]
    ) -> Dict[str, List[Dict[str, Union[str, float]]]]:
        """
        Check the similarity between base_texts and compare_to_texts.

        Args:
            top_n (int): The number of highest similarity texts to show for each comparison text.
            base_texts (Dict[str, str]): A dictionary of base texts with unique IDs as keys.
            compare_to_texts (Dict[str, str]): A dictionary of texts to compare to the base texts with unique IDs as keys.

        Returns:
            Dict[str, List[Dict[str, Union[str, float]]]]: A dictionary with the compare_to_texts IDs as keys and a list of dictionaries containing the base text IDs and their similarity scores.

        Example:
            Input:
                top_n = 2
                base_texts = {"example_id1": "This is an example.", "example_id2": "How are you?"}
                compare_to_texts = {"example_compare_id1": "This is also an example", "example_compare_id2": "Airplanes are cool"}
            Output:
                {
                    "example_compare_id1": [
                        {"id": "example_id1", "similarity": 0.9277236631938389},
                        {"id": "example_id2", "similarity": 0.0680591436014289}
                    ],
                    "example_compare_id2": [
                        {"id": "example_id1", "similarity": 0.242408965890472},
                        {"id": "example_id2", "similarity": 0.2152906189362208}
                    ]
                }
        """
        self._validate_input(top_n, "top_n", int, lambda x: x > 0)
        self._validate_input(
            base_texts,
            "base_texts",
            dict,
            lambda x: bool(x)
            and all(isinstance(k, str) and isinstance(v, str) for k, v in x.items()),
        )
        self._validate_input(
            compare_to_texts,
            "compare_to_texts",
            dict,
            lambda x: bool(x)
            and all(isinstance(k, str) and isinstance(v, str) for k, v in x.items()),
        )

        headers = {"Authorization": f"Bearer {self.token}"}
        json_data = {
            "top_n": top_n,
            "base_texts": base_texts,
            "compare_to_texts": compare_to_texts,
        }
        response = self._request_with_retry(
            "POST",
            "https://api.app.labelf.ai/v2/similarity",
            headers=headers,
            json=json_data,
        )
        return response.json()
