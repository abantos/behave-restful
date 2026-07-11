import os
import tempfile
import unittest

from assertpy import assert_that

import behave_restful._lang_imp.request_invoker as _invoker


class TestRequestInvokerInterface(unittest.TestCase):
    def setUp(self):
        super(TestRequestInvokerInterface, self).setUp()
        self.response = ResponseDouble()
        self.session = SessionDouble()
        self.session.response = self.response
        self.context = ContextDouble()
        self.context.session = self.session
        self.context.request_url = "http://my.server.com/resource"
        self.context.request_json_payload = {"id": 12, "name": "a name"}
        self.context.request_params = {"foo": 56, "bar": "baz"}
        self.context.request_headers = {"foo": 56, "bar": "baz"}

    # send_get()
    def test_invokes_get_on_session(self):
        _invoker.send_get(self.context)
        assert_that(self.session.get_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_get_stores_response_in_context(self):
        _invoker.send_get(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    def test_get_request_includes_params(self):
        _invoker.send_get(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_get_request_includes_headers(self):
        _invoker.send_get(self.context)
        assert_that(self.session.request_headers).is_same_as(
            self.context.request_headers
        )

    # send_post()
    def test_invokes_post_on_session(self):
        _invoker.send_post(self.context)
        assert_that(self.session.post_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_invokes_post_with_json_payload(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_json).is_equal_to(
            self.context.request_json_payload
        )

    def test_post_stores_response_in_context(self):
        _invoker.send_post(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    def test_post_request_includes_params(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_post_request_includes_headers(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_headers).is_same_as(
            self.context.request_headers
        )

    # send_put()
    def test_invokes_put_on_session(self):
        _invoker.send_put(self.context)
        assert_that(self.session.put_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_invokes_put_with_json_payload(self):
        _invoker.send_put(self.context)
        expected_payload = self.session.request_kwargs.get("json")
        assert_that(expected_payload).is_equal_to(self.context.request_json_payload)

    def test_put_stores_response_in_context(self):
        _invoker.send_put(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    def test_put_request_includes_params(self):
        _invoker.send_put(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_put_request_includes_headers(self):
        _invoker.send_put(self.context)
        assert_that(self.session.request_headers).is_same_as(
            self.context.request_headers
        )

    # send_patch()
    def test_invokes_patch_on_session(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.patch_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_invokes_patch_with_json_payload(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.request_json).is_equal_to(
            self.context.request_json_payload
        )

    def test_patch_request_includes_params(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_patch_request_includes_headers(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.request_headers).is_same_as(
            self.context.request_headers
        )

    def test_patch_stores_response_in_context(self):
        _invoker.send_patch(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    # send_delete()
    def test_invokes_delete_on_session(self):
        _invoker.send_delete(self.context)
        assert_that(self.session.delete_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_delete_stores_response_in_context(self):
        _invoker.send_delete(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    def test_delete_request_includes_params(self):
        _invoker.send_delete(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_delete_request_includes_headers(self):
        _invoker.send_delete(self.context)
        assert_that(self.session.request_headers).is_same_as(
            self.context.request_headers
        )


class TestRequestInvokerFileUpload(unittest.TestCase):
    def setUp(self):
        super(TestRequestInvokerFileUpload, self).setUp()
        self.response = ResponseDouble()
        self.session = SessionDouble()
        self.session.response = self.response
        self.context = ContextDouble()
        self.context.session = self.session
        self.context.request_url = "http://my.server.com/resource"
        self.context.request_params = {"foo": 56, "bar": "baz"}
        self.context.request_headers = {"baz": 57, "qux": "quux"}
        self.file_path = self._create_temp_file(suffix=".txt")
        self.context.request_files = {"attachment": self.file_path}
        self.context.request_form_data_payload = {"description": "a file"}

    def _create_temp_file(self, suffix):
        handle, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(handle, "wb") as f: f.write(b"file content")
        self.addCleanup(os.remove, path)
        return path

    def _sent_file(self, field="attachment"):
        return self.session.request_files[field]

    # send_post()
    def test_invokes_post_on_session(self):
        _invoker.send_post(self.context)
        assert_that(self.session.post_invoked).is_true()
        assert_that(self.session.request_url).is_equal_to(self.context.request_url)

    def test_post_stores_response_in_context(self):
        _invoker.send_post(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    def test_post_request_includes_params(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_params).is_same_as(self.context.request_params)

    def test_post_request_includes_headers(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_headers).is_same_as(self.context.request_headers)

    def test_sends_file_with_name_and_content_type(self):
        _invoker.send_post(self.context)
        file_name, file_object, content_type = self._sent_file()
        assert_that(file_name).is_equal_to(os.path.basename(self.file_path))
        assert_that(file_object.name).is_equal_to(self.file_path)
        assert_that(content_type).is_equal_to("text/plain")

    def test_defaults_content_type_when_it_cannot_be_guessed(self):
        path = self._create_temp_file(suffix=".unknown")
        self.context.request_files = {"attachment": path}
        _invoker.send_post(self.context)
        _, _, content_type = self._sent_file()
        assert_that(content_type).is_equal_to("application/octet-stream")

    def test_sends_form_data_with_files(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_data).is_same_as(self.context.request_form_data_payload)

    def test_form_data_is_optional(self):
        del self.context.request_form_data_payload
        _invoker.send_post(self.context)
        assert_that(self.session.request_data).is_none()

    def test_does_not_send_json_payload_with_files(self):
        _invoker.send_post(self.context)
        assert_that(self.session.request_json).is_none()

    def test_closes_files_after_request(self):
        _invoker.send_post(self.context)
        _, file_object, _ = self._sent_file()
        assert_that(file_object.closed).is_true()

    # send_put()
    def test_invokes_put_with_files(self):
        _invoker.send_put(self.context)
        assert_that(self.session.put_invoked).is_true()
        file_name, _, content_type = self._sent_file()
        assert_that(file_name).is_equal_to(os.path.basename(self.file_path))
        assert_that(content_type).is_equal_to("text/plain")
        assert_that(self.session.request_data).is_same_as(self.context.request_form_data_payload)

    def test_put_stores_response_in_context(self):
        _invoker.send_put(self.context)
        assert_that(self.context.response).is_same_as(self.response)

    # send_patch()
    def test_invokes_patch_with_files(self):
        _invoker.send_patch(self.context)
        assert_that(self.session.patch_invoked).is_true()
        file_name, _, content_type = self._sent_file()
        assert_that(file_name).is_equal_to(os.path.basename(self.file_path))
        assert_that(content_type).is_equal_to("text/plain")
        assert_that(self.session.request_data).is_same_as(self.context.request_form_data_payload)

    def test_patch_stores_response_in_context(self):
        _invoker.send_patch(self.context)
        assert_that(self.context.response).is_same_as(self.response)


class SessionDouble(object):
    def __init__(self):
        self.response = None
        self.get_invoked = False
        self.post_invoked = False
        self.put_invoked = False
        self.patch_invoked = False
        self.delete_invoked = False
        self.request_url = None
        self.request_headers = None
        self.request_params = None
        self.request_data = None
        self.request_json = None
        self.request_files = None
        self.request_kwargs = None

    def get(self, url, params=None, headers=None, **kwargs):
        self.get_invoked = True
        self.request_url = url
        self.request_headers = headers
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response

    def post(self, url, data=None, json=None, params=None, headers=None, files=None, **kwargs):
        self.post_invoked = True
        self.request_url = url
        self.request_headers = headers
        self.request_data = data
        self.request_json = json
        self.request_params = params
        self.request_files = files
        self.request_kwargs = kwargs
        return self.response

    def put(self, url, data=None, params=None, headers=None, files=None, **kwargs):
        self.put_invoked = True
        self.request_url = url
        self.request_headers = headers
        self.request_data = data
        self.request_params = params
        self.request_files = files
        self.request_kwargs = kwargs
        return self.response

    def patch(self, url, data=None, json=None, params=None, headers=None, files=None, **kwargs):
        self.patch_invoked = True
        self.request_url = url
        self.request_headers = headers
        self.request_data = data
        self.request_json = json
        self.request_params = params
        self.request_files = files
        self.request_kwargs = kwargs
        return self.response

    def delete(self, url, params=None, headers=None, **kwargs):
        self.delete_invoked = True
        self.request_url = url
        self.request_headers = headers
        self.request_params = params
        self.request_kwargs = kwargs
        return self.response


class ResponseDouble(object):
    pass


class ContextDouble(object):
    pass


if __name__ == "__main__":
    unittest.main()