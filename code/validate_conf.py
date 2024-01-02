from schema import And, Optional, Or, Schema


def list_string_example(resource, req=False):
    if not req:
        req_message = f"'{resource}' can also be left without a value to import all, such as:\n\t{resource}:"
    else:
        req_message = ""
    return f"""
'{resource}' expects list of strings in format such as:
    {resource}:
        - abc123
        - xyz789
Found non-list value or non-string value in list.
{req_message}
"""


def list_integer_example(resource, req=False):
    if not req:
        req_message = f"'{resource}' can also be left without a value to import all, such as:\n\t{resource}:"
    else:
        req_message = ""
    return f"""
'{resource}' expects list of integers in format such as:
    {resource}:
        - 12345
        - 67890
Found non-list value or non-integer value in list.
{req_message}
"""


def list_string_integer_example(resource, req=False):
    if not req:
        req_message = f"'{resource}' can also be left without a value to import all, such as:\n\t{resource}:"
    else:
        req_message = ""
    return f"""
'{resource}' expects list of strings or integers in format such as:
    {resource}:
        - 123456
        - foobarbiz
Found non-list value or non-string/integer value in list.
{req_message}
"""


def no_value_example(resource):
    return f"""
'{resource}' should not have a value if enabled, keep as the following if desired:
    {resource}:
"""


def aws_example():
    return f"""
'integration_aws' expects the following configuration:
    integration_aws:
        - aws_account_ids:
            - 123456789123
        - roles:
            - asdasdaszxczxczcx
        - account_role:
            - 1234:zxzxc
None of aws_account_ids, roles, or account_roles are required; more than one can be provided; if none provided
all resources for integration_aws will be imported.
"""


def slack_example():
    return f"""
The configuration for 'integration_slack_channel' is as follows:
    integration_slack_channel:
        - slack_account_channels:
            - account_name:
              - channel_name
              - other_channel
        - slack_account_names:
            - account_name
            - other_account_name
One of slack_account_channels or slack_account_names is required; more than one can be provided.
"""


def nested_resource(resource):
    return f"""
'{resource}' expects the following configuration:
    {resource}:
        - ids:
          - abc-123-xyz
          - bcd-456-qrs
        - tags:
          - env:prod
          - app:foo
        - tagsets:
          - team_a:
            - app:foo
            - env: prod
          - team_b:
            - team:b
            - app:bar
None of ids, tags, or tagsets is required; more than one can be provided. The value for {resource} can
also be left empty to impor all, such as:
    {resource}:
"""


def tagset_example():
    return f"""
'tagsets' expects a list of dictionaries, where the key of the dictionary is arbitrary (used for organization), and the value
is a list of tag combinations such as:
    - tagsets:
        - team_a:
        - app:foo
        - env: prod
        - team_b:
        - team:b
        - app:bar
"""


