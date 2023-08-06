# How to contribute
After clone repository

## 1.- Install dependencies
```bash
poetry install
```

## 2.- Run test
```bash
make test
```

## 3.- Run lint
```bash
make lint && make isort
```

## How to publish new version
Once we have done a merge of our Pull request and we have the updated master branch we can generate a new version. For them we have 3 commands that change the version of our library and generate the corresponding tag so that the Bitbucket pipeline starts and publishes our library automatically.

```bash
make release-patch
```

```bash
make release-minor
```

```bash
make release-major
```

# How works
This project provides an API for querying Salesforce opportunities data and transforming it into an easy-to-use format. The API is built upon the `SalesforceQueryExecutor` and `Project` classes, with the latter inheriting from `SalesforceQueryExecutor`.

## Installation

Make sure you have **Python 3.8+** installed. Then, install the required dependencies using `poetry`:

```bash
poetry install
```

## Usage

First, import the necessary classes:

```python
from ms_salesforce_to_bigquery.salesforce.project import Project
```

Then, initialize the `Project` class with your Salesforce credentials:

```python
project = Project(
    client_id="your_client_id",
    username="your_username",
    domain="your_domain",
    private_key="your_private_key",
    audience="https://login.salesforce.com", # Default value
    session_duration_hours=1, # Default value
    api_version='57.0',  # Default value
)
```

Now, you can call the get_opportunities method with a query to get the opportunities data:

```python
opportunities = project.get_opportunities()
```

The opportunities variable will contain an array of opportunity objects with the transformed data. For example:

```python
[
    {
        "client_fiscal_name": "Five Eight Twenty-Two Consulting Inc.",
        "client_account_name": "5822",
        "currency": "CAD",
        "amount": 30000.0,
        "invoicing_country_code": "ES",
        "operation_coordinator_email": "jhon.doe@ext.makingscience.com",
        "operation_coordinator_sub_email": "jhon.doe@ext.makingscience.com",
        "created_at": "2023-02-15T09:30:06.000+0000",
        "last_updated_at": "2023-04-04T10:43:24.000+0000",
        "opportunity_name": "5822 - OPORTUNITY NAME",
        "stage": "Closed Won",
        "billing_country": "CA",
        "lead_source": "TEST LEAD SOURCE",
        "project_code": "ESMSEX00000",
        "project_id": "1234567890abcde",
        "project_name": "PROJECT TEST NAME",
        "project_start_date": "2023-02-01",
        "controller_email": None,
        "controller_sub_email": "jhon.doe@ext.makingscience.com",
        "profit_center": None,
        "cost_center": None,
        "project_tier": "Unkown",
        "jira_task_url": "https://makingscience.atlassian.net/browse/ESMSBD0001-00000",
        "opportunity_percentage": 100.0
    }
]
```

You can customize the query as needed to retrieve different data from Salesforce.

```python
query = "SELECT Id, Name FROM Project WHERE Project.Id = 'ESMS0000'"

opportunities = project.get_opportunities(query)
```

# Testing
To run the unit tests, simply execute the following command:

```bash
make test
```
This will run all the tests and display the results. Make sure that all tests pass before using the API in a production environment.
