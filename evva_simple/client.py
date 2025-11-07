"""
Main client for Evva AirKey API
"""

import logging
from typing import Any, Dict, List, Optional
import requests

from .exceptions import (
    EvvaAPIError,
    EvvaAuthenticationError,
    EvvaNotFoundError,
    EvvaValidationError,
)


class EvvaClient:
    """Simple client for interacting with the Evva AirKey API"""

    DEFAULT_BASE_URL = "https://integration.api.airkey.evva.com"

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = 30,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize the Evva AirKey client.

        Args:
            api_key: Your Evva AirKey API key
            base_url: Base URL for the API (defaults to production endpoint)
            timeout: Request timeout in seconds
            logger: Optional logger instance
        """
        self.api_key = api_key
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Make an API request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            params: Query parameters
            json_data: JSON request body

        Returns:
            Response data

        Raises:
            EvvaAuthenticationError: If authentication fails
            EvvaNotFoundError: If resource is not found
            EvvaValidationError: If request validation fails
            EvvaAPIError: For other API errors
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                timeout=self.timeout,
            )

            # Handle different status codes
            if response.status_code == 401:
                raise EvvaAuthenticationError("Authentication failed. Check your API key.")
            elif response.status_code == 404:
                raise EvvaNotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code == 400:
                error_msg = response.text or "Validation error"
                raise EvvaValidationError(f"Validation error: {error_msg}")
            elif response.status_code >= 400:
                raise EvvaAPIError(
                    f"API error {response.status_code}: {response.text}"
                )

            response.raise_for_status()

            # Return empty dict for 204 No Content
            if response.status_code == 204:
                return {}

            return response.json() if response.content else {}

        except requests.exceptions.Timeout:
            raise EvvaAPIError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise EvvaAPIError(f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            if not isinstance(e, (EvvaAPIError, EvvaAuthenticationError, EvvaNotFoundError)):
                raise EvvaAPIError(f"Request failed: {str(e)}")
            raise

    # Lock operations
    def list_locks(
        self, offset: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all locks.

        Args:
            offset: Pagination offset
            limit: Number of results per page

        Returns:
            List of lock objects
        """
        return self._request(
            "GET", "/v1/locks", params={"offset": offset, "limit": limit}
        )

    def get_lock(self, lock_id: str) -> Dict[str, Any]:
        """
        Get details of a specific lock.

        Args:
            lock_id: Lock ID

        Returns:
            Lock object
        """
        return self._request("GET", f"/v1/locks/{lock_id}")

    # Person operations
    def list_persons(
        self, offset: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all persons.

        Args:
            offset: Pagination offset
            limit: Number of results per page

        Returns:
            List of person objects
        """
        return self._request(
            "GET", "/v1/persons", params={"offset": offset, "limit": limit}
        )

    def get_person(self, person_id: str) -> Dict[str, Any]:
        """
        Get details of a specific person.

        Args:
            person_id: Person ID

        Returns:
            Person object
        """
        return self._request("GET", f"/v1/persons/{person_id}")

    def create_person(
        self,
        first_name: str,
        last_name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new person.

        Args:
            first_name: Person's first name
            last_name: Person's last name
            email: Person's email address
            phone: Person's phone number

        Returns:
            Created person object
        """
        data = {
            "firstName": first_name,
            "lastName": last_name,
        }
        if email:
            data["email"] = email
        if phone:
            data["phoneNumber"] = phone

        return self._request("POST", "/v1/persons", json_data=data)

    def delete_person(self, person_id: str) -> None:
        """
        Delete a person.

        Args:
            person_id: Person ID
        """
        self._request("DELETE", f"/v1/persons/{person_id}")

    # Authorization operations
    def list_authorizations(
        self, offset: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all authorizations.

        Args:
            offset: Pagination offset
            limit: Number of results per page

        Returns:
            List of authorization objects
        """
        return self._request(
            "GET", "/v1/authorizations", params={"offset": offset, "limit": limit}
        )

    def create_authorization(
        self,
        medium_id: str,
        lock_id: str,
        valid_from: str,
        valid_to: str,
    ) -> Dict[str, Any]:
        """
        Create a new authorization for a medium to access a lock.

        Args:
            medium_id: Access medium ID (smartphone, card, etc.)
            lock_id: Lock ID
            valid_from: Start timestamp (ISO 8601 format)
            valid_to: End timestamp (ISO 8601 format)

        Returns:
            Created authorization object
        """
        data = {
            "mediumId": medium_id,
            "lockId": lock_id,
            "validFrom": valid_from,
            "validTo": valid_to,
        }
        return self._request("POST", "/v1/authorizations", json_data=data)

    def delete_authorization(self, authorization_id: str) -> None:
        """
        Delete an authorization.

        Args:
            authorization_id: Authorization ID
        """
        self._request("DELETE", f"/v1/authorizations/{authorization_id}")

    # Access media operations
    def list_media(
        self, offset: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all access media (smartphones, cards, key tags).

        Args:
            offset: Pagination offset
            limit: Number of results per page

        Returns:
            List of medium objects
        """
        return self._request(
            "GET", "/v1/media", params={"offset": offset, "limit": limit}
        )

    def get_medium(self, medium_id: str) -> Dict[str, Any]:
        """
        Get details of a specific access medium.

        Args:
            medium_id: Medium ID

        Returns:
            Medium object
        """
        return self._request("GET", f"/v1/media/{medium_id}")
