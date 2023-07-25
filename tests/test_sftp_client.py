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

    def test_RemoveRemoteDir_dir_exist(self):
        dir = 'directory'
        self.mock_connection.rmdir.return_value = None

        result = self.sftp_client.removeRemoteDirectory(dir) 

        self.assertTrue(result)    

    def test_RemoveRemoteDir_dir_does_not_exist(self):
        dir = 'directory_does_not_exist'
        self.mock_connection.rmdir.side_effect = IOError('Unable to directory: ' + dir)
        result = self.sftp_client.removeRemoteDirectory(dir) 

        self.assertEqual(str(result), 'Unable to remove directory: ' + dir)

if __name__ == "__main__":
    unittest.main()
