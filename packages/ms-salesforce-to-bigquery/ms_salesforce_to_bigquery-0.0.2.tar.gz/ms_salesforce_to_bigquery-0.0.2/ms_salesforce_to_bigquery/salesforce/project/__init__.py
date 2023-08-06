import logging

from ms_salesforce_to_bigquery.salesforce.project.dto import OpportunityDTO
from ms_salesforce_to_bigquery.salesforce.SalesforceQueryExecutor import (
    SalesforceQueryExecutor,
)

DEFAULT_PROJECT_OPPORTUNITY_QUERY = "SELECT+Project_Account__r.Business_Name__c,Project_Account__r.Name,CurrencyIsoCode,Total_Project_Amount__c,Invoicing_Country_Code__c,Operation_Coordinator__r.Name,Operation_Coordinator_Sub__r.Name,CreatedDate,LastModifiedDate,Opportunity__r.Opportunity_Name_Short__c,Opportunity__r.StageName,Opportunity__r.LeadSource,Project_Account__r.BillingCountryCode,FRM_MSProjectCode__c,Name,Start_Date__c,Operation_Coordinator__r.Controller__c,Operation_Coordinator_Sub__r.Controller_SUB__c,Profit_Center__c,Cost_Center__c,Opportunity__r.Probability,Opportunity__r.Tier_Short__c,Opportunity__r.JiraComponentURL__c+FROM+Project__c"  # noqa: E501


class Project(SalesforceQueryExecutor):
    def get_opportunities(
        self,
        query: str = DEFAULT_PROJECT_OPPORTUNITY_QUERY,
    ):
        try:
            data = self.fetch_data(query)
            if data is None:
                return []

            opportunities = [
                OpportunityDTO.from_salesforce_record(record)
                for record in data
            ]
            return opportunities
        except Exception as e:
            logging.error(f"Failed to get opportunities: {e}")
            return []
