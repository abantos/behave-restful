"""
"""
from behave import *

import behave_restful._lang_imp.request_builder as _builder

@given('a request url {url}')
def step_impl(context, url):
    _builder.set_url(context, url)


@given('a request json payload')
def step_impl(context):
    _builder.set_json_payload(context, context.text)


@given('request headers')
def step_impl(context):
    _builder.set_request_headers(context, context.table)


@given('request parameters')
def step_impl(context):
    _builder.set_request_params(context, context.table)


@given("request form-data")
def step_impl(context):
    _builder.set_form_data(context, context.table)