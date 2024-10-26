from __future__ import annotations

import io
import pathlib
from contextlib import redirect_stdout
from typing import TYPE_CHECKING, Any, Dict, List, Optional, cast
from unittest import mock

import altair as alt
import nbconvert
import nbformat
import pandas as pd
import pytest
from freezegun import freeze_time

from great_expectations.core import ExpectationSuite
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core.domain import Domain, SemanticDomainTypes
from great_expectations.core.metric_domain_types import MetricDomainTypes
from great_expectations.core.usage_statistics.events import UsageStatsEvents
from great_expectations.data_context.util import file_relative_path
from great_expectations.rule_based_profiler.altair import AltairDataTypes
from great_expectations.rule_based_profiler.data_assistant_result import (
    DataAssistantResult,
    OnboardingDataAssistantResult,
)
from great_expectations.rule_based_profiler.data_assistant_result.plot_result import (
    PlotResult,
)
from great_expectations.rule_based_profiler.helpers.simple_semantic_type_filter import (
    SimpleSemanticTypeFilter,
)
from great_expectations.rule_based_profiler.helpers.util import get_batch_ids
from great_expectations.rule_based_profiler.parameter_container import (
    FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY,
    ParameterNode,
)
from great_expectations.validator.metric_configuration import MetricConfiguration
from tests.render.util import load_notebook_from_path
from tests.test_utils import find_strings_in_nested_obj, load_data_into_test_database

if TYPE_CHECKING:
    from great_expectations.data_context import FileDataContext


@pytest.fixture
def bobby_onboarding_data_assistant_result_usage_stats_enabled(
    bobby_columnar_table_multi_batch_deterministic_data_context,
) -> OnboardingDataAssistantResult:
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
    )

    return cast(OnboardingDataAssistantResult, data_assistant_result)


@pytest.fixture(scope="module")
def bobby_onboarding_data_assistant_result(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
) -> OnboardingDataAssistantResult:
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
    )

    return cast(OnboardingDataAssistantResult, data_assistant_result)


@pytest.fixture(scope="module")
def quentin_implicit_invocation_result_actual_time(
    quentin_columnar_table_multi_batch_data_context,
) -> OnboardingDataAssistantResult:
    context: FileDataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
    )

    return cast(OnboardingDataAssistantResult, data_assistant_result)


@pytest.fixture(scope="module")
@freeze_time("09/26/2019 13:42:41")
def quentin_implicit_invocation_result_frozen_time(
    quentin_columnar_table_multi_batch_data_context,
):
    context: FileDataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
    )

    return cast(OnboardingDataAssistantResult, data_assistant_result)


def run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
    context: FileDataContext,
    new_cell: str,
    implicit: bool,
):
    """
    To set this test up we:
    - create a suite
    - write code (as a string) for creating an OnboardingDataAssistantResult
    - add a new cell to the notebook that was passed to this method
    - write both cells to ipynb file

    We then:
    - load the notebook back from disk
    - execute the notebook (Note: this will raise various errors like
      CellExecutionError if any cell in the notebook fails)
    """
    root_dir: str = context.root_directory

    expectation_suite_name: str = "test_suite"
    context.add_or_update_expectation_suite(
        expectation_suite_name=expectation_suite_name
    )

    notebook_path = pathlib.Path(root_dir, "run_onboarding_data_assistant.ipynb")

    notebook_code_initialization: str = """
    from typing import Optional, Union

    import uuid

    import great_expectations as gx
    from great_expectations.data_context import AbstractDataContext
    from great_expectations.validator.validator import Validator
    from great_expectations.rule_based_profiler.data_assistant import (
        DataAssistant,
        OnboardingDataAssistant,
    )
    from great_expectations.rule_based_profiler.data_assistant_result import DataAssistantResult
    from great_expectations.rule_based_profiler.helpers.util import get_validator_with_expectation_suite
    import great_expectations.exceptions as gx_exceptions

    context = gx.get_context()

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    """

    explicit_instantiation_code: str = """
    validator: Validator = get_validator_with_expectation_suite(
        data_context=context,
        batch_list=None,
        batch_request=batch_request,
        expectation_suite_name=None,
        expectation_suite=None,
        component_name="onboarding_data_assistant",
        persist=False,
    )

    data_assistant: DataAssistant = OnboardingDataAssistant(
        name="test_onboarding_data_assistant",
        validator=validator,
    )

    data_assistant_result: DataAssistantResult = data_assistant.run()
    """

    implicit_invocation_code: str = """
    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(batch_request=batch_request)
    """

    notebook_code: str
    if implicit:
        notebook_code = notebook_code_initialization + implicit_invocation_code
    else:
        notebook_code = notebook_code_initialization + explicit_instantiation_code

    nb = nbformat.v4.new_notebook()
    nb["cells"] = []
    nb["cells"].append(nbformat.v4.new_code_cell(notebook_code))
    nb["cells"].append(nbformat.v4.new_code_cell(new_cell))

    # Write notebook to path and load it as NotebookNode
    with open(notebook_path, "w") as f:
        nbformat.write(nb, f)

    nb: nbformat.notebooknode.NotebookNode = load_notebook_from_path(
        notebook_path=notebook_path
    )

    # Run notebook
    ep: nbconvert.preprocessors.ExecutePreprocessor = (
        nbconvert.preprocessors.ExecutePreprocessor(timeout=180, kernel_name="python3")
    )
    ep.preprocess(nb, {"metadata": {"path": root_dir}})


