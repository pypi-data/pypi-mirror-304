from typing import TYPE_CHECKING, Optional

from great_expectations.compatibility.typing_extensions import override
from great_expectations.core import ExpectationConfiguration
from great_expectations.core._docs_decorators import public_api
from great_expectations.expectations.expectation import (
    ColumnMapExpectation,
    InvalidExpectationConfigurationError,
)
from great_expectations.render.renderer_configuration import (
    RendererConfiguration,
    RendererValueType,
)

if TYPE_CHECKING:
    from great_expectations.render.renderer_configuration import AddParamArgs


class ExpectColumnValueZScoresToBeLessThan(ColumnMapExpectation):
    """Expect the Z-scores of a column's values to be less than a given threshold.

    expect_column_values_to_be_of_type is a \
    [Column Map Expectation](https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/how_to_create_custom_column_map_expectations) \
    for typed-column backends, and also for PandasExecutionEngine where the column \
    dtype and provided type_ are unambiguous constraints \
    (any dtype except 'object' or dtype of 'object' with type_ specified as 'object').

    Args:
        column (str): \
            The column name of a numerical column.
        threshold (number): \
            A maximum Z-score threshold. All column Z-scores that are lower than this threshold will evaluate \
            successfully.

    Keyword Args:
        mostly (None or a float between 0 and 1): \
            Successful if at least mostly fraction of values match the expectation. \
            For more detail, see [mostly](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#mostly).
        double_sided (boolean): \
            A True or False value indicating whether to evaluate double sidedly. Examples... \
            (double_sided = True, threshold = 2) -> Z scores in non-inclusive interval(-2,2) | \
            (double_sided = False, threshold = 2) -> Z scores in non-inclusive interval (-infinity,2)

    Other Parameters:
        result_format (str or None): \
            Which output mode to use: BOOLEAN_ONLY, BASIC, COMPLETE, or SUMMARY. \
            For more detail, see [result_format](https://docs.greatexpectations.io/docs/reference/expectations/result_format).
        include_config (boolean): \
            If True, then include the Expectation config as part of the result object.
        catch_exceptions (boolean or None): \
            If True, then catch exceptions and include them as part of the result object. \
            For more detail, see [catch_exceptions](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#catch_exceptions).
        meta (dict or None): \
            A JSON-serializable dictionary (nesting allowed) that will be included in the output without \
            modification. For more detail, see [meta](https://docs.greatexpectations.io/docs/reference/expectations/standard_arguments/#meta).

    Returns:
        An [ExpectationSuiteValidationResult](https://docs.greatexpectations.io/docs/terms/validation_result)

        Exact fields vary depending on the values passed to result_format, include_config, catch_exceptions, and meta.
    """

    # This dictionary contains metadata for display in the public gallery
    library_metadata = {
        "maturity": "production",
        "tags": ["core expectation", "column map expectation"],
        "contributors": ["@great_expectations"],
        "requirements": [],
        "has_full_test_suite": True,
        "manually_reviewed_code": True,
    }

    # Setting necessary computation metric dependencies and defining kwargs, as well as assigning kwargs default values\
    map_metric = "column_values.z_score.under_threshold"
    success_keys = ("threshold", "double_sided", "mostly")

    # Default values
    default_kwarg_values = {
        "row_condition": None,
        "condition_parser": None,
        "threshold": None,
        "double_sided": True,
        "mostly": 1,
        "result_format": "BASIC",
        "include_config": True,
        "catch_exceptions": False,
    }
    args_keys = ("column", "threshold")

    @public_api
    @override
    def validate_configuration(
        self, configuration: Optional[ExpectationConfiguration] = None
    ) -> None:
        """
        Validate the configuration of an Expectation.

        For `expect_column_value_z_scores_to_be_less_than` it is required that:
            - A Z-score `threshold` is provided.
            - `threshold` is one of the following types: `float`, `int`, or `dict`
            - If `threshold` is a `dict`, it is assumed to be an Evaluation Parameter, and therefore the
             dictionary keys must be `$PARAMETER`.
            - If provided, `double_sided` is one of the following types: `bool` or `dict`
            - If `double_sided` is a `dict`, it is assumed to be an Evaluation Parameter, and therefore the
             dictionary keys must be `$PARAMETER`.

        The configuration will also be validated using each of the `validate_configuration` methods in its Expectation
        superclass hierarchy.

        Args:
            configuration: An `ExpectationConfiguration` to validate. If no configuration is provided, it will be pulled
            from the configuration attribute of the Expectation instance.

        Raises:
            `InvalidExpectationConfigurationError`: The configuration does not contain the values required by the
            Expectation
        """
        # Setting up a configuration
        super().validate_configuration(configuration)
        configuration = configuration or self.configuration
        try:
            # Ensuring Z-score Threshold metric has been properly provided
            assert (
                "threshold" in configuration.kwargs
            ), "A Z-score threshold must be provided"
            assert isinstance(
                configuration.kwargs["threshold"], (float, int, dict)
            ), "Provided threshold must be a number"
            if isinstance(configuration.kwargs["threshold"], dict):
                assert (
                    "$PARAMETER" in configuration.kwargs["threshold"]
                ), 'Evaluation Parameter dict for threshold kwarg must have "$PARAMETER" key.'

            assert isinstance(
                configuration.kwargs["double_sided"], (bool, dict)
            ), "Double sided parameter must be a boolean value"
            if isinstance(configuration.kwargs["double_sided"], dict):
                assert (
                    "$PARAMETER" in configuration.kwargs["double_sided"]
                ), 'Evaluation Parameter dict for double_sided kwarg must have "$PARAMETER" key.'
        except AssertionError as e:
            raise InvalidExpectationConfigurationError(str(e))

    @override
    @classmethod
    def _prescriptive_template(
        cls,
        renderer_configuration: RendererConfiguration,
    ) -> RendererConfiguration:
        add_param_args: AddParamArgs = (
            ("column", RendererValueType.STRING),
            ("threshold", RendererValueType.NUMBER),
            ("double_sided", RendererValueType.BOOLEAN),
            ("mostly", RendererValueType.NUMBER),
        )
        for name, param_type in add_param_args:
            renderer_configuration.add_param(name=name, param_type=param_type)

        params = renderer_configuration.params

        if renderer_configuration.include_column_name:
            template_str = "$column value z-scores must be "
        else:
            template_str = "Value z-scores must be "

        if params.double_sided.value is True:
            inverse_threshold = params.threshold.value * -1
            renderer_configuration.add_param(
                name="inverse_threshold", param_type=RendererValueType.NUMBER
            )
            if inverse_threshold < params.threshold.value:
                template_str += (
                    "greater than $inverse_threshold and less than $threshold"
                )
            else:
                template_str += (
                    "greater than $threshold and less than $inverse_threshold"
                )
        else:
            template_str += "less than $threshold"

        if params.mostly and params.mostly.value < 1.0:
            renderer_configuration = cls._add_mostly_pct_param(
                renderer_configuration=renderer_configuration
            )
            template_str += ", at least $mostly_pct % of the time."
        else:
            template_str += "."

        renderer_configuration.template_str = template_str

        return renderer_configuration
