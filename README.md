# Behave Restful

[![build](https://github.com/abantos/behave-restful/actions/workflows/python-verify-library.yml/badge.svg)](https://github.com/abantos/behave-restful/actions/workflows/python-verify-library.yml)

Behave Restful is a Behavior Driven Development (BDD) framework based on
[behave](https://pythonhosted.org/behave/), that implements a language suitable
to test and validate REST APIs and Services. It leverages the power of the
[gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin) language to write
business readable tests that validate the behavior of REST APIs.

Although, Behave Restful is implemented in [python](http://www.python.org) and
uses [behave](https://pythonhosted.org/behave/) as underlying framework, it can
test services implemented in any language as easy as:

```gherkin

Feature: API to add a new book to our collection
    As a user, I want to add a new book to my "to-read" collection.

    Scenario: Add a new book to collection.
        Given a request url http://my.reads/api/books
            And a request json payload
                """
                {
                    "category": "reference",
                    "author": "Nigel Rees",
                    "title": "Sayings of the Century",
                    "price": 8.95,
                    "status": "to-read"
                }
                """
        When the request sends POST
        Then the response status is CREATED
            And the response json matches
                """
                {
                    "title": "BookObject",
                    "type": "object"
                    "properties": {
                        "id": {"type": "number"},
                        "category": {"type": "string"},
                        "author": {"type": "string"},
                        "title": {"type": "string"},
                        "price": {"type": "number"},
                        "status": {"type": "string", "enum": ["to-read", "reading", "read"]}
                    },
                    "required": ["id", "category", "title"]
                }
                """
            And the response json at $.id is equal to 100
            And the response json at $.category is equal to "reference"
            And the response json at $.title is equal to "Sayings of the Century"
```


As you can see in the example, we send a POST request to the specified url with
a JSON payload, and we can validate the result very easy. First, we verify that
the status of the response is CREATED (it succeeds). Then we validate the
response JSON body using the expected [JSON Schema](http://json-schema.org/).
Finally, we validate specific values in the response using
[JSONPath](http://goessner.net/articles/JsonPath/)

## Installation

Use pip to install behave-restful in your project

```
pip install behave-restful
```

## Setup

To add support for `behave-restful` steps in your `.feature` files, you need to include behave-restful's environment and step definitions.

You can do this simply by adding two boilerplate files to your project:

In the root of your `features` directory, add this `environment.py` file:

```python
# {your_project}/features/en/__init__.py

import os

import behave_restful.app as br_app


def before_all(context):
    this_directory = os.path.abspath(os.path.dirname(__file__))
    br_app.BehaveRestfulApp().initialize_context(context, this_directory)
    context.hooks.invoke(br_app.BEFORE_ALL, context)


def after_all(context):
    context.hooks.invoke(br_app.AFTER_ALL, context)


def before_feature(context, feature):
    context.hooks.invoke(br_app.BEFORE_FEATURE, context, feature)


def after_feature(context, feature):
    context.hooks.invoke(br_app.AFTER_FEATURE, context, feature)


def before_scenario(context, scenario):
    context.hooks.invoke(br_app.BEFORE_SCENARIO, context, scenario)


def after_scenario(context, scenario):
    context.hooks.invoke(br_app.AFTER_SCENARIO, context, scenario)


def before_step(context, step):
    context.hooks.invoke(br_app.BEFORE_STEP, context, step)


def after_step(context, step):
    context.hooks.invoke(br_app.AFTER_STEP, context, step)


def before_tag(context, tag):
    context.hooks.invoke(br_app.BEFORE_TAG, context, tag)


def after_tag(context, tag):
    context.hooks.invoke(br_app.AFTER_TAG, context, tag)
```

And under `features/steps` add this `__init__.py` file:

```python
# {your_project}/features/steps/__init__.py
from behave_restful.lang import *
```