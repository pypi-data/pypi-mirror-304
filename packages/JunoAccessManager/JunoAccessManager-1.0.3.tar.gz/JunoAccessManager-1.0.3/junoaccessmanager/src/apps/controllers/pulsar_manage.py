import requests
# from jose import jwt
import jwt
from typing import List
from junoaccessmanager.src.settings import settings
from junoaccessmanager.src.apps.models.permission import TopicActions
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

headers = {
    'Authorization': f'Bearer {settings.PULSAR_ADMIN_TOKEN}',
    'Content-Type': 'application/json'
}


def create_mq_token(username: str):
    with open('src/certs/jwt-private.key', 'rb') as key:
        private_key_der = key.read()
        private_key = serialization.load_der_private_key(data=private_key_der, password=None, backend=default_backend())
        # private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())

    payload = {'sub': username}
    header = {'alg': 'RS256', 'typ': None}
    # token = jwt.encode(claims=payload, key=private_key_pem.decode(), headers=header, algorithm='RS256')
    token = jwt.encode(payload=payload, key=private_key, algorithm='RS256', headers=header)
    return token


def get_brokers():
    url = f"{settings.PULSAR_ADMIN_HOST}/brokers"
    response = requests.get(url=url, headers=headers)
    return response


def get_clusters():
    url = f"{settings.PULSAR_ADMIN_HOST}/clusters"
    response = requests.get(url=url, headers=headers)
    return response


def get_tenants():
    url = f"{settings.PULSAR_ADMIN_HOST}/tenants"
    response = requests.get(url=url, headers=headers)
    return response


def get_namespaces(tenant: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}"
    response = requests.get(url=url, headers=headers)
    return response


def get_topics(tenant: str, namespace: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}"
    response = requests.get(url=url, headers=headers)
    return response


def get_roles_in_namespace(tenant: str, namespace: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}/{namespace}/permissions"
    response = requests.get(url=url, headers=headers)
    return response


def get_roles_in_topic(tenant: str, namespace: str, topic: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}/permissions"
    response = requests.get(url=url, headers=headers)
    return response


def create_tenant(clusters: List[str], tenant: str):
    bind_cluster = {'allowedClusters': clusters}
    url = f"{settings.PULSAR_ADMIN_HOST}/tenants/{tenant}"
    response = requests.put(url=url, json=bind_cluster, headers=headers)
    return response


def delete_tenant(tenant: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/tenants/{tenant}"
    response = requests.delete(url=url, headers=headers)
    return response


def create_namespace(tenant: str, namespace: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}/{namespace}"
    response = requests.put(url=url, headers=headers)
    return response


def delete_namespace(tenant: str, namespace: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}/{namespace}"
    response = requests.delete(url=url, headers=headers)
    return response


def create_topic(tenant: str, namespace: str, topic: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}"
    response = requests.put(url=url, headers=headers)
    return response


def delete_topic(tenant: str, namespace: str, topic: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}"
    response = requests.delete(url=url, headers=headers)
    return response


def create_subscription(tenant: str, namespace: str, topic: str, subscription: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}/subscription/{subscription}"
    response = requests.put(url=url, headers=headers)
    return response


def delete_subscription(tenant: str, namespace: str, topic: str, subscription: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}/subscription/{subscription}"
    response = requests.delete(url=url, headers=headers)
    return response


def grant_namespace_permission(tenant: str, namespace: str, role: str, actions: TopicActions):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}/{namespace}/permissions/{role}"
    response = requests.post(url=url, headers=headers, json=actions.value.split('_'))
    return response


# 对于单独给指定角色授权过的topic，就算撤回上层namespace级别的授权，依旧不影响该角色对该topic的访问。
def delete_namespace_permission(tenant: str, namespace: str, role: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/namespaces/{tenant}/{namespace}/permissions/{role}"
    response = requests.delete(url=url, headers=headers)
    return response


def grant_topic_permission(tenant: str, namespace: str, topic: str, role: str, actions: TopicActions):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}/permissions/{role}"
    response = requests.post(url=url, headers=headers, json=actions.value.split('_'))
    return response


def delete_topic_permission(tenant: str, namespace: str, topic: str, role: str):
    url = f"{settings.PULSAR_ADMIN_HOST}/persistent/{tenant}/{namespace}/{topic}/permissions/{role}"
    response = requests.delete(url=url, headers=headers)
    return response
