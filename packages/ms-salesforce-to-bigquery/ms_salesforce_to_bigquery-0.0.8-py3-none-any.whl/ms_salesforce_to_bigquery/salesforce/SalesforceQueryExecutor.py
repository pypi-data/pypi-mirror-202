import logging
import time

import requests

from ms_salesforce_to_bigquery.salesforce.Auth import SalesforceAuthenticator

DEFAULT_SALESFORCE_VERSION = "57.0"
SALESFORCE_QUERY_ENDPOINT = "services/data/v{}/query/"


class SalesforceQueryExecutor(SalesforceAuthenticator):
    def __init__(
        self,
        client_id,
        username,
        domain,
        private_key,
        audience="https://login.salesforce.com",
        session_duration_hours=1,
        api_version=DEFAULT_SALESFORCE_VERSION,
    ):
        super().__init__(
            client_id,
            username,
            domain,
            private_key,
            audience,
            session_duration_hours,
        )
        self.endpoint = (
            f"{domain}/{SALESFORCE_QUERY_ENDPOINT.format(api_version)}"
        )
        self.domain = domain
        self.access_token = self.authenticate()

    def fetch_data(self, query: str):
        if not self.access_token:
            logging.error("Authentication failed, cannot fetch data")
            return None

        headers = {"Authorization": f"Bearer {self.access_token}"}

        all_records = []
        next_url = f"{self.endpoint}?q={query}"

        while next_url:
            response = self._make_request(next_url, headers)
            if response:
                data = response.json()
                all_records.extend(data.get("records", []))
                nextRecordsUrl = data.get("nextRecordsUrl", None)
                if nextRecordsUrl:
                    next_url = f"{self.domain}{nextRecordsUrl}"
                else:
                    next_url = None
            else:
                next_url = None

        return all_records

    def _make_request(self, url, headers):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            else:
                logging.error(
                    f"Request failed with status code: {response.status_code}"
                )
                return None
        except requests.exceptions.Timeout:
            logging.warning("Request timeout, retrying in 2 seconds")
            time.sleep(2)
            return self._make_request(url, headers)
