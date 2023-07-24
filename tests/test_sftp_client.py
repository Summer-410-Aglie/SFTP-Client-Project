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

    def test_RemoveRemoteFile_file_exist(self):
        file = 'file.txt'
        self.mock_connection.remove.return_value = None

        result = self.sftp_client.removeRemoteFile(file) 

        self.assertTrue(result)    

    def test_RemoveRemoteFile_file_does_not_exist(self):
        file = 'file_does_not_exist.txt'
        self.mock_connection.remove.side_effect = IOError('Unable to remove file: ' + file)
        result = self.sftp_client.removeRemoteFile(file) 

        self.assertEqual(str(result), 'Unable to remove file: ' + file)


if __name__ == "__main__":
    unittest.main()