@pytest.mark.big
@pytest.mark.slow  # 6.90s
def test_onboarding_data_assistant_result_serialization(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    onboarding_data_assistant_result_as_dict: dict = (
        bobby_onboarding_data_assistant_result.to_dict()
    )
    assert (
        set(onboarding_data_assistant_result_as_dict.keys())
        == DataAssistantResult.ALLOWED_KEYS
    )
    assert (
        bobby_onboarding_data_assistant_result.to_json_dict()
        == onboarding_data_assistant_result_as_dict
    )
    assert len(bobby_onboarding_data_assistant_result.profiler_config.rules) == 8


@pytest.mark.big
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
@pytest.mark.slow  # 7.34s
def test_onboarding_data_assistant_result_get_expectation_suite(
    mock_emit,
    bobby_onboarding_data_assistant_result_usage_stats_enabled: OnboardingDataAssistantResult,
):
    expectation_suite_name: str = "my_suite"

    suite: ExpectationSuite = bobby_onboarding_data_assistant_result_usage_stats_enabled.get_expectation_suite(
        expectation_suite_name=expectation_suite_name
    )

    assert suite is not None and len(suite.expectations) > 0

    assert mock_emit.call_count == 1

    # noinspection PyUnresolvedReferences
    actual_events: List[mock._Call] = mock_emit.call_args_list
    assert (
        actual_events[-1][0][0]["event"]
        == UsageStatsEvents.DATA_ASSISTANT_RESULT_GET_EXPECTATION_SUITE
    )


@pytest.mark.big
def test_onboarding_data_assistant_metrics_count(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    domain: Domain
    parameter_values_for_fully_qualified_parameter_names: Dict[str, ParameterNode]
    num_metrics: int

    domain_key = Domain(
        domain_type=MetricDomainTypes.TABLE,
    )

    num_metrics = 0
    for (
        domain,
        parameter_values_for_fully_qualified_parameter_names,
    ) in bobby_onboarding_data_assistant_result.metrics_by_domain.items():
        if domain.is_superset(other=domain_key):
            num_metrics += len(parameter_values_for_fully_qualified_parameter_names)

    assert num_metrics == 4

    num_metrics = 0
    for (
        domain,
        parameter_values_for_fully_qualified_parameter_names,
    ) in bobby_onboarding_data_assistant_result.metrics_by_domain.items():
        num_metrics += len(parameter_values_for_fully_qualified_parameter_names)

    assert num_metrics == 300


@pytest.mark.big
def test_onboarding_data_assistant_result_batch_id_to_batch_identifier_display_name_map_coverage(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
):
    metrics_by_domain: Optional[
        Dict[Domain, Dict[str, ParameterNode]]
    ] = bobby_onboarding_data_assistant_result.metrics_by_domain

    parameter_values_for_fully_qualified_parameter_names: Dict[str, ParameterNode]
    parameter_node: ParameterNode
    batch_id: str
    assert all(
        bobby_onboarding_data_assistant_result._batch_id_to_batch_identifier_display_name_map[
            batch_id
        ]
        is not None
        for parameter_values_for_fully_qualified_parameter_names in metrics_by_domain.values()
        for parameter_node in parameter_values_for_fully_qualified_parameter_names.values()
        for batch_id in (
            parameter_node[FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY]
            if FULLY_QUALIFIED_PARAMETER_NAME_ATTRIBUTED_VALUE_KEY in parameter_node
            else {}
        ).keys()
    )


@pytest.mark.unit
def test_onboarding_data_assistant_should_fail_forward(
    ephemeral_context_with_defaults,
    rule_state_with_domains_and_parameters,
):
    """When one rule fails, the rest of the rules should still be executed."""
    context = ephemeral_context_with_defaults
    datasource = context.sources.add_or_update_pandas("my_datasource")
    asset = datasource.add_dataframe_asset("my_asset")
    # noinspection PyTypeChecker
    df = pd.DataFrame(
        {
            "non-null": [i for i in range(100)],
            "null": [None for _ in range(100)],
            "low-null": [None for _ in range(38)] + [i for i in range(62)],
        }
    )
    batch_request = asset.build_batch_request(dataframe=df)

    num_rules = 8  # There are 8 rules in the onboarding data assistant.
    with mock.patch(
        "great_expectations.rule_based_profiler.rule.rule.Rule.run",
    ) as mock_run:
        # Set first rule to fail and the rest to pass.
        call_count = 0

        def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ValueError("This rule failed.")
            return rule_state_with_domains_and_parameters

        mock_run.side_effect = side_effect

        data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
            batch_request=batch_request,
            estimation="flag_outliers",
            numeric_columns_rule={
                "round_decimals": 15,
                "false_positive_rate": 0.1,
                "random_seed": 43792,
            },
            datetime_columns_rule={
                "truncate_values": {
                    "lower_bound": 0,
                    "upper_bound": 4481049600,  # Friday, January 1, 2112 0:00:00
                },
                "round_decimals": 0,
            },
            text_columns_rule={
                "strict_min": True,
                "strict_max": True,
                "success_ratio": 0.8,
            },
            categorical_columns_rule={
                "false_positive_rate": 0.1,
                # "round_decimals": 4,
            },
        )
        # Although the first rule fails, the rest of the rules should still be executed.
        assert mock_run.call_count == num_rules
        assert call_count == num_rules

        result = data_assistant_result.to_json_dict()
        assert result["rule_exception_tracebacks"]
        assert (
            result["rule_exception_tracebacks"]["table_rule"]["exception_message"]
            == "This rule failed."
        )


@pytest.mark.spark
def test_onboarding_data_assistant_numeric_column_containing_dot_spark(
    spark_session,
    ephemeral_context_with_defaults,
):
    """What does this test and why?

    Spark identifiers are less restrictive than ANSI SQL identifiers. This test ensures that we can use identifiers
    compliant with: https://spark.apache.org/docs/latest/sql-ref-identifier.html, specifically the dot case e.g. `a.b`.
    """

    columns = ["snake_case", "kebab-case", "dot.case"]
    values = [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4), (5, 5, 5)]

    df = spark_session.createDataFrame(data=values, schema=columns)

    context = ephemeral_context_with_defaults
    datasource = context.sources.add_or_update_spark("my_datasource")
    asset = datasource.add_dataframe_asset("my_asset")
    batch_request = asset.build_batch_request(dataframe=df)

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request, exclude_column_names=["snake_case", "kebab-case"]
    )

    # Histogram metric cannot be computed when using columns containing `.` with the current metric implementation.
    # Other metrics should pass.
    assert list(data_assistant_result.rule_exception_tracebacks.keys()) == [
        "numeric_columns_rule"
    ]
    assert (
        data_assistant_result.rule_exception_tracebacks["numeric_columns_rule"][
            "exception_message"
        ]
        == "Column names cannot contain '.' when computing the histogram metric."
    )


