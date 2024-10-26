from __future__ import annotations

import logging
import os
import pathlib
import re
from typing import TYPE_CHECKING, cast

import boto3
import botocore
import pytest

from great_expectations.core.util import DBFSPath
from great_expectations.datasource.fluent import SparkDBFSDatasource
from great_expectations.datasource.fluent.data_asset.data_connector import (
    DBFSDataConnector,
)
from great_expectations.datasource.fluent.file_path_data_asset import (
    _FilePathDataAsset,
)
from great_expectations.datasource.fluent.interfaces import TestConnectionError
from great_expectations.datasource.fluent.spark_file_path_datasource import (
    CSVAsset,
)
from tests.test_utils import create_files_in_directory

if TYPE_CHECKING:
    from pyfakefs.fake_filesystem import FakeFilesystem


logger = logging.getLogger(__file__)


@pytest.fixture
def spark_dbfs_datasource(fs: FakeFilesystem, test_backends) -> SparkDBFSDatasource:
    if "SparkDFDataset" not in test_backends:
        pytest.skip("No spark backend selected.")

    # Copy boto modules into fake filesystem (see https://github.com/spulec/moto/issues/1682#issuecomment-645016188)
    for module in [boto3, botocore]:
        module_dir = pathlib.Path(module.__file__).parent
        fs.add_real_directory(module_dir, lazy_read=False)

    # Copy google credentials into fake filesystem if they exist on your filesystem
    google_cred_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if google_cred_file:
        fs.add_real_file(google_cred_file)

    base_directory: str = "/dbfs/great_expectations"
    fs.create_dir(base_directory)

    create_files_in_directory(
        directory=base_directory,
        file_name_list=[
            "alex_20200809_1000.csv",
            "eugene_20200809_1500.csv",
            "james_20200811_1009.csv",
            "abe_20200809_1040.csv",
            "will_20200809_1002.csv",
            "james_20200713_1567.csv",
            "eugene_20201129_1900.csv",
            "will_20200810_1001.csv",
            "james_20200810_1003.csv",
            "alex_20200819_1300.csv",
        ],
    )

    return SparkDBFSDatasource(
        name="spark_dbfs_datasource",
        base_directory=pathlib.Path(base_directory),
    )


@pytest.fixture
def csv_asset(spark_dbfs_datasource: SparkDBFSDatasource) -> _FilePathDataAsset:
    asset = spark_dbfs_datasource.add_csv_asset(
        name="csv_asset",
        batching_regex=r"(?P<name>.+)_(?P<timestamp>.+)_(?P<price>\d{4})\.csv",
    )
    return asset


@pytest.fixture
def bad_regex_config(csv_asset: CSVAsset) -> tuple[re.Pattern, str]:
    regex = re.compile(
        r"(?P<name>.+)_(?P<ssn>\d{9})_(?P<timestamp>.+)_(?P<price>\d{4})\.csv"
    )
    data_connector: DBFSDataConnector = cast(
        DBFSDataConnector, csv_asset._data_connector
    )
    test_connection_error_message = f"""No file at base_directory path "{data_connector._base_directory.resolve()}" matched regular expressions pattern "{data_connector._batching_regex.pattern}" and/or glob_directive "**/*" for DataAsset "csv_asset"."""
    return regex, test_connection_error_message


@pytest.mark.spark
def test_construct_spark_dbfs_datasource(spark_dbfs_datasource: SparkDBFSDatasource):
    assert spark_dbfs_datasource.name == "spark_dbfs_datasource"


@pytest.mark.spark
def test_add_csv_asset_to_datasource(spark_dbfs_datasource: SparkDBFSDatasource):
    asset_specified_metadata = {"asset_level_metadata": "my_metadata"}
    asset = spark_dbfs_datasource.add_csv_asset(
        name="csv_asset",
        batching_regex=r"(.+)_(.+)_(\d{4})\.csv",
        batch_metadata=asset_specified_metadata,
    )
    assert asset.name == "csv_asset"
    assert asset.batching_regex.match("random string") is None
    assert asset.batching_regex.match("alex_20200819_13D0.csv") is None
    m1 = asset.batching_regex.match("alex_20200819_1300.csv")
    assert m1 is not None
    assert asset.batch_metadata == asset_specified_metadata


@pytest.mark.unit
def test_construct_csv_asset_directly():
    # noinspection PyTypeChecker
    asset = CSVAsset(
        name="csv_asset",
        batching_regex=r"(.+)_(.+)_(\d{4})\.csv",
    )
    assert asset.name == "csv_asset"
    assert asset.batching_regex.match("random string") is None
    assert asset.batching_regex.match("alex_20200819_13D0.csv") is None
    m1 = asset.batching_regex.match("alex_20200819_1300.csv")
    assert m1 is not None


@pytest.mark.spark
@pytest.mark.xfail(
    reason="Accessing objects on pyfakefs.fake_filesystem.FakeFilesystem using Spark is not working (this test is conducted using Jupyter notebook manually)."
)
def test_get_batch_list_from_fully_specified_batch_request(
    spark_dbfs_datasource: SparkDBFSDatasource,
):
    asset_specified_metadata = {"asset_level_metadata": "my_metadata"}
    asset = spark_dbfs_datasource.add_csv_asset(
        name="csv_asset",
        batching_regex=r"(?P<name>.+)_(?P<timestamp>.+)_(?P<price>\d{4})\.csv",
        batch_metadata=asset_specified_metadata,
    )

    request = asset.build_batch_request(
        {"name": "alex", "timestamp": "20200819", "price": "1300"}
    )
    batches = asset.get_batch_list_from_batch_request(request)
    assert len(batches) == 1
    batch = batches[0]
    assert batch.batch_request.datasource_name == spark_dbfs_datasource.name
    assert batch.batch_request.data_asset_name == asset.name
    assert batch.batch_request.options == (
        "name",
        "timestamp",
        "price",
        "path",
    )
    assert batch.metadata == {
        "path": "alex_20200819_1300.csv",
        "name": "alex",
        "timestamp": "20200819",
        "price": "1300",
        **asset_specified_metadata,
    }
    assert (
        batch.id
        == "spark_dbfs_datasource-csv_asset-name_alex-timestamp_20200819-price_1300"
    )

    request = asset.build_batch_request({"name": "alex"})
    batches = asset.get_batch_list_from_batch_request(request)
    assert len(batches) == 2


@pytest.mark.spark
def test_test_connection_failures(
    spark_dbfs_datasource: SparkDBFSDatasource,
    bad_regex_config: tuple[re.Pattern, str],
):
    regex, test_connection_error_message = bad_regex_config
    csv_asset = CSVAsset(  # type: ignore[call-arg] # missing args
        name="csv_asset",
        batching_regex=regex,
    )
    csv_asset._datasource = spark_dbfs_datasource
    spark_dbfs_datasource.assets = [
        csv_asset,
    ]
    csv_asset._data_connector = DBFSDataConnector(
        datasource_name=spark_dbfs_datasource.name,
        data_asset_name=csv_asset.name,
        batching_regex=re.compile(regex),
        base_directory=spark_dbfs_datasource.base_directory,
        data_context_root_directory=spark_dbfs_datasource.data_context_root_directory,
        glob_directive="*.csv",
        file_path_template_map_fn=DBFSPath.convert_to_protocol_version,
    )
    csv_asset._test_connection_error_message = test_connection_error_message

    with pytest.raises(TestConnectionError) as e:
        spark_dbfs_datasource.test_connection()

    assert str(e.value) == str(test_connection_error_message)
