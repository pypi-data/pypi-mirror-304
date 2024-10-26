import sys
import yaml
import argparse
import yamale
from io import StringIO
from typing import List, Optional
from .anypoint_platform import APIManager, AccessManagement
from .anypoint_platform.entities import Route, Upstream, SLATier, Policy, TLSContext
from .anypoint_platform.access_management import AuthenticationError
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Embedded YAML schema
YAML_SCHEMA = """
bg_name: str()
env_name: str()
flex_gw_instance_name: str()
client_id: str()
client_secret: str()
api_spec_group_id: str()
api_spec_asset_id: str()
api_spec_version: str()
listener_port: int()
listener_basepath: str()
ext_client_provider_name: str(required=False)
routes: list(include('route'), min=1)
sla_tiers: list(include('sla_tier'), required=False)
policies: list(include('policy'), required=False)

---
route:
  label: str()
  upstreams: list(include('upstream'), min=1)
  methods: str(required=False)
  host: str(required=False)
  path: str(required=False)
  headers: map(required=False)

upstream:
  label: str()
  uri: str()
  weight: int()
  tls_context: include('tls_context', required=False)

tls_context:
  secret_group_name: str()
  tls_context_name: str()

sla_tier:
  name: str()
  description: str()
  autoapprove: bool()
  max_requests: int()
  timeperiodmillis: int()

policy:
  group_id: str()
  asset_id: str()
  policy_version: str()
  configuration_data: map()
"""

class FlexGW:
    @staticmethod
    def deploy(
        bg_name: str,
        env_name: str,
        ext_client_provider_name: str,
        flex_gw_instance_name: str,
        client_id: str,
        client_secret: str,
        api_spec_group_id: str,
        api_spec_asset_id: str,
        api_spec_version: str,
        listener_port: int,
        listener_basepath: str,
        routes: List[Route],
        sla_tiers: List[SLATier],
        policies: List[Policy]
    ) -> None:
        try:
            # Authenticate and get access token
            token = AccessManagement.get_access_token(client_id, client_secret)
            
            # Get Business Group ID
            bg_id = AccessManagement.get_business_group_id(token.access_token, bg_name)
            if bg_id is None:
                logger.error(f"Failed to get Business Group ID for '{bg_name}'. Aborting deployment.")
                return

            logger.info(f"Business Group ID: {bg_id}")

            # Get Environment ID
            env_id = AccessManagement.get_environment_id(token.access_token, bg_id, env_name)
            if env_id is None:
                logger.error(f"Failed to get Environment ID for '{env_name}'. Aborting deployment.")
                return

            logger.info(f"Environment ID: {env_id}")

            # Get Client Provider ID
            client_provider_id = AccessManagement.get_client_provider_id(token.access_token, bg_id, ext_client_provider_name)
            logger.info(f"Client Provider ID: {client_provider_id}")

            # Get Flex Gateway Instance ID
            flex_gw_instance_id = APIManager.get_flex_gw_instance_id(token.access_token, bg_id, env_id, flex_gw_instance_name)
            if flex_gw_instance_id is None:
                logger.error(f"Failed to get Flex Gateway Instance ID for '{flex_gw_instance_name}'. Aborting deployment.")
                return

            logger.info(f"Flex Gateway Instance ID: {flex_gw_instance_id}")

            # Create API Instance
            api_instance_id = APIManager.create_api_instance(
                token.access_token,
                bg_id,
                env_id,
                client_provider_id,
                flex_gw_instance_id,
                flex_gw_instance_name,
                api_spec_group_id,
                api_spec_asset_id,
                api_spec_version,
                listener_port,
                listener_basepath,
                routes
            )
            if api_instance_id is None:
                logger.error("Failed to create API Instance. Aborting deployment.")
                return

            logger.info(f"API Instance ID: {api_instance_id}")

            # Create SLA Tiers
            sla_tier_ids = APIManager.create_sla_tiers(
                token.access_token,
                bg_id,
                env_id,
                api_instance_id,
                sla_tiers
            )

            logger.info(f"Created SLA Tier IDs: {[id for id in sla_tier_ids if id is not None]}")

            # Apply Policies
            policy_ids = APIManager.apply_policies(
                token.access_token,
                bg_id,
                env_id,
                api_instance_id,
                policies
            )

            logger.info(f"Applied Policy IDs: {[id for id in policy_ids if id is not None]}")

            # Deploy API Instance
            deployment_success = APIManager.deploy_instance(
                token.access_token,
                bg_id,
                env_id,
                api_instance_id,
                flex_gw_instance_id,
                flex_gw_instance_name
            )

            if not deployment_success:
                logger.error("Failed to initiate API Instance deployment. Aborting.")
                return

            logger.info("API deployment completed successfully!")
        except AuthenticationError as e:
            logger.error(f"Error: {e}")
            logger.error("API deployment failed due to authentication error.")
            return
        except Exception as e:
            logger.error(f"Error: An unexpected error occurred - {e}")
            logger.error("API deployment failed.")
            return