@pytest.mark.big
@pytest.mark.slow  # 39.26s
def test_onboarding_data_assistant_get_metrics_and_expectations_using_implicit_invocation_with_variables_directives(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
        numeric_columns_rule={
            "round_decimals": 15,
            "false_positive_rate": 0.1,
            "random_seed": 43792,
        },
        datetime_columns_rule={
            "truncate_values": {
                "lower_bound": 0,
                "upper_bound": 4481049600,  # Friday, January 1, 2112 0:00:00
            },
            "round_decimals": 0,
        },
        text_columns_rule={
            "strict_min": True,
            "strict_max": True,
            "success_ratio": 0.8,
        },
        categorical_columns_rule={
            "false_positive_rate": 0.1,
            # "round_decimals": 4,
        },
    )
    assert (
        data_assistant_result.profiler_config.rules["numeric_columns_rule"][
            "variables"
        ]["round_decimals"]
        == 15
    )
    assert (
        data_assistant_result.profiler_config.rules["numeric_columns_rule"][
            "variables"
        ]["false_positive_rate"]
        == 1.0e-1
    )
    assert data_assistant_result.profiler_config.rules["datetime_columns_rule"][
        "variables"
    ]["truncate_values"] == {
        "lower_bound": 0,
        "upper_bound": 4481049600,  # Friday, January 1, 2112 0:00:00
    }
    assert (
        data_assistant_result.profiler_config.rules["datetime_columns_rule"][
            "variables"
        ]["round_decimals"]
        == 0
    )
    assert data_assistant_result.profiler_config.rules["text_columns_rule"][
        "variables"
    ]["strict_min"]
    assert data_assistant_result.profiler_config.rules["text_columns_rule"][
        "variables"
    ]["strict_max"]
    assert (
        data_assistant_result.profiler_config.rules["text_columns_rule"]["variables"][
            "success_ratio"
        ]
        == 8.0e-1
    )
    assert (
        data_assistant_result.profiler_config.rules["categorical_columns_rule"][
            "variables"
        ]["false_positive_rate"]
        == 1.0e-1
    )


