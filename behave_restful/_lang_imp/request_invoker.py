"""
"""
import mimetypes
from contextlib import ExitStack
from pathlib import Path


def send_get(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.get(
        context.request_url,
        headers=headers,
        params=params
    )


def send_post(context):
    """
    """
    _send_with_body(context, context.session.post)


def send_put(context):
    """
    """
    _send_with_body(context, context.session.put)


def send_patch(context):
    """
    """
    _send_with_body(context, context.session.patch)


def send_delete(context):
    """
    """
    headers = _get_request_headers(context)
    params = _get_params(context)
    context.response = context.session.delete(
        context.request_url,
        headers=headers,
        params=params
    )


def _send_with_body(context, method):
    headers = _get_request_headers(context)
    params = _get_params(context)
    if hasattr(context, 'request_files'):
        with ExitStack() as stack:
            context.response = method(
                context.request_url,
                headers=headers,
                params=params,
                data=getattr(context, 'request_form_data_payload', None),
                files=_open_request_files(context, stack),
            )
    else:
        context.response = method(
            context.request_url,
            headers=headers,
            params=params,
            json=context.request_json_payload,
        )


def _open_request_files(context, stack):
    files = {}
    for field, path in context.request_files.items():
        file_object = stack.enter_context(open(path, 'rb'))
        content_type, _ = mimetypes.guess_type(path)
        files[field] = (Path(path).name, file_object, content_type or 'application/octet-stream')
    return files


def _get_params(context):
    return context.request_params if hasattr(context, 'request_params') else None

def _get_request_headers(context):
    return context.request_headers if hasattr(context, 'request_headers') else None
