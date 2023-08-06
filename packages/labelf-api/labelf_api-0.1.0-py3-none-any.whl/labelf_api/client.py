import requests
from typing import Dict, List, Union
from .exceptions import LabelfError, LabelfAPIError


class LabelfClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expires_in = None
        self._get_bearer_token()

    def _get_bearer_token(self):
        data = {"grant_type": "client_credentials"}
        response = requests.post(
            "https://auth.app.labelf.ai/oauth2/token",
            data=data,
            verify=True,
            auth=(self.client_id, self.client_secret),
        )
        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data["access_token"]
            self.token_expires_in = token_data["expires_in"]
        else:
            raise LabelfAPIError(f"Error obtaining bearer token: {response.text}")

    def _request_with_retry(
        self,
        method: str,
        url: str,
        headers: Dict[str, str] = None,
        json: Dict = None,
        retries: int = 3,
    ) -> requests.Response:
        for _ in range(retries):
            response = requests.request(method, url, headers=headers, json=json)
            if response.status_code == 200:
                return response
            elif response.status_code == 401:  # Unauthorized, token might have expired
                self._get_bearer_token()
            elif response.status_code[0] == 5:  # Service Unavailable
                continue
            else:
                raise LabelfAPIError(f"Error in API request: {response.text}")
        raise LabelfError("Max retries exceeded")

    def get_predictions(
        self, model_id: str, texts: List[str], max_predictions: int = 2
    ) -> List[Dict[str, Union[str, List[Dict[str, float]]]]]:
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
