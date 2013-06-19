import unittest
import filecmp, io
import concat

class ConcatTest(unittest.TestCase):

    def setUp(self):
        self.parser = concat.Linker(None, None)

    def _read_and_test(self, path):
        '''Reads path/file.txt, processes it and saves it as path/result.txt
        Then compares to path/expected_result.txt
        '''
        relative_file_path = path + '/file.txt'
        result_file_path = path + '/result.txt'
        expected_result_path = path +'/expected_result.txt'

        linker = concat.Linker(relative_file_path, result_file_path)
        linker.process();
        
        self.assertTrue(filecmp.cmp(expected_result_path, result_file_path))

    def test_no_arguments(self):
        #should take exactly 1 argument
        self.assertRaises(TypeError, self.parser._concat)

    def test_unexistent_file(self):
        #should handle nonexistent files
        self.assertRaises(ValueError, self.parser._concat, 'testfiles/unexistent_file')

    def test_wrong_type(self):
        #io.open only accepts strings, concat should do the same
        self.assertRaises(TypeError, self.parser._concat, [])
        self.assertRaises(TypeError, self.parser._concat, None)
        self.assertRaises(TypeError, self.parser._concat, 2)

    def test_read_empty_file(self):
        #should return empty unicode string if empty file is read
        self.assertEqual(self.parser._concat('testfiles/empty.txt'), u'')

    def test_read_and_process_file_with_no_imports(self):
        #should return original file contents
        self._read_and_test('testfiles/no_imports')

    def test_read_and_process_file_with_imports_but_with_no_leading_whitespaces(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/top_imports')

    def test_read_and_process_file_with_imports_and_leading_whitespaces(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/leading_whitespace_imports')

    def test_read_and_process_file_with_missing_files_in_imports(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/missing_files')
    
    def test_recursive_top_imports(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/recursive_top_imports')
    
    def test_recursive_imports_with_leading_whitespaces(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/recursive_leading_whitespaces_imports')

    def test_infinitely_recursive_import_detection(self):
        #should return as expected in expected_result.txt file
        self._read_and_test('testfiles/infinite_recursion_detection_0')
        self._read_and_test('testfiles/infinite_recursion_detection_1')

if __name__ == '__main__':
    unittest.main()


