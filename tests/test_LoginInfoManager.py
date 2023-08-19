import unittest
import os
import xml.etree.ElementTree as ET
from src.LoginInfoManager import LoginInfoManager

class TestLoginInfoManager(unittest.TestCase):

    TEST_FILE_PATH = "test_connection_profiles.xml"
    
    def setUp(self):
        self.manager = LoginInfoManager(self.TEST_FILE_PATH)
    
    def tearDown(self):
        if os.path.exists(self.TEST_FILE_PATH):
            os.remove(self.TEST_FILE_PATH)
    
    def test_addLoginInfo(self):
        result = self.manager.addLoginInfo("user1", "host1", "password1")
        self.assertTrue(result)
        
        result = self.manager.addLoginInfo("user1", "host1", "password1")
        self.assertFalse(result)

    def test_getAllLoginInfo(self):
        self.manager.addLoginInfo("user1", "host1", "password1")
        self.manager.addLoginInfo("user2", "host2", "password2")

        expected = [
            {"username": "user1", "host": "host1", "password": "password1"},
            {"username": "user2", "host": "host2", "password": "password2"}
        ]

        self.assertEqual(self.manager.getAllLoginInfo(), expected)

    def test_deleteLoginInfo(self):
        self.manager.addLoginInfo("user1", "host1", "password1")
        result = self.manager.deleteLoginInfo({"username": "user1", "host": "host1", "password": "password1"})
        self.assertTrue(result)

        result = self.manager.deleteLoginInfo({"username": "nonexistent", "host": "host", "password": "password"})
        self.assertFalse(result)

    def test_generateXml(self):
        self.manager.addLoginInfo("user1", "host1", "password1")
        
        self.assertTrue(os.path.exists(self.TEST_FILE_PATH))
        
        with open(self.TEST_FILE_PATH, 'r') as file:
            content = file.read()
            root = ET.fromstring(content)
            self.assertIsNotNone(root.find("login"))

if __name__ == "__main__":
    unittest.main()