def load_and_validate_yaml_config(file_path: str) -> dict:
    try:
        schema = yamale.make_schema(content=YAML_SCHEMA)
        data = yamale.make_data(file_path)
        yamale.validate(schema, data)
        
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yamale.YamaleError as e:
        logger.error(f"Configuration validation error:")
        for result in e.results:
            logger.error(f"  {result}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        sys.exit(1)

def create_upstream(upstream_data: dict) -> Upstream:
    tls_context_data = upstream_data.pop('tls_context', None)
    tls_context = TLSContext(**tls_context_data) if tls_context_data else None
    return Upstream(**upstream_data, tls_context=tls_context)

def create_route(route_data: dict) -> Route:
    upstreams = [create_upstream(upstream) for upstream in route_data.pop('upstreams', [])]
    return Route(**route_data, upstreams=upstreams)

def main():
    parser = argparse.ArgumentParser(description="Deploy API using configuration from a YAML file or command-line arguments.")
    
    # File-based configuration
    parser.add_argument("--file", help="Path to the YAML configuration file")
    
    # Command-line arguments
    parser.add_argument("--bg-name", help="Business Group Name")
    parser.add_argument("--env-name", help="Environment Name")
    parser.add_argument("--flex-gw-instance-name", help="Flex Gateway Instance Name")
    parser.add_argument("--client-id", help="Client ID")
    parser.add_argument("--client-secret", help="Client Secret")
    parser.add_argument("--api-spec-group-id", help="API Specification Group ID")
    parser.add_argument("--api-spec-asset-id", help="API Specification Asset ID")
    parser.add_argument("--api-spec-version", help="API Specification Version")
    parser.add_argument("--listener-port", type=int, help="Listener Port")
    parser.add_argument("--listener-basepath", help="Listener Basepath")
    parser.add_argument("--upstream-url", help="Upstream URL")
    parser.add_argument("--action", choices=['deploy'], help="Action to perform")

    args = parser.parse_args()

    try:
        if args.action == "deploy":  # Check for the "deploy" action
            if args.file:
                config = load_and_validate_yaml_config(args.file)
                routes = [create_route(route) for route in config.pop('routes', [])]
                sla_tiers = [SLATier(**tier) for tier in config.pop('sla_tiers', [])] if 'sla_tiers' in config else None
                policies = [Policy(**policy) for policy in config.pop('policies', [])] if 'policies' in config else None
                ext_client_provider_name = config.pop('ext_client_provider_name', None)
            else:
                # Create config from command-line arguments
                config = {
                    'bg_name': args.bg_name,
                    'env_name': args.env_name,
                    'flex_gw_instance_name': args.flex_gw_instance_name,
                    'client_id': args.client_id,
                    'client_secret': args.client_secret,
                    'api_spec_group_id': args.api_spec_group_id,
                    'api_spec_asset_id': args.api_spec_asset_id,
                    'api_spec_version': args.api_spec_version,
                    'listener_port': args.listener_port,
                    'listener_basepath': args.listener_basepath,
                }
                
                # Create a single route with a single upstream
                routes = [Route(
                    label="default",
                    upstreams=[Upstream(label="default", uri=args.upstream_url, weight=100)],
                    methods=None,
                    host=None,
                    path=None,
                    headers=None
                )]
                
                sla_tiers = None
                policies = None
                ext_client_provider_name = None

            # Validate that all required fields are present
            required_fields = ['bg_name', 'env_name', 'flex_gw_instance_name', 'client_id', 'client_secret',
                               'api_spec_group_id', 'api_spec_asset_id', 'api_spec_version', 'listener_port', 'listener_basepath']
            missing_fields = [field for field in required_fields if not config.get(field)]
            if missing_fields:
                raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

            FlexGW.deploy(
                **config,
                routes=routes,
                sla_tiers=sla_tiers or [],
                policies=policies or [],
                ext_client_provider_name=ext_client_provider_name
            )
        else:
            logger.error("No valid action specified. Use --action deploy to execute the deployment.")
            sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
