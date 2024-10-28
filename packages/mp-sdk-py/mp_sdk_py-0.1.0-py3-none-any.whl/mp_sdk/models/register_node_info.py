from dataclasses import dataclass

@dataclass
class RegisterNodeInfo:
    node_id: str
    dev_language: str
    tenant_id: str