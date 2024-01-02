# Datadog As Code Quick Start

This repository contains scripts to generate a repository of Terraform files for a given Datadog account.
The inspiration for creating this has come from many experiences with Datadog customers that want to 
maintain their Datadog environment as code, but also don't want to start from scratch.

This quick-start allows for a small amount of configuration that will generate Terraform files from existing
Datadog resources along with their current state, allowing for granular management by resource type in a 
very short span of time. The following Datadog resources are supported:

  - Dashboards
    - Dashboard configurations
    - Dashboard lists
  - Logging
    - Archives
    - Archive ordering
    - Custom pipelines
    - Integration pipelines
    - Pipeline ordering
    - Indexes
    - Index ordering
  - Integrations
    - AWS
      - Accounts
      - Log Lambdas
      - Log collection rules
    - Azure
      - Accounts
    - PagerDuty
      - Services
    - Slack
      - Channels
  - Metric metadata
  - Monitors
  - Security Rules
    - Enabled default rules
    - Custom rules
  - SLOs
  - Synthetics
    - Test definitions
    - Global variables
    - Private locations
  - User Management
    - Users
    - Roles

## Use Cases

There are several reasons to consider using this tool, and probably more that we have not thought of. 

- Create a basis for managing observability as code
- Import your most important/critical resources to ensure consistency in the future
- Import different sets of resources for different teams to manage
- Provide a backup of your current Datadog state

## What Does It Do, and How Does It Work?

