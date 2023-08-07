import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from src.sftp_client import SFTPClient
import pysftp

class SFTPClientTest(unittest.TestCase):
    def setUp(self) -> None:
        self.host_name: str = "example.com"
        self.user_name: str = "username"
        self.password: str = "password"
        self.sftp_client: SFTPClient = SFTPClient(self.host_name, self.user_name, self.password)
        pass

    def test_renameLocal_success(self):
        src_name = 'file_name'
        dest_name = 'new_file_name'

        with patch('os.rename') as mock_rename:
            
            result = self.sftp_client.renameLocal(src_name, dest_name)
            
            self.assertTrue(result)

            mock_rename.assert_called_once_with(src_name, dest_name)


    def test_renameLocal_error(self):
        src_name = 'file_name'
        dest_name = 'new_file_name'

        with patch('os.rename') as mock_rename:

            mock_rename.side_effect = FileNotFoundError(f"{src_name} does not exist")

            result = self.sftp_client.renameLocal(src_name, dest_name)

            self.assertEqual(str(result), f"{src_name} does not exist")
            mock_rename.assert_called_once_with(src_name, dest_name)

if __name__ == "__main__":
    unittest.main()