@pytest.mark.big
@pytest.mark.slow  # 38.26s
def test_onboarding_data_assistant_get_metrics_and_expectations_using_implicit_invocation_with_estimation_directive(
    quentin_columnar_table_multi_batch_data_context,
):
    context: FileDataContext = quentin_columnar_table_multi_batch_data_context

    batch_request: dict = {
        "datasource_name": "taxi_pandas",
        "data_connector_name": "monthly",
        "data_asset_name": "my_reports",
    }

    data_assistant_result: DataAssistantResult = context.assistants.onboarding.run(
        batch_request=batch_request,
    )

    rule_config: dict
    assert all(
        rule_config["variables"]["estimator"] == "exact"
        if "estimator" in rule_config["variables"]
        else True
        for rule_config in data_assistant_result.profiler_config.rules.values()
    )


@pytest.mark.big
@pytest.mark.slow  # 25.61s
def test_onboarding_data_assistant_plot_descriptive_notebook_execution_fails(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    new_cell: str = (
        "data_assistant_result.plot_metrics(this_is_not_a_real_parameter=True)"
    )

    with pytest.raises(nbconvert.preprocessors.CellExecutionError):
        run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
            context=context,
            new_cell=new_cell,
            implicit=False,
        )

    with pytest.raises(nbconvert.preprocessors.CellExecutionError):
        run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
            context=context,
            new_cell=new_cell,
            implicit=True,
        )


