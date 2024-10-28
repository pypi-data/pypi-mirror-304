""" 
Test for read_env_file.py.
This will look for a .env file in CWD, and recursively in up to three levels above.

Author: Darren

PRE-REQS:
- There must be a .env in the hierarchy. E.g. in project dazbo-commons-py folder.
- It must contain:
  TEST=123
"""
import unittest
import logging
import os
from unittest.mock import patch
import dazbo_commons as dc

APP_NAME = __name__
logger = dc.retrieve_console_logger(APP_NAME)
logger.setLevel(logging.DEBUG)
logger.info("Logger initialised.")
    
class TestGetEnvsFromFile(unittest.TestCase):
    """ Test the read_env.file.py module """
       
    def test_env_file_found(self):
        """ Ensure .env in folder hierarchy with TEST defined. """
        result = dc.get_envs_from_file()
        self.assertTrue(result)                
        self.assertEqual(os.environ.get('TEST'), '123')

    @patch('os.path.exists')
    @patch('dotenv.load_dotenv')
    def test_no_env_file_found(self, mock_load_dotenv, mock_exists):
        # Mock os.path.exists to always return False
        mock_exists.return_value = False
        result = dc.get_envs_from_file()

        # Assert that load_dotenv was never called and the function returned False
        mock_load_dotenv.assert_not_called()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
