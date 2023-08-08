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

    def test_removeLocalFile_success(self):
        file_path = 'file_path'

        with patch('os.remove') as mock_remove:

            result = self.sftp_client.removeLocalFile(file_path)

            self.assertTrue(result)

            mock_remove.assert_called_once_with(file_path)

    def test_removeLocalFile_error(self):
        file_path = 'file_path'

        with patch('os.remove') as mock_remove:

            mock_remove.side_effect = OSError('Unable to remove: ' + file_path)

            result = self.sftp_client.removeLocalFile(file_path)

            self.assertEqual(str(result), 'Unable to remove: ' + file_path)

            mock_remove.assert_called_once_with(file_path)

    def test_removeLocalDirectory_success(self):
        file_path = 'directory_path'

        with patch('os.rmdir') as mock_rmdir:

            result = self.sftp_client.removeLocalDirectory(file_path)

            self.assertTrue(result)

            mock_rmdir.assert_called_once_with(file_path)

    def test_removeLocalDirectory_error(self):
        file_path = 'directory_path'

        with patch('os.rmdir') as mock_rmdir:

            mock_rmdir.side_effect = OSError('Unable to remove directory: ' + file_path)

            result = self.sftp_client.removeLocalDirectory(file_path)

            self.assertEqual(str(result), 'Unable to remove directory: ' + file_path)

            mock_rmdir.assert_called_once_with(file_path)

if __name__ == "__main__":
    unittest.main()
