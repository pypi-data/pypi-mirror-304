import requests
from dataclasses import dataclass
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Token:
    access_token: str
    token_type: str
    expires_in: int

class AuthenticationError(Exception):
    pass

class AccessManagement:
    BASE_URL = "https://anypoint.mulesoft.com"

    @staticmethod
    def get_access_token(client_id: str, client_secret: str) -> Token:
        logger.info("Authenticating with Anypoint Platform")
        url = f"{AccessManagement.BASE_URL}/accounts/api/v2/oauth2/token"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            return Token(
                access_token=data["access_token"],
                token_type=data["token_type"],
                expires_in=data["expires_in"]
            )
        except requests.exceptions.HTTPError as e:
            # Raise an AuthenticationError if the HTTP Status is 401 or 403
            if e.response.status_code in (401, 403):
                error_message = f"Authentication failed: HTTP {e.response.status_code} - {e.response.text}"
                raise AuthenticationError(error_message)
            else:
                raise  # Re-raise other HTTP errors

    @staticmethod
    def get_business_group_id(access_token: str, bg_name: str) -> Optional[str]:
        logger.info(f"Getting Business Group ID for: {bg_name}")
        url = f"{AccessManagement.BASE_URL}/accounts/api/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for org in data.get("user", {}).get("memberOfOrganizations", []):
                if org["name"] == bg_name:
                    return org["id"]
            
            logger.info(f"Business Group '{bg_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting Business Group ID: HTTP {e.response.status_code} - {e.response.text}")
            return None

    @staticmethod
    def get_environment_id(access_token: str, bg_id: str, env_name: str) -> Optional[str]:
        logger.info(f"Getting Environment ID for: {env_name}")
        url = f"{AccessManagement.BASE_URL}/accounts/api/organizations/{bg_id}/environments"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for env in data.get("data", []):
                if env["name"] == env_name:
                    return env["id"]
            
            logger.info(f"Environment '{env_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting Environment ID: HTTP {e.response.status_code} - {e.response.text}")
            return None

    @staticmethod
    def get_client_provider_id(access_token: str, bg_id: str, provider_name: str) -> Optional[str]:
        logger.info(f"Getting Client Provider ID for: {provider_name}")
        url = f"{AccessManagement.BASE_URL}/accounts/api/cs/organizations/{bg_id}/clientProviders"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for provider in data.get("data", []):
                if provider.get("name") == provider_name:
                    return provider.get("providerId")
            logger.info(f"Client Provider '{provider_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting Client Provider ID: HTTP {e.response.status_code} - {e.response.text}")
            return None

__all__ = ['AccessManagement', 'AuthenticationError', 'Token']