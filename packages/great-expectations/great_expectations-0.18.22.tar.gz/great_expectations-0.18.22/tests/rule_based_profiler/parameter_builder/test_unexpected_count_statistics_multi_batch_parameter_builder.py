from typing import List, Optional

import pytest

from great_expectations.core.metric_function_types import (
    SummarizationMetricNameSuffixes,
)
from great_expectations.data_context import AbstractDataContext
from great_expectations.rule_based_profiler.config import ParameterBuilderConfig
from great_expectations.rule_based_profiler.parameter_builder import (
    ParameterBuilder,
    UnexpectedCountStatisticsMultiBatchParameterBuilder,
)
from great_expectations.rule_based_profiler.parameter_builder.unexpected_count_statistics_multi_batch_parameter_builder import (
    _standardize_mostly_for_single_batch,
)
from great_expectations.rule_based_profiler.parameter_container import (
    DOMAIN_KWARGS_PARAMETER_FULLY_QUALIFIED_NAME,
)


@pytest.mark.big
def test_instantiation_unexpected_count_statistics_multi_batch_parameter_builder(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    data_context: AbstractDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    parameter_builder: ParameterBuilder = (  # noqa: F841
        UnexpectedCountStatisticsMultiBatchParameterBuilder(
            name="my_name",
            mode="unexpected_count_fraction_values",
            unexpected_count_parameter_builder_name="my_unexpected_count",
            total_count_parameter_builder_name="my_total_count",
            data_context=data_context,
        )
    )


@pytest.mark.big
def test_instantiation_unexpected_count_statistics_multi_batch_parameter_builder_builder_required_arguments_absent(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    data_context: AbstractDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    with pytest.raises(TypeError) as excinfo:
        parameter_builder: ParameterBuilder = (
            UnexpectedCountStatisticsMultiBatchParameterBuilder(
                name="my_name",
                data_context=data_context,
            )
        )

    assert (
        "__init__() missing 3 required positional arguments: 'unexpected_count_parameter_builder_name', 'total_count_parameter_builder_name', and 'mode'"
        in str(excinfo.value)
    )

    with pytest.raises(TypeError) as excinfo:
        # noinspection PyUnusedLocal,PyArgumentList
        parameter_builder: ParameterBuilder = (  # noqa: F841
            UnexpectedCountStatisticsMultiBatchParameterBuilder(
                name="my_name",
                unexpected_count_parameter_builder_name="my_unexpected_count",
                total_count_parameter_builder_name="my_total_count",
                data_context=data_context,
            )
        )

    assert "__init__() missing 1 required positional argument: 'mode'" in str(
        excinfo.value
    )


@pytest.mark.big
def test_unexpected_count_statistics_multi_batch_parameter_builder_bobby_check_serialized_keys_no_evaluation_parameter_builder_configs(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    data_context: AbstractDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    unexpected_count_statistics_multi_batch_parameter_builder: ParameterBuilder = (
        UnexpectedCountStatisticsMultiBatchParameterBuilder(
            name="my_passenger_count_values_not_null_unexpected_count_statistics",
            unexpected_count_parameter_builder_name="my_null_count",
            total_count_parameter_builder_name="my_total_count",
            mode="unexpected_count_fraction_values",
            evaluation_parameter_builder_configs=None,
            data_context=data_context,
        )
    )

    # Note: "evaluation_parameter_builder_configs" is not one of "ParameterBuilder" formal property attributes.
    assert set(
        unexpected_count_statistics_multi_batch_parameter_builder.to_json_dict().keys()
    ) == {
        "class_name",
        "module_name",
        "name",
        "unexpected_count_parameter_builder_name",
        "total_count_parameter_builder_name",
        "mode",
        "max_error_rate",
        "expectation_type",
        "evaluation_parameter_builder_configs",
    }


@pytest.mark.big
def test_unexpected_count_statistics_multi_batch_parameter_builder_bobby_check_serialized_keys_with_evaluation_parameter_builder_configs(
    bobby_columnar_table_multi_batch_deterministic_data_context,
):
    data_context: AbstractDataContext = (
        bobby_columnar_table_multi_batch_deterministic_data_context
    )

    my_null_count_metric_multi_batch_parameter_builder_config = ParameterBuilderConfig(
        module_name="great_expectations.rule_based_profiler.parameter_builder",
        class_name="MetricMultiBatchParameterBuilder",
        name="my_null_count",
        metric_name=f"column_values.nonnull.{SummarizationMetricNameSuffixes.UNEXPECTED_COUNT.value}",
        metric_domain_kwargs=DOMAIN_KWARGS_PARAMETER_FULLY_QUALIFIED_NAME,
        metric_value_kwargs=None,
        enforce_numeric_metric=False,
        replace_nan_with_zero=False,
        reduce_scalar_metric=True,
        evaluation_parameter_builder_configs=None,
    )
    my_total_count_metric_multi_batch_parameter_builder_config = ParameterBuilderConfig(
        module_name="great_expectations.rule_based_profiler.parameter_builder",
        class_name="MetricMultiBatchParameterBuilder",
        name="my_total_count",
        metric_name="table.row_count",
        metric_domain_kwargs=DOMAIN_KWARGS_PARAMETER_FULLY_QUALIFIED_NAME,
        metric_value_kwargs=None,
        enforce_numeric_metric=False,
        replace_nan_with_zero=False,
        reduce_scalar_metric=True,
        evaluation_parameter_builder_configs=None,
    )

    evaluation_parameter_builder_configs: Optional[List[ParameterBuilderConfig]] = [
        my_null_count_metric_multi_batch_parameter_builder_config,
        my_total_count_metric_multi_batch_parameter_builder_config,
    ]
    unexpected_count_statistics_multi_batch_parameter_builder: ParameterBuilder = (
        UnexpectedCountStatisticsMultiBatchParameterBuilder(
            name="my_passenger_count_values_not_null_unexpected_count_statistics",
            unexpected_count_parameter_builder_name="my_null_count",
            total_count_parameter_builder_name="my_total_count",
            mode="unexpected_count_fraction_values",
            evaluation_parameter_builder_configs=evaluation_parameter_builder_configs,
            data_context=data_context,
        )
    )

    # Note: "evaluation_parameter_builder_configs" is not one of "ParameterBuilder" formal property attributes.
    assert set(
        unexpected_count_statistics_multi_batch_parameter_builder.to_json_dict().keys()
    ) == {
        "class_name",
        "module_name",
        "name",
        "unexpected_count_parameter_builder_name",
        "total_count_parameter_builder_name",
        "mode",
        "max_error_rate",
        "expectation_type",
        "evaluation_parameter_builder_configs",
    }


@pytest.mark.unit
@pytest.mark.parametrize(
    ["expectation_type", "mostly", "result"],
    [
        # Standardizes for expect_column_values_to_be_null
        ["expect_column_values_to_be_null", 1.0, 1.0],
        ["expect_column_values_to_be_null", 0.997, 0.99],
        ["expect_column_values_to_be_null", 0.99, 0.99],
        ["expect_column_values_to_be_null", 0.98, 0.975],
        ["expect_column_values_to_be_null", 0.975, 0.975],
        # returns mostly as-is
        ["expect_column_values_to_be_null", 0.9612, 0.9612],
        ["expect_column_values_to_be_null", 0.1010, 0.1010],
        #####
        # Standardizes for expect_column_values_to_not_be_null
        ["expect_column_values_to_not_be_null", 1.0, 1.0],
        ["expect_column_values_to_not_be_null", 0.997, 0.99],
        ["expect_column_values_to_not_be_null", 0.99, 0.99],
        # Rounds down to nearest 0.025
        ["expect_column_values_to_not_be_null", 0.62, 0.6],
        ["expect_column_values_to_not_be_null", 0.64, 0.625],
        ["expect_column_values_to_not_be_null", 0.062, 0.05],
    ],
)
def test_standardize_mostly_for_single_batch(expectation_type, mostly, result):
    assert _standardize_mostly_for_single_batch(expectation_type, mostly) == result
