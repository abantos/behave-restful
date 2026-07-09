import json

from assertpy import assert_that
from behave import *


@given('a test session')
def step_impl(context):
    context.session = SessionDouble()


@given('a test response')
def step_impl(context):
    context.response = ResponseDouble()


@given('a response status of {status}')
def step_impl(context, status):
    context.response.status_code = int(status)


@given('the response contains a json body like')
def step_impl(context):
    json_body = json.loads(context.text)
    context.response.json_payload = json_body


@given('the response contains headers like')
def step_impl(context):
    json_body = json.loads(context.text)
    context.response.headers = json_body


@then('the context request url is equal to {expected_url}')
def step_impl(context, expected_url):
    assert_that(context.request_url).is_equal_to(expected_url)


@then('the context request json payload is equal to')
def step_impl(context):
    expected_payload = json.loads(context.text)
    assert_that(context.request_json_payload).is_equal_to(expected_payload)


@then('the context contains request form-data text {key} with value set to {value}')
def step_impl(context, key, value):
    assert_that(context.request_form_data_payload[key]).is_equal_to(value)


@then('the context contains request form-data file {key} with value set to {value}')
def step_impl(context, key, value):
    assert_that(context.request_files[key]).is_equal_to(value)


@then('the session {name} property is {value}')
def step_impl(context, name, value):
    expected_value = eval(value)
    actual_value = getattr(context.session, name)
    assert_that(actual_value).is_equal_to(expected_value)


@then('the context contains param {param} with value set to {value}')
def step_impl(context, param, value):
    assert_that(context.request_params.get(param)).is_equal_to(value)


@then('the context contains header {header} with value set to {value}')
def step_impl(context, header, value):
    assert_that(context.request_headers.get(header)).is_equal_to(value)



class SessionDouble(object):
    def __init__(self):
        self.response = None
        self.get_invoked = False
        self.post_invoked = False
        self.put_invoked = False
        self.patch_invoked = False
        self.delete_invoked = False
        self.request_url = None
        self.request_params = None
        self.request_data = None
        self.request_json = None
        self.request_kwargs = None


    def get(self, url, params=None, **kwargs):
        self.get_invoked = True
        self.request_url = url
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


    def post(self, url, data=None, json=None, **kwargs):
        self.post_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_json = json
        self.request_kwargs = kwargs
        return self.response


    def put(self, url, data=None, **kwargs):
        self.put_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_kwargs = kwargs
        return self.response


    def patch(self, url, data=None, json=None, **kwargs):
        self.patch_invoked = True
        self.request_url = url
        self.request_data = data
        self.request_json = json
        self.request_kwargs = kwargs
        return self.response


    def delete(self, url, **kwargs):
        self.delete_invoked = True
        self.request_url = url
        self.request_kwargs = kwargs
        return self.response



class ResponseDouble(object):
    def __init__(self):
        self.status_code = 200
        self.json_payload = None
        self.headers = None


    def json(self):
        if self.json_payload: return self.json_payload
        raise ValueError('No JSON object could be decoded')