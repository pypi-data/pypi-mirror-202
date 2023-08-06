import unittest
from unittest.mock import Mock, patch

from ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor import (
    SalesforceQueryExecutor,
)


class TestSalesforceQueryExecutor(unittest.TestCase):
    def setUp(self):
        self.client_id = "test_client_id"
        self.username = "test_username"
        self.domain = "https://auth.example.com"
        self.private_key = "test_private_key"
        self.audience = "https://login.salesforce.com"

    def mocked_requests_post(self, *args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test_access_token"}
        return mock_response

    def mocked_requests_get_success(self, *args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "records": [{"Id": "001", "Name": "Test Record"}],
            "nextRecordsUrl": None,
        }
        return mock_response

    def mocked_requests_get_failure(self, *args, **kwargs):
        mock_response = Mock()
        mock_response.status_code = 400
        return mock_response

    @patch(
        "ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor.requests.post"  # noqa: E501
    )
    @patch(
        "ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor.requests.get"  # noqa: E501
    )
    def test_fetch_data_success(self, mock_get, mock_post):
        mock_post.side_effect = self.mocked_requests_post
        mock_get.side_effect = self.mocked_requests_get_success

        query_executor = SalesforceQueryExecutor(
            self.client_id,
            self.username,
            self.domain,
            self.private_key,
            self.audience,
        )

        query = "SELECT Id, Name FROM Account"
        records = query_executor.fetch_data(query)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["Id"], "001")
        self.assertEqual(records[0]["Name"], "Test Record")

    @patch(
        "ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor.requests.post"  # noqa: E501
    )
    @patch(
        "ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor.requests.get"  # noqa: E501
    )
    def test_fetch_data_failure(self, mock_get, mock_post):
        mock_post.side_effect = self.mocked_requests_post
        mock_get.side_effect = self.mocked_requests_get_failure

        query_executor = SalesforceQueryExecutor(
            self.client_id,
            self.username,
            self.domain,
            self.private_key,
            self.audience,
        )

        query = "SELECT Id, Name FROM Account"
        records = query_executor.fetch_data(query)

        self.assertEqual(records, [])

    @patch(
        "ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor.requests.post"  # noqa: E501
    )
    def test_auth_failure(self, mock_post):
        mock_post.return_value = Mock(status_code=400)

        query_executor = SalesforceQueryExecutor(
            self.client_id,
            self.username,
            self.domain,
            self.private_key,
            self.audience,
        )

        self.assertIsNone(query_executor.access_token)
