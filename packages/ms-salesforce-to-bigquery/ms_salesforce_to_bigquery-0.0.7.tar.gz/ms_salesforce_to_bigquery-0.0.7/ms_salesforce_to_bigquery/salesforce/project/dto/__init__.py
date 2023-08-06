class OpportunityDTO:
    def __init__(
        self,
        client_fiscal_name,
        client_account_name,
        currency,
        amount,
        invoicing_country_code,
        operation_coordinator_email,
        operation_coordinator_sub_email,
        created_at,
        last_updated_at,
        opportunity_name,
        stage,
        billing_country,
        lead_source,
        project_code,
        project_id,
        project_name,
        project_start_date,
        controller_email,
        controller_sub_email,
        profit_center,
        cost_center,
        project_tier,
        jira_task_url,
        opportunity_percentage,
    ):
        self.client_fiscal_name = client_fiscal_name
        self.client_account_name = client_account_name
        self.currency = currency
        self.amount = amount
        self.invoicing_country_code = invoicing_country_code
        self.operation_coordinator_email = operation_coordinator_email
        self.operation_coordinator_sub_email = operation_coordinator_sub_email
        self.created_at = created_at
        self.last_updated_at = last_updated_at
        self.opportunity_name = opportunity_name
        self.stage = stage
        self.billing_country = billing_country
        self.lead_source = lead_source
        self.project_code = project_code
        self.project_id = project_id
        self.project_name = project_name
        self.project_start_date = project_start_date
        self.controller_email = controller_email
        self.controller_sub_email = controller_sub_email
        self.profit_center = profit_center
        self.cost_center = cost_center
        self.project_tier = project_tier
        self.jira_task_url = jira_task_url
        self.opportunity_percentage = opportunity_percentage

    @staticmethod
    def from_salesforce_record(record):
        return OpportunityDTO(
            client_fiscal_name=record["Project_Account__r"][
                "Business_Name__c"
            ],
            client_account_name=record["Project_Account__r"]["Name"],
            currency=record["CurrencyIsoCode"],
            amount=record["Total_Project_Amount__c"],
            invoicing_country_code=record["Invoicing_Country_Code__c"],
            operation_coordinator_email=record["Operation_Coordinator__r"][
                "Name"
            ],
            operation_coordinator_sub_email=record[
                "Operation_Coordinator_Sub__r"
            ]["Name"],
            created_at=record["CreatedDate"],
            last_updated_at=record["LastModifiedDate"],
            opportunity_name=record["Opportunity__r"][
                "Opportunity_Name_Short__c"
            ],
            stage=record["Opportunity__r"]["StageName"],
            billing_country=record["Project_Account__r"]["BillingCountryCode"],
            lead_source=record["Opportunity__r"]["LeadSource"],
            project_code=record["FRM_MSProjectCode__c"],
            project_id=record.get("Id", ""),
            project_name=record["Name"],
            project_start_date=record["Start_Date__c"],
            controller_email=record["Operation_Coordinator__r"][
                "Controller__c"
            ],
            controller_sub_email=record["Operation_Coordinator_Sub__r"][
                "Controller_SUB__c"
            ],
            profit_center=record["Profit_Center__c"],
            cost_center=record["Cost_Center__c"],
            project_tier=record["Opportunity__r"]["Tier_Short__c"],
            jira_task_url=record["Opportunity__r"]["JiraComponentURL__c"],
            opportunity_percentage=record["Opportunity__r"]["Probability"],
        )
