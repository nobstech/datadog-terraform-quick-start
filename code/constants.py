LIST_RESOURCES = [
    "dashboard",
    "dashboard_list",
    "logs_archive",
    "logs_custom_pipeline",
    "logs_integration_pipeline",
    "logs_index",
    "integration_aws_lambda_arn",
    "integration_aws_log_collection",
    "integration_azure",
    "integration_pagerduty_service_object",
    "metric_metadata",
    "role",
    "security_monitoring_default_rule",
    "security_monitoring_rule",
    "synthetics_global_variable",
    "synthetics_private_location",
    "user",
]

NO_ID_RESOURCES = [
    "logs_archive_order",
    "logs_pipeline_order",
    "logs_index_order",
]

NESTED_RESOURCES = ["monitor", "service_level_objective", "synthetics_test"]

OTHER_RESOURCES = [
    "integration_aws",
    "integration_slack_channel",
]

SUPPORTED_RESOURCES = (
    LIST_RESOURCES + NO_ID_RESOURCES + NESTED_RESOURCES + OTHER_RESOURCES + ["all"]
)

ID_MAP = {
    "integration_aws_lambda_arn": "lambda_arn",
    "aws_account_ids": "account_id",
    "roles": "role_name",
    "slack_account_names": "account_name",
    "slack_account_channels": "channel_name",
    "integration_azure": "client_id",
}

HAS_COLONS = [
    "integration_aws_lambda_arn",
    "synthetics_private_location",
    "tags",
    "tagsets",
]
