import unittest
import sys
from pkg_vers.package_manager import _get_excluded_module_names

class TestGetAllIncludedModuleNames(unittest.TestCase):

    def test_function_returns_list(self):
        result = _get_excluded_module_names()
        self.assertIsInstance(result, list)

    def test_function_returns_non_empty_list(self):
        result = _get_excluded_module_names()
        self.assertTrue(len(result) > 0)

    def test_function_returns_sorted_list(self):
        result = _get_excluded_module_names()
        self.assertEqual(result, sorted(result))

    def test_common_modules_present(self):
        result = _get_excluded_module_names()
        common_modules = ['os', 'sys', 'math', 'datetime', 'random']
        for module in common_modules:
            self.assertIn(module, result)

    @unittest.skipIf(sys.version_info > (3, 10), "Test only for Python 3.10+")
    def test_python_310_plus_method(self):
        result = _get_excluded_module_names()
        self.assertIn('sys', result)
        self.assertIn('os', result)
        # Check if some modules from sys.builtin_module_names are present
        builtin_modules = set(sys.builtin_module_names)
        self.assertTrue(any(module in result for module in builtin_modules))

    @unittest.skipIf(sys.version_info >= (3, 10), "Test only for Python < 3.10")
    def test_python_pre_310_method(self):
        result = _get_excluded_module_names()
        self.assertIn('sys', result)
        self.assertIn('os', result)
        # Check if the result doesn't contain obviously non-standard modules
        self.assertNotIn('numpy', result)
        self.assertNotIn('pandas', result)

if __name__ == '__main__':
    unittest.main()