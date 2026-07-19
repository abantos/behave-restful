"""
"""
import json

def set_url(context, url):
    """
    """
    resolved_url = context.vars.resolve(url)
    context.request_url = resolved_url


def set_json_payload(context, payload):
    """
    """
    resolved_payload = context.vars.resolve(payload)
    context.request_json_payload = json.loads(resolved_payload)


def set_request_params(context, params):
    """
    """
    resolve = context.vars.resolve
    resolved_params = {resolve(param['param']): resolve(param['value']) for param in params}
    context.request_params = resolved_params

def set_request_headers(context, headers):
    """
    """
    resolve = context.vars.resolve
    resolved_headers = {resolve(header['param']): resolve(header['value']) for header in headers}
    context.request_headers = resolved_headers

def set_form_data_payload(context, table):
    """
    """
    resolve = context.vars.resolve
    data = {}
    files = {}
    for row in table:
        name = resolve(row["key"])
        value = resolve(row["value"])
        if row["type"] == "file": files[name] = value
        else: data[name] = value
    context.request_form_data_payload = data
    context.request_files = files