import unittest

from assertpy import assert_that, fail

import behave_restful._definitions as _definitions
import behave_restful._lang_imp.request_builder as _builder


class TestBuilderInterface(unittest.TestCase):

    def setUp(self):
        super(TestBuilderInterface, self).setUp()
        self.vars = {
            'BASE_URL': 'http://server.com',
            'resource': 'resource',
            'OBJECT_ID': 5,
            'OBJECT_NAME': 'resolved name',
            'PARAM1': 'resolved_param1',
            'PARAM2': 'resolved_param2',
            'FILE_PATH': 'data/resolved_file.txt'
        }
        self.vars_manager = _definitions.VarsManager()
        self.vars_manager.add_vars(self.vars)
        self.context = ContextDouble()
        self.context.vars = self.vars_manager


    def test_should_set_url_in_context(self):
        url = 'http://a/url'
        _builder.set_url(self.context, url)
        assert_that(self.context.request_url).is_equal_to(url)


    def test_embedded_variables_in_url_are_resolved(self):
        _builder.set_url(self.context, '${BASE_URL}/a/${resource}')
        assert_that(self.context.request_url).is_equal_to('http://server.com/a/resource')


    def test_should_set_payload_in_context(self):
        payload = """
        {
            "id": 1,
            "name": "an object"
        }
        """
        expected_payload = {
            'id': 1,
            'name': 'an object'
        }
        _builder.set_json_payload(self.context, payload)
        assert_that(self.context.request_json_payload).is_equal_to(expected_payload)


    def test_embedded_variables_in_payload_are_resolved(self):
        payload = """
        {
            "id": ${OBJECT_ID},
            "name": "${OBJECT_NAME}"
        }
        """
        expected_payload = {
            'id': 5,
            'name': 'resolved name'
        }
        _builder.set_json_payload(self.context, payload)
        assert_that(self.context.request_json_payload).is_equal_to(expected_payload)


    def test_request_parameters_are_set_in_context(self):
        actual_params = TableDouble()
        expected_params = {'id': '4',
                            'name': 'foo_bar'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)


    def test_request_parameter_values_are_resolved(self):
        actual_params = TableDouble(resolve_values=True)
        expected_params = {'id': '5',
                           'name': 'resolved name'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)


    def test_request_parameter_names_are_resolved(self):
        actual_params = TableDouble(resolve_names=True)
        expected_params = {'resolved_param1': 'foo',
                           'resolved_param2': 'bar'}
        _builder.set_request_params(self.context, actual_params)
        assert_that(self.context.request_params).is_equal_to(expected_params)

        
    def test_request_headers_are_set_in_context(self):
        actual_headers = TableDouble()
        expected_headers = {'id': '4',
                            'name': 'foo_bar'}
        _builder.set_request_headers(self.context, actual_headers)
        assert_that(self.context.request_headers).is_equal_to(expected_headers)


    def test_request_header_values_are_resolved(self):
        actual_headers = TableDouble(resolve_values=True)
        expected_headers = {'id': '5',
                           'name': 'resolved name'}
        _builder.set_request_headers(self.context, actual_headers)
        assert_that(self.context.request_headers).is_equal_to(expected_headers)


    def test_request_header_names_are_resolved(self):
        actual_headers = TableDouble(resolve_names=True)
        expected_headers = {'resolved_param1': 'foo',
                           'resolved_param2': 'bar'}
        _builder.set_request_headers(self.context, actual_headers)
        assert_that(self.context.request_headers).is_equal_to(expected_headers)


    def test_form_data_fields_are_set_in_context(self):
        actual_form_data = FormDataTableDouble()
        expected_form_data = {'description': 'a file'}
        _builder.set_form_data(self.context, actual_form_data)
        assert_that(self.context.request_form_data).is_equal_to(expected_form_data)


    def test_form_data_file_fields_are_set_in_context(self):
        actual_form_data = FormDataTableDouble()
        expected_files = {'attachment': 'data/a_file.txt'}
        _builder.set_form_data(self.context, actual_form_data)
        assert_that(self.context.request_files).is_equal_to(expected_files)


    def test_form_data_values_are_resolved(self):
        actual_form_data = FormDataTableDouble(resolve_values=True)
        _builder.set_form_data(self.context, actual_form_data)
        assert_that(self.context.request_form_data).is_equal_to({'description': 'resolved name'})
        assert_that(self.context.request_files).is_equal_to({'attachment': 'data/resolved_file.txt'})


    def test_form_data_names_are_resolved(self):
        actual_form_data = FormDataTableDouble(resolve_names=True)
        _builder.set_form_data(self.context, actual_form_data)
        assert_that(self.context.request_form_data).is_equal_to({'resolved_param1': 'foo'})
        assert_that(self.context.request_files).is_equal_to({'resolved_param2': 'data/a_file.txt'})


    def test_form_data_files_are_empty_when_no_file_fields(self):
        actual_form_data = FormDataTableDouble(text_only=True)
        _builder.set_form_data(self.context, actual_form_data)
        assert_that(self.context.request_form_data).is_equal_to({'description': 'a file'})
        assert_that(self.context.request_files).is_equal_to({})


class ContextDouble(object):
    pass




class TableDouble(object):

    def __init__(self, resolve_values=False, resolve_names=False):
        self.resolve_values = resolve_values
        self.resolve_names = resolve_names

    def __iter__(self):
        if self.resolve_values:
            yield {'param': 'id',
                   'value': '${OBJECT_ID}'}
            yield {'param': 'name',
                   'value': '${OBJECT_NAME}'}

        elif self.resolve_names:
            yield {'param': '${PARAM1}',
                   'value': 'foo'}
            yield {'param': '${PARAM2}',
                   'value': 'bar'}
                   
        else:
            yield {'param': 'id',
                   'value': '4'}
            yield {'param': 'name',
                   'value': 'foo_bar'}


class FormDataTableDouble(object):
    def __init__(self, resolve_values=False, resolve_names=False, text_only=False):
        self.resolve_values = resolve_values
        self.resolve_names = resolve_names
        self.text_only = text_only

    def __iter__(self):
        if self.resolve_values:
            yield {'param': 'description',
                   'value': '${OBJECT_NAME}',
                   'type': 'text'}
            yield {'param': 'attachment',
                   'value': '${FILE_PATH}',
                   'type': 'file'}

        elif self.resolve_names:
            yield {'param': '${PARAM1}',
                   'value': 'foo',
                   'type': 'text'}
            yield {'param': '${PARAM2}',
                   'value': 'data/a_file.txt',
                   'type': 'file'}

        elif self.text_only:
            yield {'param': 'description',
                   'value': 'a file',
                   'type': 'text'}

        else:
            yield {'param': 'description',
                   'value': 'a file',
                   'type': 'text'}
            yield {'param': 'attachment',
                   'value': 'data/a_file.txt',
                   'type': 'file'}


if __name__=="__main__":
    unittest.main()