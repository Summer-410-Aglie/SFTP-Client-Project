import unittest
from unittest.mock import MagicMock
from src.sftp_client import SFTPClient
import pysftp

class SFTPClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.host_name: str = "example.com"
        self.user_name: str = "username"
        self.password: str = "password"
        self.sftp_client: SFTPClient = SFTPClient(self.host_name, self.user_name, self.password)
        self.mock_connection = MagicMock()
        self.sftp_client.connection = self.mock_connection
        pass

    def test_renameRemote_rename_success(self):
        src_name = 'file_exist'
        dest_name = 'new_test_name'

        self.mock_connection.rename.return_value = None

        result = self.sftp_client.renameRemote(src_name, dest_name)

        self.assertTrue(result)

    def test_renameRemote_error(self):
        src_name = 'file_exist'
        dest_name = 'new_test_name'

        self.mock_connection.rename.side_effect = IOError('Unable to rename file or directory: ' + src_name + ' to: ' + dest_name)

        result = self.sftp_client.renameRemote(src_name, dest_name)

        self.assertEqual(str(result), 'Unable to rename file or directory: ' + src_name + ' to: ' + dest_name)    


if __name__ == "__main__":
    unittest.main()
