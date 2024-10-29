import subprocess
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys
import os

# Ensure the package directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pkg_vers')))

# Import the __main__ module from pkg_vers
import pkg_vers.__main__ as main_module

class TestMain(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['__main__.py', 'get_versions', 'test_path1', 'test_path2'])
    @patch('pkg_vers.__main__.get_pkg_vers')
    def test_get_versions(self, mock_get_pkg_vers, mock_stdout):
        # Set up the mock return value
        mock_get_pkg_vers.return_value = {
            'package1': '1.0.0',
            'package2': '2.3.4'
        }

        # Call the main function to trigger the CLI
        main_module.main()

        # Define expected output
        expected_output = "package1: 1.0.0\npackage2: 2.3.4\n"

        # Get the actual output and strip any extra whitespace
        actual_output = mock_stdout.getvalue().strip()

        # Check the actual output
        self.assertEqual(actual_output, expected_output.strip())


class TestPackageInstallation(unittest.TestCase):

    @patch('subprocess.run')
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.argv', ['__main__.py', 'install_packages', 'package1==1.0.0', 'package2==2.0.0'])
    def test_install_packages(self, mock_stdout, mock_subprocess_run):
        # Configure the mock to simulate Mamba success for package1 and failure for package2
        def mock_subprocess_effect(*args, **kwargs):
            if 'mamba' in args[0] and 'package1==1.0.0' in args[0]:
                return MagicMock(returncode=0)
            elif 'mamba' in args[0] and 'package2==2.0.0' in args[0]:
                raise subprocess.CalledProcessError(1, args[0])
            elif 'pip' in args[0] and 'package2==2.0.0' in args[0]:
                return MagicMock(returncode=0)
            return MagicMock(returncode=0)

        mock_subprocess_run.side_effect = mock_subprocess_effect

        # Call the main function to trigger the CLI
        main_module.main()

        # Get the actual output
        actual_output = mock_stdout.getvalue()

        # Check for expected output
        self.assertIn("Attempting to install package1==1.0.0 with Mamba", actual_output)
        self.assertIn("Attempting to install package2==2.0.0 with Mamba", actual_output)
        self.assertIn("Mamba installation failed for package2", actual_output)
        self.assertIn("Attempting pip install", actual_output)

if __name__ == '__main__':
    unittest.main()
