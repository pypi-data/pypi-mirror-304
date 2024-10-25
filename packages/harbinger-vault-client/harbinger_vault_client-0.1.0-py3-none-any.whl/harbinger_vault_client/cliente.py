import requests
import os
import json

class ContainerNameError(Exception):
    """Raised when the container name is not properly set."""
    pass

class VaultClient:
    def __init__(self, vault_url, auth_token):
        self.vault_url = vault_url
        self.auth_token = auth_token
        self.error = None
        self.container_name = None
        self.extra_headers = {}  # Initialize extra headers

        try:
            self.container_name = self._get_container_name()
        except ContainerNameError as e:
            self.error = str(e)

    def _get_container_name(self):
        container_name = os.environ.get('VAULT_CLIENT_CONTAINER_NAME')
        if not container_name:
            raise ContainerNameError("VAULT_CLIENT_CONTAINER_NAME environment variable is not set or empty")
        return container_name

    def set_extra_headers(self, headers):
        """Set extra headers to be included in the request."""
        self.extra_headers.update(headers)

    def get_credentials(self, cred_list):
        if self.error:
            return {
                "error": {
                    "code": 400,
                    "message": self.error
                }
            }
        
        try:
            payload = {
                "credentials": cred_list,
                "container_name": self.container_name
            }
            headers = {
                "Authorization": f"Bearer {self.auth_token}",
            }
            
            # Merge extra headers with default headers
            headers.update(self.extra_headers)
            
            response = requests.post(
                self.vault_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            response.raise_for_status()
            
            if not response.text:
                return {
                    "error": {
                        "code": 204,
                        "message": "Empty response from server"
                    }
                }
            
            try:
                return response.json()
            except json.JSONDecodeError:
                return {
                    "error": {
                        "code": 500,
                        "message": "Failed to decode JSON response"
                    },
                    "details": {
                        "status_code": response.status_code,
                        "content_type": response.headers.get('Content-Type')
                    }
                }
        except requests.exceptions.RequestException as e:
            return {
                "error": {
                    "code": 500,
                    "message": f"Failed to retrieve credentials: {str(e)}"
                }
            }
