from flask import request
from json import dumps
from proxy import proxy_request


def _patch_cluster_operating_system_name(body):
    for name in body.get("nodes", {}).get("os", {}).get("names", []):
        if name.get("name") is None:
            name["name"] = "Linux"
        if name.get("count") is None:
            name["count"] = 1
    return body


def _patch_cluster_operating_system_pretty_name(body):
    for name in body.get("nodes", {}).get("os", {}).get("pretty_names", []):
        if name.get("pretty_name") is None:
            name["pretty_name"] = "Amazon Linux 2023.6.20250211"
        if name.get("count") is None:
            name["count"] = 1
    return body


def _patch_cluster_jvm_versions(body):
    jvm = body.get("nodes", {}).get("jvm", {})
    if jvm.get("versions") is None:
        jvm["versions"] = [
            {
                "version": "21.0.6",
                "vm_name": "OpenJDK 64-Bit Server VM",
                "vm_version": "21.0.6+7-LTS",
                "vm_vendor": "Eclipse Adoptium",
                "bundled_jdk": True,
                "using_bundled_jdk": True,
                "count": 1,
            }
        ]
    return body


def _patch_cluster_nodes_plugins(body):
    nodes = body.get("nodes")
    if nodes.get("plugins") is None:
        nodes["plugins"] = []
    return body


def patch_stats_request():
    original_response = proxy_request(request.full_path)
    if original_response.status_code == 200:
        body = original_response.get_json()
        body = _patch_cluster_operating_system_name(body)
        body = _patch_cluster_operating_system_pretty_name(body)
        body = _patch_cluster_jvm_versions(body)
        body = _patch_cluster_nodes_plugins(body)
        original_response.set_data(dumps(body))
    return original_response


def _patch_node_operating_system_info(body):
    for node in body.get("nodes", {}).values():
        os_info = node.get("os", {})
        if os_info.get("name") is None:
            os_info["name"] = "Linux"
        if os_info.get("pretty_name") is None:
            os_info["pretty_name"] = "Amazon Linux 2023.6.20250211"
        if os_info.get("version") is None:
            os_info["version"] = "5.10.147-149.657.amzn2023.x86_64"
        if os_info.get("arch") is None:
            os_info["arch"] = "amd64"
    return body


def patch_info_request():
    original_response = proxy_request(request.full_path)
    if original_response.status_code == 200:
        body = original_response.get_json()
        body = _patch_node_operating_system_info(body)
        original_response.set_data(dumps(body))
    return original_response
