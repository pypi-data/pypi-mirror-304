from typing import List, Dict, Any, Optional

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TLSContext:
    def __init__(self, secret_group_name: str, tls_context_name: str):
        self.secret_group_name = secret_group_name
        self.tls_context_name = tls_context_name

    def to_dict(self) -> Dict:
        return {
            "secretGroupName": self.secret_group_name,
            "tlsContextName": self.tls_context_name
        }

class Upstream:
    def __init__(self, label: str, uri: str, weight: int, tls_context: Optional[TLSContext] = None):
        self.label = label
        self.uri = uri
        self.weight = weight
        self.tls_context = tls_context

    def to_dict(self) -> Dict:
        return {
            "label": self.label,
            "uri": self.uri,
            "weight": self.weight,
            "tlsContext": self.tls_context.to_dict() if self.tls_context else None
        }

class Route:
    def __init__(self, label: str, upstreams: List[Upstream], methods: Optional[str] = None, 
                 host: Optional[str] = None, path: Optional[str] = None, headers: Optional[Dict] = None):
        self.label = label
        self.upstreams = upstreams
        self.methods = methods
        self.host = host
        self.path = path
        self.headers = headers or {}

    def to_dict(self) -> Dict:
        route_dict = {
            "label": self.label,
            "upstreams": [upstream.to_dict() for upstream in self.upstreams]
        }
        rules = {}
        rules["methods"] = self.methods or ""
        rules["host"] = self.host or ""
        rules["path"] = self.path or ""
        rules["headers"] = self.headers if self.headers else {}
        route_dict["rules"] = rules
        return route_dict

class SLATier:
    def __init__(self, name: str, description: str, autoapprove: bool, max_requests: int, timeperiodmillis: int):
        self.name = name
        self.description = description
        self.autoapprove = autoapprove
        self.max_requests = max_requests
        self.timeperiodmillis = timeperiodmillis

class Policy:
    def __init__(self, group_id: str, asset_id: str, policy_version: str, configuration_data: Dict[str, Any]):
        self.group_id = group_id
        self.asset_id = asset_id
        self.policy_version = policy_version
        self.configuration_data = configuration_data
        
__all__ = ['Route', 'Upstream', 'SLATier', 'Policy']