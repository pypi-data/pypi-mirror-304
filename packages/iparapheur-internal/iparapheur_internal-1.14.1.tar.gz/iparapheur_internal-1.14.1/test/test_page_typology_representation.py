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

from iparapheur_internal.models.page_typology_representation import PageTypologyRepresentation

class TestPageTypologyRepresentation(unittest.TestCase):
    """PageTypologyRepresentation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PageTypologyRepresentation:
        """Test PageTypologyRepresentation
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PageTypologyRepresentation`
        """
        model = PageTypologyRepresentation()
        if include_optional:
            return PageTypologyRepresentation(
                total_elements = 56,
                total_pages = 56,
                size = 56,
                content = [
                    iparapheur_internal.models.typology_representation.TypologyRepresentation(
                        id = '', 
                        name = 'jXAuKb%@;_5)#fEb-bx%oZ01', 
                        parent_id = '', 
                        children_count = 56, )
                    ],
                number = 56,
                sort = iparapheur_internal.models.sort_object.SortObject(
                    empty = True, 
                    sorted = True, 
                    unsorted = True, ),
                first = True,
                last = True,
                number_of_elements = 56,
                pageable = iparapheur_internal.models.pageable_object.PageableObject(
                    offset = 56, 
                    sort = iparapheur_internal.models.sort_object.SortObject(
                        empty = True, 
                        sorted = True, 
                        unsorted = True, ), 
                    page_size = 56, 
                    paged = True, 
                    page_number = 56, 
                    unpaged = True, ),
                empty = True
            )
        else:
            return PageTypologyRepresentation(
        )
        """

    def testPageTypologyRepresentation(self):
        """Test PageTypologyRepresentation"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
