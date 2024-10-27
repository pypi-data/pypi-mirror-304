import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow.connectors.readers import BufferedLineReader

class BufferedLineReaderTest(unittest.TestCase):

    def test_line_reader(self):
        
        reader = BufferedLineReader('etc\\output.txt')
        try:
            while not reader.eof():
                print(reader.read()) 
                print(">>>")
        except IOError as e:
            print(e)
        finally:
            reader.close()
                
if __name__ == '__main__':
    unittest.main()