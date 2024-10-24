# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from iparapheur_internal.api.document_api import DocumentApi


class TestDocumentApi(unittest.TestCase):
    """DocumentApi unit test stubs"""

    def setUp(self) -> None:
        self.api = DocumentApi()

    def tearDown(self) -> None:
        pass

    def test_create_annotation(self) -> None:
        """Test case for create_annotation

        Creates a PDF annotation
        """
        pass

    def test_create_signature_placement_annotation(self) -> None:
        """Test case for create_signature_placement_annotation

        Creates a signature placement annotation
        """
        pass

    def test_delete_annotation(self) -> None:
        """Test case for delete_annotation

        Deletes the given PDF annotation
        """
        pass

    def test_get_signature_placement_annotations(self) -> None:
        """Test case for get_signature_placement_annotations

        Get all signaturePlacement Annotations of a document
        """
        pass


if __name__ == '__main__':
    unittest.main()
