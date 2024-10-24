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

from iparapheur_internal.models.mail_params import MailParams

class TestMailParams(unittest.TestCase):
    """MailParams unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MailParams:
        """Test MailParams
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MailParams`
        """
        model = MailParams()
        if include_optional:
            return MailParams(
                public_annotation = '',
                private_annotation = '',
                metadata = {
                    'key' : ''
                    },
                to = [
                    ''
                    ],
                cc = [
                    ''
                    ],
                bcc = [
                    ''
                    ],
                object = '',
                message = '',
                password = '',
                payload = '',
                include_docket = True
            )
        else:
            return MailParams(
                to = [
                    ''
                    ],
                object = '',
        )
        """

    def testMailParams(self):
        """Test MailParams"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
