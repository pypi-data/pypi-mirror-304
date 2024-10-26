import os

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py imports">
import great_expectations as gx

# </snippet>
from great_expectations.datasource.fluent.sql_datasource import SQLDatasource
from tests.test_utils import check_athena_table_count, clean_athena_db

ATHENA_DB_NAME = os.getenv("ATHENA_DB_NAME")
if not ATHENA_DB_NAME:
    raise ValueError(
        "Environment Variable ATHENA_DB_NAME is required to run integration tests against AWS Athena"
    )
ATHENA_STAGING_S3 = os.getenv("ATHENA_STAGING_S3")
if not ATHENA_STAGING_S3:
    raise ValueError(
        "Environment Variable ATHENA_STAGING_S3 is required to run integration tests against AWS Athena"
    )

connection_string = f"awsathena+rest://@athena.us-east-1.amazonaws.com/{ATHENA_DB_NAME}?s3_staging_dir={ATHENA_STAGING_S3}"

# create datasource and add to DataContext
# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py get_context">
context = gx.get_context()
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py Connect and Build Batch Request">
athena_source: SQLDatasource = context.sources.add_or_update_sql(
    "my_awsathena_datasource", connection_string=connection_string
)
athena_table = athena_source.add_table_asset("taxitable", table_name="taxitable")


batch_request = athena_table.build_batch_request()
# </snippet>

# clean db to prepare for test
clean_athena_db(connection_string, ATHENA_DB_NAME, "taxitable")

# Test 1 : temp_table is not created (default)

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py Create Expectation Suite">
expectation_suite_name = "my_awsathena_expectation_suite"
suite = context.add_or_update_expectation_suite(
    expectation_suite_name=expectation_suite_name
)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py Test Datasource with Validator">
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite_name,
)
validator.head(n_rows=5, fetch_all=False)
# </snippet>
assert validator

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py Add Checkpoint">
checkpoint = context.add_or_update_checkpoint(
    name="my_checkpoint",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": expectation_suite_name,
        },
    ],
)
# </snippet>

# <snippet name="tests/integration/docusaurus/connecting_to_your_data/database/athena_python_example.py Run Checkpoint">
checkpoint_result = checkpoint.run()
# </snippet>

# clean db
clean_athena_db(connection_string, ATHENA_DB_NAME, "taxitable")

# Check that only our original table exists
assert check_athena_table_count(connection_string, ATHENA_DB_NAME, 1)