@pytest.mark.big
@pytest.mark.slow  # 28.73s
def test_onboarding_data_assistant_plot_descriptive_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    new_cell: str = "data_assistant_result.plot_metrics()"

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
@pytest.mark.slow  # 36.23s
def test_onboarding_data_assistant_plot_prescriptive_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    new_cell: str = "data_assistant_result.plot_expectations_and_metrics()"

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
@pytest.mark.slow  # 27.95s
def test_onboarding_data_assistant_plot_descriptive_theme_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    theme = {"font": "Comic Sans MS"}

    new_cell: str = f"data_assistant_result.plot_metrics(theme={theme})"

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
@pytest.mark.slow  # 35.34s
def test_onboarding_data_assistant_plot_prescriptive_theme_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    theme = {"font": "Comic Sans MS"}

    new_cell: str = (
        f"data_assistant_result.plot_expectations_and_metrics(theme={theme})"
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
@pytest.mark.slow  # 2.02s
def test_onboarding_data_assistant_plot_returns_proper_dict_repr_of_table_domain_chart(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    plot_result: PlotResult = bobby_onboarding_data_assistant_result.plot_metrics()

    table_domain_chart: dict = plot_result.charts[0].to_dict()
    assert find_strings_in_nested_obj(table_domain_chart, ["Table Row Count per Batch"])


@pytest.mark.big
@pytest.mark.slow  # 3.42s
def test_onboarding_data_assistant_plot_returns_proper_dict_repr_of_column_domain_chart(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    plot_result: PlotResult = bobby_onboarding_data_assistant_result.plot_metrics()

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 100

    columns: List[str] = [
        "VendorID",
        "passenger_count",
        "RatecodeID",
        "store_and_fwd_flag",
        "payment_type",
        "extra",
        "mta_tax",
        "tolls_amount",
        "improvement_surcharge",
        "congestion_surcharge",
    ]
    assert find_strings_in_nested_obj(column_domain_charts, columns)


@pytest.mark.big
def test_onboarding_data_assistant_plot_metrics_include_column_names_filters_output(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    include_column_names: List[str] = ["passenger_count", "trip_distance"]
    plot_result: PlotResult = bobby_onboarding_data_assistant_result.plot_metrics(
        include_column_names=include_column_names
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 13
    assert find_strings_in_nested_obj(column_domain_charts, include_column_names)


@pytest.mark.big
@pytest.mark.slow  # 2.74s
def test_onboarding_data_assistant_plot_metrics_exclude_column_names_filters_output(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    exclude_column_names: List[str] = ["VendorID", "passenger_count"]
    plot_result: PlotResult = bobby_onboarding_data_assistant_result.plot_metrics(
        exclude_column_names=exclude_column_names,
        sequential=False,
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 86
    assert not find_strings_in_nested_obj(column_domain_charts, exclude_column_names)


@pytest.mark.big
@pytest.mark.slow  # 1.67s
def test_onboarding_data_assistant_plot_expectations_and_metrics_include_column_names_filters_output(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    include_column_names: List[str] = ["passenger_count", "trip_distance"]
    plot_result: PlotResult = (
        bobby_onboarding_data_assistant_result.plot_expectations_and_metrics(
            include_column_names=include_column_names
        )
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 15
    assert find_strings_in_nested_obj(column_domain_charts, include_column_names)


@pytest.mark.big
@pytest.mark.slow  # 8.26s
def test_onboarding_data_assistant_plot_expectations_and_metrics_exclude_column_names_filters_output(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    exclude_column_names: List[str] = ["VendorID", "passenger_count"]
    plot_result: PlotResult = (
        bobby_onboarding_data_assistant_result.plot_expectations_and_metrics(
            exclude_column_names=exclude_column_names
        )
    )

    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 99
    assert not find_strings_in_nested_obj(column_domain_charts, exclude_column_names)


@pytest.mark.big
def test_onboarding_data_assistant_plot_include_and_exclude_column_names_raises_error(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    with pytest.raises(ValueError) as e:
        bobby_onboarding_data_assistant_result.plot_metrics(
            include_column_names=["VendorID"], exclude_column_names=["pickup_datetime"]
        )

    assert "either use `include_column_names` or `exclude_column_names`" in str(e.value)


@pytest.mark.unit
def test_onboarding_data_assistant_result_plot_expectations_and_metrics_correctly_handle_empty_plot_data() -> (
    None
):
    data_assistant_result: DataAssistantResult = OnboardingDataAssistantResult()

    include_column_names: List[str] = [
        "congestion_surcharge",
    ]
    plot_result: PlotResult = data_assistant_result.plot_expectations_and_metrics(
        include_column_names=include_column_names
    )

    # This test passes only if absense of any metrics and expectations to plot does not cause exceptions to be raised.
    column_domain_charts: List[dict] = [p.to_dict() for p in plot_result.charts[2:]]
    assert len(column_domain_charts) == 0


@pytest.mark.big
@pytest.mark.slow  # 5.63s
def test_onboarding_data_assistant_plot_custom_theme_overrides(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    font: str = "Comic Sans MS"
    title_color: str = "#FFA500"
    title_font_size: int = 48
    point_size: int = 1000
    y_axis_label_color: str = "red"
    y_axis_label_angle: int = 180
    x_axis_title_color: str = "brown"

    theme: Dict[str, Any] = {
        "font": font,
        "title": {
            "color": title_color,
            "fontSize": title_font_size,
        },
        "point": {"size": point_size},
        "axisY": {
            "labelColor": y_axis_label_color,
            "labelAngle": y_axis_label_angle,
        },
        "axisX": {"titleColor": x_axis_title_color},
    }
    plot_result: PlotResult = (
        bobby_onboarding_data_assistant_result.plot_expectations_and_metrics(
            theme=theme
        )
    )

    # ensure a config has been added to each chart
    assert all(
        not isinstance(chart.config, alt.utils.schemapi.UndefinedType)
        for chart in plot_result.charts
    )

    # ensure the theme elements were updated for each chart
    assert all(chart.config.font == font for chart in plot_result.charts)
    assert all(
        chart.config.title["color"] == title_color for chart in plot_result.charts
    )
    assert all(
        chart.config.title["fontSize"] == title_font_size
        for chart in plot_result.charts
    )
    assert all(chart.config.point["size"] == point_size for chart in plot_result.charts)
    assert all(
        chart.config.axisY["labelColor"] == y_axis_label_color
        for chart in plot_result.charts
    )
    assert all(
        chart.config.axisY["labelAngle"] == y_axis_label_angle
        for chart in plot_result.charts
    )
    assert all(
        chart.config.axisX["titleColor"] == x_axis_title_color
        for chart in plot_result.charts
    )


@pytest.mark.big
@pytest.mark.slow  # 5.61s
def test_onboarding_data_assistant_plot_return_tooltip(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
) -> None:
    plot_result: PlotResult = (
        bobby_onboarding_data_assistant_result.plot_expectations_and_metrics()
    )

    expected_tooltip: List[alt.Tooltip] = [
        alt.Tooltip(
            **{
                "field": "column",
                "format": "",
                "title": "Column",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "month",
                "format": "",
                "title": "Month",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "name",
                "format": "",
                "title": "Name",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "year",
                "format": "",
                "title": "Year",
                "type": AltairDataTypes.ORDINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "min_value",
                "format": "",
                "title": "Min Value",
                "type": AltairDataTypes.QUANTITATIVE.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "max_value",
                "format": "",
                "title": "Max Value",
                "type": AltairDataTypes.QUANTITATIVE.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "strict_min",
                "format": "",
                "title": "Strict Min",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
        alt.Tooltip(
            **{
                "field": "strict_max",
                "format": "",
                "title": "Strict Max",
                "type": AltairDataTypes.NOMINAL.value,
            }
        ),
    ]

    for chart in plot_result.charts:
        chart_title: str = DataAssistantResult._get_chart_layer_title(layer=chart)
        if chart_title == "expect_column_min_to_be_between":
            single_column_return_chart: alt.LayerChart = chart
    layer_1: alt.Chart = single_column_return_chart.layer[1]
    actual_tooltip: List[alt.Tooltip] = layer_1.encoding.tooltip

    for tooltip in expected_tooltip:
        assert tooltip in actual_tooltip


@pytest.mark.big
@pytest.mark.slow  # 27.11s
def test_onboarding_data_assistant_metrics_plot_descriptive_non_sequential_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    new_cell: str = "data_assistant_result.plot_metrics(sequential=False)"

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
@pytest.mark.slow  # 34.85s
def test_onboarding_data_assistant_metrics_and_expectations_plot_descriptive_non_sequential_notebook_execution(
    bobby_columnar_table_multi_batch_probabilistic_data_context,
):
    context: FileDataContext = (
        bobby_columnar_table_multi_batch_probabilistic_data_context
    )

    new_cell: str = (
        "data_assistant_result.plot_expectations_and_metrics(sequential=False)"
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=False,
    )

    run_onboarding_data_assistant_result_jupyter_notebook_with_new_cell(
        context=context,
        new_cell=new_cell,
        implicit=True,
    )


@pytest.mark.big
def test_onboarding_data_assistant_result_empty_suite_plot_metrics_and_expectations(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
):
    data_assistant_result: OnboardingDataAssistantResult = (
        bobby_onboarding_data_assistant_result
    )
    data_assistant_result.expectation_configurations = []

    try:
        data_assistant_result.plot_expectations_and_metrics()
    except Exception as exc:
        assert (
            False
        ), f"DataAssistantResult.plot_expectations_and_metrics raised an exception '{exc}'"


@pytest.mark.big
def test_onboarding_data_assistant_plot_metrics_stdout(
    bobby_onboarding_data_assistant_result: OnboardingDataAssistantResult,
):
    data_assistant_result: OnboardingDataAssistantResult = (
        bobby_onboarding_data_assistant_result
    )

    metrics_calculated = 300
    metrics_plots_implemented = 102

    f = io.StringIO()
    with redirect_stdout(f):
        data_assistant_result.plot_metrics()
    stdout = f.getvalue()
    assert (
        f"""{metrics_calculated} Metrics calculated, {metrics_plots_implemented} Metric plots implemented
Use DataAssistantResult.metrics_by_domain to show all calculated Metrics"""
        in stdout
    )


@pytest.mark.trino
@pytest.mark.parametrize("use_fds", [True, False])
def test_onboarding_data_assistant__trino_with_string_fields(
    empty_data_context, use_fds
):
    CONNECTION_STRING = "trino://test@localhost:8088/memory/schema"

    # This utility is not for general use. It is only to support testing.
    load_data_into_test_database(
        table_name="taxi_data",
        csv_path=file_relative_path(
            __file__,
            "../../test_sets/taxi_yellow_tripdata_samples/yellow_tripdata_sample_2019-01.csv",
        ),
        connection_string=CONNECTION_STRING,
        convert_colnames_to_datetime=["pickup_datetime"],
    )

    context = empty_data_context
    if not use_fds:
        datasource_config = {
            "name": "my_trino_datasource",
            "class_name": "Datasource",
            "execution_engine": {
                "class_name": "SqlAlchemyExecutionEngine",
                "connection_string": CONNECTION_STRING,
            },
            "data_connectors": {
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "batch_identifiers": ["default_identifier_name"],
                },
                "default_inferred_data_connector_name": {
                    "class_name": "InferredAssetSqlDataConnector",
                    "include_schema_name": True,
                },
            },
        }

        context.add_datasource(**datasource_config)
        batch_request = RuntimeBatchRequest(
            datasource_name="my_trino_datasource",
            data_connector_name="default_runtime_data_connector_name",
            data_asset_name="default_name",  # this can be anything that identifies this data
            runtime_parameters={
                "query": "SELECT pickup_datetime, dropoff_datetime, store_and_fwd_flag from taxi_data LIMIT 10"
            },
            batch_identifiers={"default_identifier_name": "default_identifier"},
        )
    else:
        datasource = context.sources.add_sql(
            name="my_trino_datasource", connection_string=CONNECTION_STRING
        )
        asset = datasource.add_table_asset(name="taxi_data")
        batch_request = asset.build_batch_request()

    context.add_or_update_expectation_suite(expectation_suite_name="test_suite")
    validator = context.get_validator(
        batch_request=batch_request, expectation_suite_name="test_suite"
    )

    desired_metric = MetricConfiguration(
        metric_name="table.column_types",
        metric_domain_kwargs={},
        metric_value_kwargs=None,
    )
    validator.execution_engine.resolve_metrics([desired_metric])

    if not use_fds:
        batch_ids = get_batch_ids(data_context=context, batch_request=batch_request)
        # Ensure that the data types are read correctly
        semantic_type_filter = SimpleSemanticTypeFilter(
            validator=validator,
            batch_ids=batch_ids,
            column_names=["pickup_datetime", "dropoff_datetime", "store_and_fwd_flag"],
        )
        assert (
            semantic_type_filter.table_column_name_to_inferred_semantic_domain_type_map
            == {
                "pickup_datetime": SemanticDomainTypes.DATETIME,
                "dropoff_datetime": SemanticDomainTypes.TEXT,
                "store_and_fwd_flag": SemanticDomainTypes.TEXT,
            }
        )

    # Attempt to run the onboarding assistant
    result = context.assistants.onboarding.run(
        batch_request=batch_request,
        estimation="flag_outliers",
        include_column_names=[
            "pickup_datetime",
            "dropoff_datetime",
            "store_and_fwd_flag",
        ],
    )

    assert result
    assert len(result.expectation_configurations) > 0

    # Should have some expectations for all three columns
    assert any(
        x["kwargs"].get("column") == "pickup_datetime"
        for x in result.expectation_configurations
    )
    assert any(
        x["kwargs"].get("column") == "dropoff_datetime"
        for x in result.expectation_configurations
    )
    assert any(
        x["kwargs"].get("column") == "store_and_fwd_flag"
        for x in result.expectation_configurations
    )
