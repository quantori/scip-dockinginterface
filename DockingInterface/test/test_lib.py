import unittest

from pathlib import Path
from platform import machine
from DockingInterface.lib import LibPathResolver, LIBRARY_PATHS


class TestResolvingLibPath(unittest.TestCase):

    TEST_LIBRARY_PATH_PREFIX = Path(__file__).parent

    def setUp(self):
        self.expected_path = str(self.TEST_LIBRARY_PATH_PREFIX / 'C_Dynamic_Libs/Linux')
        self.resolver = LibPathResolver(str(self.TEST_LIBRARY_PATH_PREFIX), self.expected_path) 

    def test_wrong_library_name(self):
        '''
        Incorrect library name raise ValueError exception
        '''
        with self.assertRaises(ValueError):
            self.resolver.get_lib('xtrx')

    @unittest.skip("not implemented")
    def test_unsupported_platform(self):
        '''
        In case of unsupported platform we expect NotImplementedError exception
        '''
        with self.assertRaises(NotImplementedError):
            self.resolver.get_lib('smina')

    def test_qvina_library_path(self):
        '''
        Get full path to qvina dynamic library
        '''
        path = self.resolver.get_lib('qvina')
        self.assertIsNotNone(path, 'Actual path is None for qvina library')
        self.assertEqual(self.expected_path, str(path.parent))
        
    def test_smina_library_path(self):
        '''
        Get full path to smina dynamic library
        '''
        path = self.resolver.get_lib('smina')
        self.assertIsNotNone(path, 'Actual path is None for smina library')
        self.assertEqual(self.expected_path, str(path.parent))

    def test_vina_library_path(self):
        '''
        Get full path to vina dynamic library
        '''
        path = self.resolver.get_lib('vina')
        self.assertIsNotNone(path, 'Actual path is None for vina library')
        self.assertEqual(self.expected_path, str(path.parent))


class TestResolvingLibDefaults(unittest.TestCase):

    TEST_LIBRARY_PATH_PREFIX = Path(__file__).parent.parent / 'DockingInterface'

    def setUp(self):
        self.resolver = LibPathResolver() 

    def test_search_path(self):
        '''
        Verify that deafult search paths are subfolder of the current package
        '''
        expected = LIBRARY_PATHS[machine().lower()]
        self.assertEqual(
            len(expected),
            len(self.resolver.spaths),
            'Number of elements for expected and actual search path are not the same'
        )
        for path in self.resolver.spaths:
            self.assertTrue(path.is_relative_to(self.TEST_LIBRARY_PATH_PREFIX))