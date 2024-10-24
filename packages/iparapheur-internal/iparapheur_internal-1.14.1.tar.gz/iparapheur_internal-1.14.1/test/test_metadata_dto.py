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

from iparapheur_internal.models.metadata_dto import MetadataDto

class TestMetadataDto(unittest.TestCase):
    """MetadataDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MetadataDto:
        """Test MetadataDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MetadataDto`
        """
        model = MetadataDto()
        if include_optional:
            return MetadataDto(
                id = '',
                name = 'Example metadata',
                key = 'example_metadata',
                index = 56,
                type = 'TEXT',
                restricted_values = [
                    ''
                    ]
            )
        else:
            return MetadataDto(
                name = 'Example metadata',
                key = 'example_metadata',
        )
        """

    def testMetadataDto(self):
        """Test MetadataDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
