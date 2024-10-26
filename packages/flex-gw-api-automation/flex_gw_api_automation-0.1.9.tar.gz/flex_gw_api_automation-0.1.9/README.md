# API Deployment Script Documentation

## Table of Contents
- [Prerequisites](#prerequisites)
- [Usage and Modules](#usage-and-modules)
  - [Flex GW API Deployment](#flex-gw-api-deployment)
    - [1. Using Command-Line Arguments](#1-using-command-line-arguments)
    - [2. Using a YAML Configuration File](#2-using-a-yaml-configuration-file)
      - [Minimal YAML Configuration](#minimal-yaml-configuration)
      - [Full YAML Configuration](#full-yaml-configuration)
    - [Notes](#notes)
    - [Output](#output)
- [Packaging and Dependencies](#packaging-and-dependencies)
  - [Install Dependencies Manually and Run Script](#install-dependencies-manually-and-run-script)
  - [Package using PyPi and Pip](#package-using-pypi-and-pip)
    - [Install Poetry](#install-poetry)
    - [Configure PyPI Repository](#configure-pypi-repository)
    - [Publish Package](#publish-package)
    - [Use Pip Package](#use-pip-package)
- [Collaborate](#collaborate)

This script allows you to deploy an API to Anypoint Platform using either command-line arguments or a YAML configuration file.

## Prerequisites

- Python 3.x
- pip
- Anypoint Platform Connected App
- API Spec uploaded to Anypoint Exchange

### Connected App

The Anypoint Platform API credentials are required to authenticate with the Anypoint Platform API. The Connected App should have the following permissions:

- **API Manager:** Manage APIs Configuration, Manage Policies, Manage Contracts, and Deploy API Proxies
- **Runtime Manager:** Read Servers, Manage Servers, Create Applications, and Delete Applications
- **Exchange:** Exchange Contributor and Exchange Viewer
- **General:** View Organization, View Client Management Providers
- **OpenID:** Profile
- **Secrets Manager:** Grant access to secrets

## Usage and Modules

### Flex GW API Deployment

The Flex Gateway API Deployment script can be run in two ways:

1. Using command-line arguments
2. Using a YAML configuration file

#### 1. Using Command-Line Arguments

To run the script with command-line arguments, use the following format:

```bash
python3 -m flex_gw_api_automation.flex_gw --action deploy --bg-name "Your BG" --env-name "Your Env" --flex-gw-instance-name "Your FG" --client-id "Your ID" --client-secret "Your Secret" --api-spec-group-id "Your Group ID" --api-spec-asset-id "Your Asset ID" --api-spec-version "Your Version" --listener-port 8081 --listener-basepath "/api" --upstream-url "http://your-upstream-url"
```

Replace the placeholder values with your actual configuration details.

#### 2. Using a YAML Configuration File

To run the script with a YAML configuration file, use the following format:

```bash
python3 -m flex_gw_api_automation.flex_gw --action deploy --file your_config.yaml
```

##### Minimal YAML Configuration

A minimal YAML configuration file should contain only the required parameters. Here's an example:

```yaml
bg_name: "Your Business Group"
env_name: "Your Environment"
flex_gw_instance_name: "Your Flex Gateway Instance"
client_id: "Your Client ID"
client_secret: "Your Client Secret"
api_spec_group_id: "Your API Spec Group ID"
api_spec_asset_id: "Your API Spec Asset ID"
api_spec_version: "Your API Spec Version"
listener_port: 8081
listener_basepath: "/api"
routes:
  - label: "default"
    upstreams:
      - label: "default"
        uri: "http://your-upstream-url"
        weight: 100
```

Save this as `deploy_config_minimal.yaml` and run:

```bash
python3 -m flex_gw_api_automation.flex_gw --action deploy --file deploy_config_minimal.yaml
```

##### Full YAML Configuration

A full YAML configuration file should contain all the required and optional parameters. Here's an example:

```yaml
bg_name: "Your Business Group"
env_name: "Your Environment"
ext_client_provider_name: "Your External Client Provider Name"
flex_gw_instance_name: "Your Flex Gateway Instance"
client_id: "Your Client ID"
client_secret: "Your Client Secret"
api_spec_group_id: "Your API Spec Group ID"
api_spec_asset_id: "Your API Spec Asset ID"
api_spec_version: "Your API Spec Version"
listener_port: 8081
listener_basepath: "/api"

routes:
  - label: Route 1
    methods: POST|PUT
    host: www.example.com
    path: /test/*
    headers:
      destination: "2"
    upstreams:
      - label: httpbin1
        uri: http://httpbin.org
        weight: 100
        tls_context:
          secret_group_name: "flex-gateway-secret-group"
          tls_context_name: "flex-gateway-tls-context"
  - label: Route 2
    methods: null
    host: null
    path: null
    headers: {}
    upstreams:
      - label: httpbin2
        uri: http://httpbin.org
        weight: 50
        tls_context:
          secret_group_name: "flex-gateway-secret-group"
          tls_context_name: "flex-gateway-tls-context"
      - label: httpbin3
        uri: http://httpbin.org
        weight: 50
        tls_context:
          secret_group_name: "flex-gateway-secret-group"
          tls_context_name: "flex-gateway-tls-context"

sla_tiers:
  - name: Gold
    description: Gold Tier
    autoapprove: false
    max_requests: 1000
    timeperiodmillis: 3600000

policies:
  - group_id: 68ef9520-24e9-4cf2-b2f5-620025690913
    asset_id: message-logging
    policy_version: "2.0.1"
    configuration_data:
      loggingConfiguration: 
        - itemName: Log
          itemData:
            message: "#['TEST']"
            level: "INFO"
            firstSection: true
            secondSection: false
```

Save this as `deploy_config.yaml` and run:

```bash
python3 -m flex_gw_api_automation.flex_gw --action deploy --file deploy_config.yaml
```

#### Notes

- The command-line argument method is suitable for basic deployments with one upstream and no policies or SLA tiers.
- The YAML file method allows for more complex configurations and is recommended for production deployments.
- Ensure all required fields are provided, whether using command-line arguments or a YAML file.

#### Output

The example output will look like this:

```bash
Authenticating with Anypoint Platform
Getting Business Group ID for: <Business Group>
Business Group ID: <Business Group ID>
Getting Environment ID for: <Environment>
Environment ID: <Environment ID>
Getting Client Provider ID for: <External Provider Name>
Client Provider ID: <External Provider ID>
Getting Flex Gateway Instance ID for: <Instance Name>
Flex Gateway Instance ID: <Instance ID>
Creating API Instance
Getting Secret Group ID for: <Secret Group Name>
Getting TLS Context ID for: <TLS Context Name>
Getting Secret Group ID for: <Secret Group Name>
Getting TLS Context ID for: <TLS Context Name>
API Instance ID: <API Instance ID>
Creating SLA Tiers
Created SLA Tier: Gold
Created SLA Tier IDs: [<SLA Tier ID>]
Applying Policies
Applied Policy: message-logging
Applied Policy IDs: [<Policy ID>]
Deploying API Instance: <API Instance ID>
API Instance <API Instance ID> deployment initiated successfully
API deployment completed successfully!
```

## Packaging and Dependencies

This script can be packaged as a Python package and imported or downloaded using Pip. Another option is to zip and download the script folder and install the dependencies manually.

### Install Dependencies Manually and Run Script

```sh
pip install -r requirements.txt
python3 -m flex_gw_api_automation.flex_gw --action deploy <COMMANDS>
```

### Package using PyPi and Pip

This script can be transformed into a Python Package using Poetry and be uploaded to any PyPI repository.

#### Install Poetry

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Or

```sh
pip install poetry
```

#### Configure PyPI Repository

To generate the package and publish it to a PyPI repository first you have to configure the URL and credentials. For example, use the default PyPI public repository:

```sh
poetry config pypi-token.pypi <PYPI_API_TOKEN>
```

For more information:
[Poetry Docs - Repository](https://python-poetry.org/docs/repositories/)

#### Publish Package

First, generate the requirements.txt file that will be used by pip if the package is downloaded manually. Then, publish the package.

```sh
poetry export -f requirements.txt --output requirements.txt --without-hashes
poetry publish
```


#### Use Pip Package

If the library is uploaded to your PyPI repository, you can download the package as a Pip dependency and use it.

```sh
pip install flex-gw-api-automation
python -m flex_gw_api_automation.flex_gw --action deploy <COMMANDS>
```

## Collaborate

To work with this Python package you'll need **Poetry** installed.

Create a virtual environment running

```sh
poetry install
poetry env info
```

Activate the Poetry environment and run the script:

```sh
poetry shell
python -m flex_gw_api_automation.flex_gw --action deploy
```
