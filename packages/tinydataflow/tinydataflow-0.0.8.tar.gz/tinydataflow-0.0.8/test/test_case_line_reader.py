import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow import TinyDataFlow
from tinydataflow.transformers.writers import LineWriter
from tinydataflow.connectors.readers import BufferedLineReader

class FileSelTest(unittest.TestCase):

    def test_file_selector(self):
        
        reader = BufferedLineReader('etc\\output.txt')
        writer = LineWriter('etc\\copy.txt')

        try:
            app = TinyDataFlow(reader, [writer])
            app.setup({'open_mode': 'w'})
            app.setup()
            app.run()    
            print(f"Resultados: {app.outputs}")
            
            self.assertEqual(len(app.outputs), 35)
        except TypeError as e:
            print(f"Erro de compatibilidade: {e}")
               
if __name__ == '__main__':
    unittest.main()