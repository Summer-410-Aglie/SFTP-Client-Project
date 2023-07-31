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
        self.mock_os = MagicMock()
        self.sftp_client.rename = self.mock_os_rename
        pass

    def test_renameLocal_success(self):
        src_name = 'file_name'
        dest_name = 'new_file_name'

        self.mock_connection.rename.return_value = True

        result = self.sftp_client.renameLocal(src_name, dest_name)

        self.assertTrue(result)

    def test_renameLocal_error(self):
        src_name = 'file_name'
        dest_name = 'new_file_name'

        self.mock_connection.rename.side_effect = FileNotFoundError(src_name + ' does not exist')

        result = self.sftp_client.renameLocal(src_name, dest_name)

        self.assertEqual(str(result), src_name + ' does not exist')

if __name__ == "__main__":
    unittest.main()
