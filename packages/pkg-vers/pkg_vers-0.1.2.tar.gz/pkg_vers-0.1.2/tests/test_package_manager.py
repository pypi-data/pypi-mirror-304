import unittest
from unittest.mock import patch
from pkg_vers.package_manager import _get_installed_packages, _get_package_versions
from pkg_vers.package_manager import _get_imported_top_level_packages
from pkg_vers.package_manager import get_pkg_vers

class TestPackageManager(unittest.TestCase):
    def test_get_installed_packages(self):
        packages = _get_installed_packages()
        self.assertIsInstance(packages, dict)
        self.assertGreater(len(packages), 0)  # Ensure some packages are returned

    def test_get_specific_package_versions(self):
        versions = _get_package_versions(['torch', 'numpy'], {'torch': '1.0', 'numpy': '2.0'})
        self.assertIsInstance(versions, dict)
        self.assertIn('torch', versions)
        self.assertIn('numpy', versions)

    def test_get_imported_top_level_packages(self):
        imported_packages = _get_imported_top_level_packages([__file__])
        self.assertIsInstance(imported_packages, set)
        self.assertIn('unittest', imported_packages)  # Ensure this test file's imports are detected

    def test_include_pkg_vers(self):
        # Create a simple test file
        with open('test.py', 'w') as f:
            f.write('import numpy')
        
        try:
            # Mock installed packages
            with patch('pkg_vers.package_manager._get_installed_packages') as mock_installed:
                mock_installed.return_value = {
                    'numpy': '1.21.0',
                    'pkg-vers': '0.1.0'
                }
                
                # Test without include_pkg_vers
                result = get_pkg_vers('test.py')
                self.assertNotIn('pkg-vers', result)
                
                # Test with include_pkg_vers=True
                result = get_pkg_vers('test.py', include_pkg_vers=True)
                self.assertIn('pkg-vers', result)
        
        finally:
            import os
            os.remove('test.py')

if __name__ == '__main__':
    unittest.main()