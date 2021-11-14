from django.utils.encoding import force_text

from mayan.apps.documents.permissions import (
    permission_document_file_view, permission_document_version_view,
    permission_document_view
)
from mayan.apps.documents.search import (
    document_file_page_search, document_file_search, document_search,
    document_version_page_search, document_version_search
)
from mayan.apps.documents.tests.base import GenericDocumentViewTestCase
from mayan.apps.dynamic_search.tests.mixins import (
    SearchTestMixin, SearchViewTestMixin
)

from ..permissions import permission_document_metadata_view

from .mixins import DocumentMetadataMixin, MetadataTypeTestMixin


class DocumentSearchResultWidgetViewTestCase(
    DocumentMetadataMixin, MetadataTypeTestMixin, SearchViewTestMixin,
    GenericDocumentViewTestCase
):
    _test_search_index_object_name = 'test_document'
    _test_search_model = document_search
    auto_upload_test_document = False

    def setUp(self):
        super().setUp()
        self._create_test_metadata_type(add_test_document_type=True)
        self._upload_test_document()
        self._create_test_document_metadata()
        self._test_object_permission = permission_document_view
        self._test_object_text = self.test_document.label
        self._test_search_model = document_search
        self._test_search_term_data = {'uuid': self.test_document.uuid}

    def test_document_metadata_widget_no_permission(self):
        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text,
            status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_metadata_type_access(self):
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_document_view_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=self._test_object_permission
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_document_metadata_view_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertNotContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_all_document_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_metadata_view_and_document_view_access(self):
        self.grant_access(
            obj=self.test_document, permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertNotContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )

    def test_document_metadata_widget_with_full_access(self):
        self.grant_access(
            obj=self.test_document,
            permission=self._test_object_permission
        )
        self.grant_access(
            obj=self.test_document,
            permission=permission_document_metadata_view
        )
        self.grant_access(
            obj=self.test_metadata_type,
            permission=permission_document_metadata_view
        )

        response = self._request_search_results_view(
            data=self._test_search_term_data, kwargs={
                'search_model_name': self._test_search_model.get_full_name()
            }
        )
        self.assertContains(
            response=response, text=self._test_object_text, status_code=200
        )
        self.assertContains(
            response=response, text=self.test_metadata_type.label,
            status_code=200
        )


class DocumentFileSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    _test_search_index_object_name = 'test_document_file'
    _test_search_model = document_file_search

    def setUp(self):
        super().setUp()
        self._test_object_text = self.test_document_file.filename
        self._test_object_permission = permission_document_file_view
        self._test_search_model = document_file_search
        self._test_search_term_data = {
            'document__uuid': self.test_document.uuid
        }


class DocumentFilePageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    _test_search_index_object_name = 'test_document_file_page'
    _test_search_model = document_file_page_search

    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_file.pages.first())
        self._test_object_permission = permission_document_file_view
        self._test_search_model = document_file_page_search
        self._test_search_term_data = {
            'document_file__document__uuid': self.test_document.uuid
        }


class DocumentVersionSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    _test_search_index_object_name = 'test_document_version'
    _test_search_model = document_version_search

    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_version)
        self._test_object_permission = permission_document_version_view
        self._test_search_model = document_version_search
        self._test_search_term_data = {
            'document__uuid': self.test_document.uuid
        }


class DocumentVersionPageSearchResultWidgetViewTestCase(
    DocumentSearchResultWidgetViewTestCase
):
    _test_search_index_object_name = 'test_document_version_page'
    _test_search_model = document_version_page_search

    def setUp(self):
        super().setUp()
        self._test_object_text = force_text(s=self.test_document_version.pages.first())
        self._test_object_permission = permission_document_version_view
        self._test_search_model = document_version_page_search
        self._test_search_term_data = {
            'document_version__document__uuid': self.test_document.uuid
        }
