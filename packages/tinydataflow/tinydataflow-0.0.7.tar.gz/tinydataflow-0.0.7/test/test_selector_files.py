import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow import TinyDataFlow
from tinydataflow.connectors.selectors import FileListSelector

class FileSelTest(unittest.TestCase):

    def test_file_selector(self):
        
        file_selector = FileListSelector('etc\\.', '*.txt')
        try:
            while not file_selector.eof():
                print(file_selector.read()) 
                print(">>>")
        except IOError as e:
            print(e)
        finally:
            file_selector.close()
               
if __name__ == '__main__':
    unittest.main()