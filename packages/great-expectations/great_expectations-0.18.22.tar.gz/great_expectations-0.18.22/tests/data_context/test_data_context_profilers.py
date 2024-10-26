from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from marshmallow import ValidationError

from great_expectations.core.batch import BatchRequest
from great_expectations.data_context.store.profiler_store import ProfilerStore
from great_expectations.rule_based_profiler.config import RuleBasedProfilerConfig
from great_expectations.rule_based_profiler.rule_based_profiler import RuleBasedProfiler

if TYPE_CHECKING:
    from great_expectations.data_context import FileDataContext


@pytest.mark.unit
def test_add_profiler(
    empty_data_context: FileDataContext,
    profiler_config_with_placeholder_args: RuleBasedProfilerConfig,
):
    args = profiler_config_with_placeholder_args.to_json_dict()
    for attr in ("class_name", "module_name", "id"):
        args.pop(attr, None)

    profiler = empty_data_context.add_profiler(**args)
    assert isinstance(profiler, RuleBasedProfiler)


@pytest.mark.unit
def test_add_profiler_with_invalid_config_raises_error(
    empty_data_context: FileDataContext,
    profiler_config_with_placeholder_args: RuleBasedProfilerConfig,
):
    args = profiler_config_with_placeholder_args.to_json_dict()
    for attr in ("class_name", "module_name", "id"):
        args.pop(attr, None)

    # Setting invalid configuration to check that it is caught by DataContext wrapper method
    args["config_version"] = -1

    with pytest.raises(ValidationError) as e:
        empty_data_context.add_profiler(**args)

    assert "config_version" in str(e.value)


@pytest.mark.unit
@mock.patch("great_expectations.rule_based_profiler.RuleBasedProfiler.run")
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_run_profiler_with_dynamic_arguments_emits_proper_usage_stats(
    mock_emit: mock.MagicMock,
    mock_profiler_run: mock.MagicMock,
    empty_data_context_stats_enabled: FileDataContext,
    populated_profiler_store: ProfilerStore,
    profiler_name: str,
):
    with mock.patch(
        "great_expectations.data_context.AbstractDataContext.profiler_store"
    ) as mock_profiler_store:
        mock_profiler_store.__get__ = mock.Mock(return_value=populated_profiler_store)
        empty_data_context_stats_enabled.run_profiler_with_dynamic_arguments(
            name=profiler_name
        )

    assert mock_emit.call_count == 1
    assert mock_emit.call_args_list == [
        mock.call(
            {
                "event_payload": {},
                "event": "data_context.run_profiler_with_dynamic_arguments",
                "success": True,
            }
        )
    ]


@pytest.mark.unit
@mock.patch("great_expectations.rule_based_profiler.RuleBasedProfiler.run")
@mock.patch(
    "great_expectations.core.usage_statistics.usage_statistics.UsageStatisticsHandler.emit"
)
def test_run_profiler_on_data_emits_proper_usage_stats(
    mock_emit: mock.MagicMock,
    mock_profiler_run: mock.MagicMock,
    empty_data_context_stats_enabled: FileDataContext,
    populated_profiler_store: ProfilerStore,
    profiler_name: str,
):
    with mock.patch(
        "great_expectations.data_context.AbstractDataContext.profiler_store"
    ) as mock_profiler_store:
        mock_profiler_store.__get__ = mock.Mock(return_value=populated_profiler_store)
        empty_data_context_stats_enabled.run_profiler_on_data(
            name=profiler_name,
            batch_request=BatchRequest(
                **{
                    "datasource_name": "my_datasource",
                    "data_connector_name": "my_data_connector",
                    "data_asset_name": "my_data_asset",
                }
            ),
        )

    assert mock_emit.call_count == 1
    assert mock_emit.call_args_list == [
        mock.call(
            {
                "event_payload": {},
                "event": "data_context.run_profiler_on_data",
                "success": True,
            }
        )
    ]
