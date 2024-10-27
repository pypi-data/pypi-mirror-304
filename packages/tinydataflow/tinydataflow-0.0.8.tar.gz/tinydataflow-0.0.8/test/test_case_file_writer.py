import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow import TinyDataFlow
from tinydataflow.transformers.basic import ListToElem
from tinydataflow.transformers.writers import LineWriter
from tinydataflow.connectors.selectors import FileListSelector

class FileWriterTest(unittest.TestCase):

    def test_file_writer(self):
        
        file_selector = FileListSelector('etc\\.', '*.txt')
        list_to_elem = ListToElem()
        writer = LineWriter('etc\\selected.txt')
        
        try:
            app = TinyDataFlow(file_selector, [list_to_elem, writer])
            app.setup({'open_mode': 'w'})
            app.run()   
            print(app.outputs)
            
            #self.assertEqual(app.outputs, 'file_selector_output.txt')
        except TypeError as e:
            print(f"Erro de compatibilidade: {e}")
               
if __name__ == '__main__':
    unittest.main()