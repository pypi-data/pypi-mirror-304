import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow.transformers.writers import StreamWriter

class StreamWriterTest(unittest.TestCase):

    def test_stream_writer(self):
        
        text = '''Isto é um teste de escrita de texto.
Isto é um teste de escrita de texto.
Isto é um teste de escrita de texto.
Isto é um teste de escrita de texto.        
'''
        
        with open("etc\\writer.txt", "w", encoding="utf-8") as file_stream:
            writer = StreamWriter(file_stream)
            try:
                writer.handle(text)
            finally:
                writer.close()

if __name__ == '__main__':
    unittest.main()