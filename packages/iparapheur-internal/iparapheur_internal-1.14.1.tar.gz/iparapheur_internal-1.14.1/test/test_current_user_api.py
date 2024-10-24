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

from iparapheur_internal.api.current_user_api import CurrentUserApi


class TestCurrentUserApi(unittest.TestCase):
    """CurrentUserApi unit test stubs"""

    def setUp(self) -> None:
        self.api = CurrentUserApi()

    def tearDown(self) -> None:
        pass

    def test_delete_table_layout(self) -> None:
        """Test case for delete_table_layout

        Delete tableLayout
        """
        pass

    def test_update_current_user_password(self) -> None:
        """Test case for update_current_user_password

        Update user password
        """
        pass

    def test_update_table_layout(self) -> None:
        """Test case for update_table_layout

        Update tableLayout
        """
        pass


if __name__ == '__main__':
    unittest.main()
