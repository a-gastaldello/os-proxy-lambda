from flask import request, Response
from os import environ
import logging
import requests
from datetime import datetime, timezone
from json import dumps

OPENSEARCH_HOST = environ.get("OPENSEARCH_HOST", "http://localhost:9200")

logger = logging.getLogger(__name__)


def _log_apache_format(response: Response):
    remote_addr = request.remote_addr or "-"
    user_ident = "-"
    user_auth = "-"
    now = datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S +0000")
    method = request.method
    full_path = request.full_path.rstrip("?")
    protocol = request.environ.get("SERVER_PROTOCOL", "HTTP/1.1")
    status_code = response.status_code
    content_length = response.headers.get("Content-Length", "-")
    referer = request.headers.get("Referer", "-")
    user_agent = request.headers.get("User-Agent", "-")

    log_entry = (
        f"{remote_addr} {user_ident} {user_auth} [{now}] "
        f'"{method} {full_path} {protocol}" {status_code} {content_length} '
        f'"{referer}" "{user_agent}"'
    )

    logger.info(log_entry)


def proxy_request(path: str):
    method = request.method
    url = f"{OPENSEARCH_HOST}/{path}"

    headers = {key: value for key, value in request.headers if key != "Host"}
    data = request.get_data()
    params = request.args

    try:
        resp = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
            cookies=request.cookies,
            allow_redirects=False,
        )
        excluded_headers = [
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        ]
        response_headers = [
            (name, value)
            for (name, value) in resp.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        proxy_response = Response(resp.content, resp.status_code, response_headers)

        if resp.headers.get("Content-Type", "").startswith("application/json"):
            try:
                json_content = resp.json()
                logger.debug(f"JSON Response: {dumps(json_content)}")
            except ValueError:
                logger.error("Failed to parse JSON response")

        _log_apache_format(proxy_response)

        return proxy_response
    except requests.RequestException as e:
        error_response = Response(f"Error forwarding request: {str(e)}", status=500)
        _log_apache_format(error_response)
        return error_response