config_schema = Schema(
    {
        "resources": [
            Optional(
                {
                    "all": And(
                        None,
                        error=no_value_example("all"),
                    )
                }
            ),
            Optional(
                {"dashboard": Or([str], None, error=list_string_example("dashboard"))}
            ),
            Optional(
                {
                    "dashboard_list": Or(
                        [int],
                        None,
                        error=list_integer_example("dashboard_list"),
                    )
                }
            ),
            Optional(
                {
                    "logs_archive": Or(
                        [str],
                        None,
                        error=list_string_example("dashboarlogs_archived_list"),
                    )
                }
            ),
            Optional(
                {
                    "logs_archive_order": And(
                        None,
                        error=no_value_example("logs_archive_order"),
                    )
                }
            ),
            Optional(
                {
                    "logs_custom_pipeline": Or(
                        [str],
                        None,
                        error=list_string_example("logs_custom_pipeline"),
                    )
                }
            ),
            Optional(
                {
                    "logs_integration_pipeline": Or(
                        [str],
                        None,
                        error=list_string_example("logs_integration_pipeline"),
                    )
                }
            ),
            Optional(
                {
                    "logs_pipeline_order": And(
                        None, error=no_value_example("logs_pipeline_order")
                    )
                }
            ),
            Optional(
                {
                    "logs_index": Or(
                        [str],
                        None,
                        error=list_string_example("logs_pipeline_order"),
                    )
                }
            ),
            Optional(
                {
                    "logs_index_order": And(
                        None,
                        error=no_value_example("logs_index_order"),
                    )
                }
            ),
            Optional(
                {
                    "integration_aws": Or(
                        [
                            Optional(
                                {
                                    "aws_account_ids": And(
                                        [str, int],
                                        error=list_string_integer_example(
                                            "aws_account_ids", req=True
                                        ),
                                    )
                                }
                            ),
                            Optional(
                                {
                                    "roles": And(
                                        [str],
                                        error=list_string_example("roles", req=True),
                                    )
                                }
                            ),
                            Optional(
                                {
                                    "account_role": And(
                                        [str],
                                        error=list_string_example(
                                            "account_roles", req=True
                                        ),
                                    )
                                }
                            ),
                        ],
                        None,
                        error=aws_example(),
                    )
                }
            ),
            Optional(
                {
                    "integration_aws_lambda_arn": Or(
                        [str],
                        None,
                        error=list_string_example("integration_aws_lambda_arn"),
                    )
                }
            ),
            Optional(
                {
                    "integration_aws_log_collection": Or(
                        [str, int],
                        None,
                        error=list_string_integer_example(
                            "integration_aws_log_collection"
                        ),
                    )
                }
            ),
            Optional(
                {
                    "integration_azure": Or(
                        [str],
                        None,
                        error=list_string_example("integration_azure"),
                    )
                }
            ),
            Optional(
                {
                    "integration_pagerduty_service_object": Or(
                        [str],
                        None,
                        error=list_string_example(
                            "integration_pagerduty_service_object"
                        ),
                    )
                }
            ),
            Optional(
                {
                    "integration_slack_channel": Or(
                        [
                            Optional(
                                {
                                    "slack_account_channels": And(
                                        [{str: [lambda x: "#" not in x]}],
                                        error="'slack_account_channels' expects a list of dictionairies, with the key being the account name, and the value being a list of channels without the leading #.",
                                    )
                                }
                            ),
                            Optional(
                                {
                                    "slack_account_names": And(
                                        [str],
                                        error=list_string_example(
                                            "slack_account_names", req=True
                                        ),
                                    )
                                }
                            ),
                        ],
                        None,
                        error=slack_example(),
                    )
                }
            ),
            Optional(
                {
                    "metric_metadata": And(
                        [str],
                        error=list_string_example("metric_metadata", req=True),
                    )
                }
            ),
            Optional(
                {
                    "monitor": Or(
                        [
                            {
                                Optional("ids"): And(
                                    [int], error=list_integer_example("ids")
                                )
                            },
                            {
                                Optional("tags"): And(
                                    [str], error=list_string_example("tags")
                                )
                            },
                            {
                                Optional("tagsets"): And(
                                    [{str: [str]}], error=tagset_example()
                                )
                            },
                        ],
                        None,
                        error=nested_resource("monitor"),
                    )
                }
            ),
            {
                Optional("role"): Or(
                    [str],
                    error=list_string_example("metric_metadata"),
                )
            },
            {
                Optional("security_monitoring_default_rule"): And(
                    [str], error=list_string_example("security_monitoring_default_rule")
                )
            },
            {
                Optional("security_monitoring_rule"): And(
                    [str], error=list_string_example("security_monitoring_rule")
                )
            },
            Optional(
                {
                    "service_level_objective": Or(
                        [
                            {
                                Optional("ids"): And(
                                    [str], error=list_string_example("ids")
                                )
                            },
                            {
                                Optional("tags"): And(
                                    [str], error=list_string_example("tags")
                                )
                            },
                            {
                                Optional("tagsets"): And(
                                    [{str: [str]}], error=tagset_example()
                                )
                            },
                        ],
                        None,
                        error=nested_resource("service_level_objective"),
                    )
                }
            ),
            Optional(
                {
                    "synthetics_test": Or(
                        [
                            {
                                Optional("ids"): And(
                                    [str], error=list_string_example("ids")
                                )
                            },
                            {
                                Optional("tags"): And(
                                    [str], error=list_string_example("tags")
                                )
                            },
                            {
                                Optional("tagsets"): And(
                                    [{str: [str]}], error=tagset_example()
                                )
                            },
                        ],
                        None,
                        error=nested_resource("synthetics_test"),
                    )
                }
            ),
            {
                Optional("synthetics_global_variable"): Or(
                    [str],
                    error=list_string_example("synthetics_global_variable", req=True),
                )
            },
            {
                Optional("synthetics_private_location"): And(
                    [lambda x: "pl:" in x],
                    error="'synthetics_private_location' expects a list of strings of private location identifiers, including the leading pl:",
                )
            },
            {Optional("user"): Or([str], list_string_example("user"))},
        ]
    },
)