The quick start is powered by [Terraform](https://www.terraform.io/), [Terraformer](https://github.com/GoogleCloudPlatform/terraformer),
the [Datadog Terraform provider](https://registry.terraform.io/providers/DataDog/datadog/latest/docs), and some custom scripting.

Terraformer utilizes Terraform and the Datadog provider to convert Datadog API responses into Terraform files along with their current
state. The custom scripting is responsible for manipulating the resulting Terraform and Terraform state files produced by Terraformer
as a result of some of the limitations of Terraformer itself, in addition to executing the Terraformer commands required to pull 
down Datadog resources based on the provided configuration.

The end result is a tree of files like will look similar to this:

```
.
└── datadog
    ├── dashboard
    │   ├── dashboard.tf
    │   ├── provider.tf
    │   └── terraform.tfstate
    ├── integration_slack_channel
    │   ├── integration_slack_channel.tf
    │   ├── provider.tf
    │   └── terraform.tfstate
    ├── monitor
    │   ├── monitor.tf
    │   ├── provider.tf
    │   └── terraform.tfstate
    └── user
        ├── provider.tf
        ├── terraform.tfstate
        └── user.tf
```

Each type of resource will have its own state file tracked independently, so changes to monitors will not
require interaction with any other resource types (for example).

Once this import has been completed, the next steps are left up to the user. We chose to not be prescriptive with
next steps, as there can be many directions to go based on organizational preference or initial necessity for
generating these files. We have provided some suggestions below in the "Where To Go From Here" section.

## What Doesn't This Do?

- This quick start will not affect the current state of your Datadog environment; it will only read it and generate Terraform files based on it
- It will not maintain the state that it imported; this is a one time import, not programmatic management
- Any resource that is not imported via the configuration of this toolset will not be managed by Terraform

## Requirements

All that is required to run this is Docker and docker-compose.

**NOTE**: If you chose to use the files generated outside of this repository, you will need to have Terraform installed.

## Configuration & Usage

1. Copy `.env.sample` to `.env` via `mv .env.sample .env`
2. In the `.env` file, update your API and Application keys, and Site value if necessary
    - Application key must be scoped to have read capabilities to the account
3. Run `docker-compose build`
4. Edit the conf.yaml file to your desired configuration (see `example_conf.yaml` for more detail)
5. Run `docker-compose run ddtf` to execute the process

**Note**: Due to how files are imported and merged, it is recommend that if a subsequent run is required
to account for a configuration change or something that was missed initially that the generated files in the 
`datadog` directory are removed. This will avoid unintentional duplication of resource definitions and 
maintain the general cleanliness of the resulting files.

## Next Steps

Now that you have generated your desired Datadog resources as Terraform files, there are many directions you
can choose to make next steps towards.

**We recommend moving the generated files from `terraform/datadog` to another folder or repository. If you choose to
run the code in this repository again, those will be overwritten.**

Once that has been completed, here are some other ideas:

- State Backends
  - Generally speaking, it is not desirable to store Terraform state files locally, as that could lead to accidentally committing
  credentials to a repository, or make collaboration difficult. After the files are generated, you may want to create a `backend.tf`
  file or add to `provider.tf` to establish one of the many [backends that Terraform provides](https://developer.hashicorp.com/terraform/language/settings/backends/configuration).
  - Once you have added a backend, such as Azure Storage or AWS S3, you will need to run `terraform init -migrate-state`. This will move the generated
  state file to your configured backend.
- Initialize Terraform for a resource type
  - Each type of resource contains its own state file, and is managed independently. In order to be able to 
  utilize Terraform to manage these, Terraform will need to be initialized within that directory. To do so, enter 
  the resource directory and execute `terraform init`. You will now be able to run additional Terraform commands.
- CI
  - Consider building a CI process around a repository containing the generated files. This can allow for reviewing changes
  to critical dashboards and monitors to maintain standards and consistency, or preserve ownership of monitoring to a dedicated
  team. A common process would look something like this:
    - User enters a merge/pull request to the repository with a change to a resource
    - A job detects a change to that resource type, and runs a `terraform plan` against the resource to show the 
    user or reviewer exactly what would change, and ensure nothing is done unintentionally.
    - The change is reviewed, approved, and merged
    - Another set of jobs runs to apply the changes and commit the new state
- Separate Management Responsibilities
  - While this repository is intended to be used for grabbing large sets of resources based on configuration at a time, it is also possible
  to utilize it multiple times for smaller sets. As an example, consider utilizing this tooling to pull down monitors on a team tag by team
  tag basis, and then moving the generated files out to a team specific directory or repository. This can allow for distinct management
  on a team by team or app by app basis without a monolithic type monitoring repository.
- Add New Dashboards via JSON
  - Admittedly, the generated Terraform files for monitors and dashboards can be clunky, large, and difficult to understand how and where
  changes are made. The good news is that monitors and dashboards (only) can be exported from Datadog as JSON and then established within
  the Terraform files in the same format. This allows a user to go and make graphical changes in the UI, export the results, and then
  recommit the changes to the repository. There are a few ways to go about this, but the following is a suggested method. 
  - Given the following
  structure:

    ```
    .
    └── datadog
        ├── dashboard
        │   ├── dashboard.tf
        │   ├── provider.tf
        │   └── terraform.tfstate
        └── monitor
            ├── provider.tf
            ├── terraform.tfstate
            └── monitor.tf
    ```
    We can then create a `files` directory within each resource directory, export a dashboard as JSON, and add that file to the created directory:
    ```
    .
    └── datadog
    │   └── dashboard
    │       ├── dashboard.tf
    │       ├── files
    │       │   └── example.json
    │       ├── provider.tf
    │       └── tfstate.tf
    │   └── monitor
    │       ├── provider.tf
    │       ├── terraform.tfstate
    │       └── monitor.tf
    ```
    Within the `dashboard.tf` file, we can then add the following:
    ```hcl
    resource "datadog_dashboard_json" "example_dashboard" {
        dashboard = file("../example.json")
    }
    ```
    - This process is the same for monitors, just utilizing the appropriate files
    - *Note*: If you are going to replace a dashboard/monitor that has already been imported in HCL, 
    you will want to remove that entry from the file before applying the JSON change.
    - *Note*: Exporting a Datadog resource as JSON and then applying it with Terraform will cause a
    duplicate resource in Datadog, since the state was not imported. To avoid this, you can utilize
    the `terraform import` command which will update the state file appropriately. As an example,
    `terraform import datadog_dashboard_json.example_dashboard abc-123-xyz`


## Known Issues

There are some known issues with this repository, largely due to the usage of other
open source tools.

- Not all Datadog resources available
  - Terraformer does not support all of the Datadog resources that are currently available
  from the Datadog provider. As more functionality is released, this repository will be updated.
- GCP integration importing 
  - As of time of writing, Terraformer has not caught up with the change to how GCP accounts are
  added to Datadog, and as a result, GCP accounts cannot be imported directly. The good news is that
  creating the required Terraform definitions for these is not overly complicated, and documentation
  for doing such [can be found here](https://registry.terraform.io/providers/DataDog/datadog/latest/docs/resources/integration_gcp)
- Monitor Downtime importing
  - Due to API changes as of time of writing, Terraformer is not up to date with importing Monitor downtimes
- PagerDuty schedules
  - Due to API changes as of time of writing, Terraformer is not up to date with importing PagerDuty Schedules (services work, however)
- Terraformer/Datadog Provider performance
  - Due to a potentially large amount of API requests that are required to generate these files, sometimes the performance
  of this scripting can be slow, or present errors. The majority of the common occurrences have been accounted for by built-in Terraformer retries
  and additional retry loops within the scripting around this process. Any failures should be validated, as a retry was likely successful.
- Not intended to be run regularly
  - As stated in the documentation above, this repository is meant for an initial quick-start import. This is not meant to be 
  a regularly run process, and if used as such may cause unintentional behavior within the management of Datadog resources.

## Support

Have a question, need some help, or want to report a bug? Please enter an issue within the repository.

Need more help than we can give through an Issue? [Head over to our website and get in touch!](https://www.nobs.tech/contact)