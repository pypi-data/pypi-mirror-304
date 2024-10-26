import requests
from typing import Optional, Dict, List
from .entities import Route, SLATier, Policy
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIManager:
    BASE_URL = "https://anypoint.mulesoft.com"

    @staticmethod
    def deploy_api(api_spec_group_id: str, api_spec_asset_id: str, api_spec_version: str):
        logger.info(f"Deploying API: {api_spec_group_id}/{api_spec_asset_id} version {api_spec_version}")
        # Implement API deployment logic here

    @staticmethod
    def configure_policies(policies):
        logger.info("Configuring API policies")
        # Implement policy configuration logic here

    @staticmethod
    def set_sla_tiers(sla_tiers):
        logger.info("Setting SLA tiers")
        # Implement SLA tier configuration logic here

    @staticmethod
    def get_flex_gw_instance_id(access_token: str, bg_id: str, env_id: str, flex_gw_instance_name: str) -> Optional[str]:
        logger.info(f"Getting Flex Gateway Instance ID for: {flex_gw_instance_name}")
        url = f"{APIManager.BASE_URL}/apimanager/xapi/v1/organizations/{bg_id}/environments/{env_id}/flex-gateway-targets"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for target in data:
                if target["name"] == flex_gw_instance_name:
                    return target["id"]
            
            logger.info(f"Flex Gateway Instance '{flex_gw_instance_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting Flex Gateway Instance ID: HTTP {e.response.status_code} - {e.response.text}")
            return None

    @staticmethod
    def get_secret_group_id(access_token: str, bg_id: str, env_id: str, secret_group_name: str) -> Optional[str]:
        logger.info(f"Getting Secret Group ID for: {secret_group_name}")
        url = f"{APIManager.BASE_URL}/apimanager/xapi/proxies/v1/organizations/{bg_id}/environments/{env_id}/secret-groups"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for context in data:
                if context["name"] == secret_group_name:
                    return context["id"]
                
            logger.error(f"Secret Group with name '{secret_group_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting Secret Group ID: HTTP {e.response.status_code} - {e.response.text}")
            return None

    @staticmethod
    def get_tls_context_id(access_token: str, bg_id: str, env_id: str, secret_group_id: str, tls_context_name: str) -> Optional[str]:
        logger.info(f"Getting TLS Context ID for: {tls_context_name}")
        url = f"{APIManager.BASE_URL}/apimanager/xapi/proxies/v1/organizations/{bg_id}/environments/{env_id}/secret-groups/{secret_group_id}/tls-contexts/?type=FlexGateway"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            for context in data:
                if context["name"] == tls_context_name:
                    return context["id"]

            logger.error(f"TLS Context with name '{tls_context_name}' not found")
            return None

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error getting TLS Context ID: HTTP {e.response.status_code} - {e.response.text}")
            return None
        
    @staticmethod
    def create_api_instance(
        access_token: str,
        bg_id: str,
        env_id: str,
        client_provider_id: Optional[str],
        flex_gw_instance_id: str,
        flex_gw_instance_name: str,
        api_spec_group_id: str,
        api_spec_asset_id: str,
        api_spec_version: str,
        listener_port: int,
        listener_basepath: str,
        routes: List[Route]
    ) -> Optional[str]:
        logger.info("Creating API Instance")
        url = f"{APIManager.BASE_URL}/apimanager/xapi/v1/organizations/{bg_id}/environments/{env_id}/apis"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        routing = []
        for route in routes:
            route_data = {
                "upstreams": [],
                "label": route.label,
                "rules": {
                    "methods": "" if route.methods is None else route.methods,
                    "host": "" if route.host is None else route.host,
                    "path": "" if route.path is None else route.path,
                    "headers": "" if route.headers is None else route.headers
                }
            }
            for upstream in route.upstreams:
                upstream_data = {
                    "weight": upstream.weight,
                    "uri": upstream.uri,
                    "label": upstream.label
                }
                if upstream.tls_context:
                    secret_group_id = APIManager.get_secret_group_id(access_token, bg_id, env_id, upstream.tls_context.secret_group_name)
                    tls_context_id = APIManager.get_tls_context_id(access_token, bg_id, env_id, secret_group_id, upstream.tls_context.tls_context_name)
                    upstream_data["tlsContext"] = {
                        "secretGroupId": secret_group_id,
                        "tlsContextId": tls_context_id
                    }
                route_data["upstreams"].append(upstream_data)
            routing.append(route_data)

        payload = {
            "technology": "flexGateway",
            "endpoint": {
                "deploymentType": "HY",
                "type": "raml",
                "proxyUri": f"http://0.0.0.0:{listener_port}{listener_basepath}",
                "tlsContexts": {
                    "inbound": None
                }
            },
            "spec": {
                "groupId": api_spec_group_id,
                "assetId": api_spec_asset_id,
                "version": api_spec_version
            },
            "routing": routing,
            "deployment": {
                "environmentId": env_id,
                "type": "HY",
                "expectedStatus": "undeployed",
                "overwrite": False,
                "targetId": flex_gw_instance_id,
                "targetName": flex_gw_instance_name
            }
        }

        if client_provider_id:
            payload["providerId"] = client_provider_id

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            return data.get("id")

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error creating API Instance: HTTP {e.response.status_code} - {e.response.text}")
            return None

    @staticmethod
    def create_sla_tiers(
        access_token: str,
        bg_id: str,
        env_id: str,
        api_instance_id: str,
        sla_tiers: List[SLATier]
    ) -> List[Optional[str]]:
        logger.info("Creating SLA Tiers")
        url = f"{APIManager.BASE_URL}/apimanager/api/v1/organizations/{bg_id}/environments/{env_id}/apis/{api_instance_id}/tiers"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        tier_ids = []

        for tier in sla_tiers:
            payload = {
                "name": tier.name,
                "description": tier.description,
                "autoApprove": tier.autoapprove,
                "limits": [
                    {
                        "maximumRequests": tier.max_requests,
                        "timePeriodInMilliseconds": tier.timeperiodmillis,
                        "visible": True
                    }
                ],
                "status": "ACTIVE"
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors

                data = response.json()
                tier_ids.append(data.get("id"))
                logger.info(f"Created SLA Tier: {tier.name}")

            except requests.exceptions.HTTPError as e:
                logger.error(f"Error creating SLA Tier '{tier.name}': HTTP {e.response.status_code} - {e.response.text}")
                tier_ids.append(None)

        return tier_ids

    @staticmethod
    def apply_policies(
        access_token: str,
        bg_id: str,
        env_id: str,
        api_instance_id: str,
        policies: List[Policy]
    ) -> List[Optional[str]]:
        logger.info("Applying Policies")
        url = f"{APIManager.BASE_URL}/apimanager/api/v1/organizations/{bg_id}/environments/{env_id}/apis/{api_instance_id}/policies"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "x-anypnt-env-id": env_id,
            "x-anypnt-org-id": bg_id
        }

        policy_ids = []

        for policy in policies:
            payload = {
                "configurationData": policy.configuration_data,
                "groupId": policy.group_id,
                "assetId": policy.asset_id,
                "assetVersion": policy.policy_version
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an exception for HTTP errors

                data = response.json()
                policy_ids.append(data.get("id"))
                logger.info(f"Applied Policy: {policy.asset_id}")

            except requests.exceptions.HTTPError as e:
                logger.error(f"Error applying Policy '{policy.asset_id}': HTTP {e.response.status_code} - {e.response.text}")
                policy_ids.append(None)

        return policy_ids

    @staticmethod
    def deploy_instance(
        access_token: str,
        bg_id: str,
        env_id: str,
        api_instance_id: str,
        flex_gw_instance_id: str,
        flex_gw_instance_name: str
    ) -> bool:
        logger.info(f"Deploying API Instance: {api_instance_id}")
        url = f"{APIManager.BASE_URL}/apimanager/xapi/v1/organizations/{bg_id}/environments/{env_id}/apis/{api_instance_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "deployment": {
                "environmentId": env_id,
                "type": "HY",
                "expectedStatus": "deployed",
                "overwrite": False,
                "targetId": flex_gw_instance_id,
                "targetName": flex_gw_instance_name
            }
        }

        try:
            response = requests.patch(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors

            data = response.json()
            if data["deployment"]["expectedStatus"] == "deployed":
                logger.info(f"API Instance {api_instance_id} deployment initiated successfully")
                return True
            else:
                logger.error(f"Failed to initiate deployment for API Instance {api_instance_id}")
                return False

        except requests.exceptions.HTTPError as e:
            logger.error(f"Error deploying API Instance {api_instance_id}: HTTP {e.response.status_code} - {e.response.text}")
            return False

__all__ = ['APIManager']
