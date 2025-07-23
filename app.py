from flask import Flask
import logging
import serverless_wsgi
from patch import patch_info_request, patch_stats_request
from proxy import proxy_request
from dotenv import load_dotenv

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)


@app.route("/_cluster/stats", methods=["GET"])
def cluster_stats():
    return patch_stats_request()


@app.route("/_cluster/stats/nodes/<node_id>", methods=["GET"])
def cluster_stats_nodes_nodeid(node_id: str):
    return patch_stats_request()


@app.route("/_nodes", methods=["GET"])
def nodes():
    return patch_info_request()


@app.route("/_nodes/<node_id_or_metric>", methods=["GET"])
def nodes_nodeidormetric(node_id_or_metric: str):
    return patch_info_request()


@app.route("/_nodes/<node_id>/<metric>", methods=["GET"])
def nodes_nodeid_metric(node_id: str, metric: str):
    return patch_info_request()


@app.route(
    "/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
)
def proxy(path: str):
    return proxy_request(path)


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)


if __name__ == "__main__":
    app.run(debug=True)
