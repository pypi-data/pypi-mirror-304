import unittest
import os
import sys

# Necessário para que o arquivo de testes encontre
test_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(test_root)
sys.path.insert(0, os.path.dirname(test_root))
sys.path.insert(0, test_root)

from tinydataflow.connectors.readers import StreamReader

'''
Text Stream:

with open("arquivo_exemplo.txt", "r") as file_stream:
    reader = StreamReader(file_stream)
    while not reader.eof():
        print(reader.read(100))
        
Binary streams:

with open("arquivo_binario.bin", "rb") as bin_stream:
    reader = StreamReader(bin_stream)
    while not reader.eof():
        data = reader.read(512)  # Lê 512 bytes por vez
        process_binary_data(data)
        
API Stream:

import requests
from io import BytesIO

response = requests.get('https://example.com/data', stream=True)
api_stream = BytesIO(response.content)

reader = StreamReader(api_stream)
while not reader.eof():
    data = reader.read(256)  # Lê 256 bytes por vez
    process_api_data(data)
'''

class StreamReaderTest(unittest.TestCase):

    def test_stream_reader(self):
        
        with open("etc\\output.txt", "r") as file_stream:
            reader = StreamReader(file_stream, 200)
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