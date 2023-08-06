import unittest
from unittest.mock import MagicMock, patch

from ms_salesforce_to_bigquery.salesforce.project import (
    OpportunityDTO,
    Project,
)

EXAMPLE_RESPONSE = {
    "totalSize": 1,
    "done": True,
    "records": [
        {
            "attributes": {
                "type": "Project__c",
                "url": "/services/data/v57.0/sobjects/Project__c/a00AX0000041OwAYAU",  # noqa: E501
            },
            "Project_Account__r": {
                "attributes": {
                    "type": "Account",
                    "url": "/services/data/v57.0/sobjects/Account/001AX000003gVPsYAM",  # noqa: E501
                },
                "Business_Name__c": "Five Eight Twenty-Two Consulting Inc.",
                "Name": "5822",
                "BillingCountryCode": "CA",
            },
            "CurrencyIsoCode": "CAD",
            "Total_Project_Amount__c": 30000.0,
            "Invoicing_Country_Code__c": "ES",
            "Operation_Coordinator__r": {
                "attributes": {
                    "type": "Operation_Coordinator__c",
                    "url": "/services/data/v57.0/sobjects/Operation_Coordinator__c/a0uG50000001crFIAQ",  # noqa: E501
                },
                "Name": "jhon.doe@ext.makingscience.com",
                "Controller__c": None,
            },
            "Operation_Coordinator_Sub__r": {
                "attributes": {
                    "type": "Operation_Coordinator__c",
                    "url": "/services/data/v57.0/sobjects/Operation_Coordinator__c/a0uG50000001crFIAQ",  # noqa: E501
                },
                "Name": "jhon.doe@ext.makingscience.com",
                "Controller_SUB__c": "jhon.doe@ext.makingscience.com",
            },
            "CreatedDate": "2023-02-15T09:30:06.000+0000",
            "LastModifiedDate": "2023-04-04T10:43:24.000+0000",
            "Opportunity__r": {
                "attributes": {
                    "type": "Opportunity",
                    "url": "/services/data/v57.0/sobjects/Opportunity/006AX000003uMSzYAM",  # noqa: E501
                },
                "Opportunity_Name_Short__c": "5822 - GA4 implement",
                "StageName": "Closed Won",
                "LeadSource": "Partner: Local Planet",
                "Probability": 100.0,
                "Tier_Short__c": "Unkown",
                "JiraComponentURL__c": '<a href="https://makingscience.atlassian.net/browse/ESMSBD0001-10324" target="_blank">View Jira Task</a>',  # noqa: E501
            },
            "FRM_MSProjectCode__c": "ESMSEX06536",
            "Name": "EasyFinancialSupport",
            "Start_Date__c": "2023-02-01",
            "Profit_Center__c": None,
            "Cost_Center__c": None,
        }
    ],
}


class TestProject(unittest.TestCase):
    @patch(
        "ms_salesforce_to_bigquery.salesforce.project.SalesforceQueryExecutor.authenticate"  # noqa: E501
    )
    @patch(
        "ms_salesforce_to_bigquery.salesforce.project.SalesforceQueryExecutor._make_request"  # noqa: E501
    )
    def test_get_opportunities(self, mock_make_request, mock_authenticate):
        mock_authenticate.return_value = "access_token"
        mock_make_request.return_value = MagicMock()
        mock_make_request.return_value.json.return_value = EXAMPLE_RESPONSE

        client_id = "client_id"
        username = "username"
        domain = "https://auth.example.com"
        private_key = "private_key"

        project = Project(
            client_id,
            username,
            domain,
            private_key,
            audience="https://login.salesforce.com",
        )
        query = "SELECT * FROM Opportunity"

        opportunities = project.get_opportunities(query)
        self.assertEqual(len(opportunities), 1)

        opportunity = opportunities[0]
        self.assertIsInstance(opportunity, OpportunityDTO)
        self.assertEqual(
            opportunity.client_fiscal_name,
            "Five Eight Twenty-Two Consulting Inc.",
        )
        self.assertEqual(opportunity.client_account_name, "5822")
        self.assertEqual(opportunity.currency, "CAD")
        self.assertEqual(opportunity.amount, 30000.0)
        self.assertEqual(opportunity.invoicing_country_code, "ES")
        self.assertEqual(
            opportunity.operation_coordinator_email,
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity.operation_coordinator_sub_email,
            "jhon.doe@ext.makingscience.com",
        )
        self.assertEqual(
            opportunity.created_at, "2023-02-15T09:30:06.000+0000"
        )
        self.assertEqual(
            opportunity.last_updated_at, "2023-04-04T10:43:24.000+0000"
        )
        self.assertEqual(opportunity.opportunity_name, "5822 - GA4 implement")
        self.assertEqual(opportunity.stage, "Closed Won")
        self.assertEqual(opportunity.billing_country, "CA")
        self.assertEqual(opportunity.lead_source, "Partner: Local Planet")
        self.assertEqual(opportunity.project_code, "ESMSEX06536")
        self.assertEqual(opportunity.project_id, "")
        self.assertEqual(opportunity.project_name, "EasyFinancialSupport")
        self.assertEqual(opportunity.project_start_date, "2023-02-01")
        self.assertIsNone(opportunity.controller_email)
        self.assertEqual(
            opportunity.controller_sub_email, "jhon.doe@ext.makingscience.com"
        )
        self.assertIsNone(opportunity.profit_center)
        self.assertIsNone(opportunity.cost_center)
        self.assertEqual(opportunity.project_tier, "Unkown")
        self.assertEqual(
            opportunity.jira_task_url,
            '<a href="https://makingscience.atlassian.net/browse/ESMSBD0001-10324" target="_blank">View Jira Task</a>',  # noqa: E501
        )
        self.assertEqual(opportunity.opportunity_percentage, 100.0)

        mock_make_request.assert_called()

    @patch(
        "ms_salesforce_to_bigquery.salesforce.project.SalesforceQueryExecutor.authenticate"  # noqa: E501
    )
    @patch(
        "ms_salesforce_to_bigquery.salesforce.project.SalesforceQueryExecutor._make_request"  # noqa: E501
    )
    def test_get_opportunities_empty_on_failure(
        self, mock_make_request, mock_authenticate
    ):
        mock_authenticate.return_value = "access_token"
        mock_make_request.return_value = None

        client_id = "client_id"
        username = "username"
        domain = "https://auth.example.com"
        private_key = "private_key"

        project = Project(
            client_id,
            username,
            domain,
            private_key,
            audience="https://login.salesforce.com",
        )
        query = "SELECT * FROM Opportunity"

        opportunities = project.get_opportunities(query)
        self.assertEqual(opportunities, [])

        mock_make_request.assert_called()
