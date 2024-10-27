from tinydataflow.core import DataConnector, DataConnectorException
from typing import List, Type, Union


class StreamReader(DataConnector):
    
    _eof = False
    
    def __init__(self, stream, page_size = -1):
        """
        Inicializa o leitor de streams com o objeto de stream fornecido.
        :param stream: Um objeto de stream que implemente métodos como `read()`.
        :param page_size: Número de bytes/caracteres a serem lidos por vez. O padrão é -1, o que lê tudo.
        """
        self._stream = stream
        self._eof = False
        self._page_size = page_size

    @property
    def stream(self):
        return self._stream
    
    @property
    def page_size(self):
        return self._page_size

    def read(self):
        """
        Lê dados do stream até a quantidade especificada.
        :param size: Número de bytes/caracteres a serem lidos. O padrão é -1, o que lê tudo.
        :return: Dados lidos do stream.
        """
        if self.eof():
            return ''
        
        data = self._stream.read(self.page_size)
        if data == '' or data == b'' or len(data) < self.page_size:
            # Se não há mais dados para ler, marcamos EOF
            self.set_eof(True)
        return data

    def eof(self):
        """
        Verifica se o fim do stream foi atingido.
        :return: True se o fim do stream foi atingido, False caso contrário.
        """
        return self._eof
    
    def set_eof(self, eof: bool):
        self._eof = eof
        
    def close(self):
        if hasattr(self._stream, 'close') and callable(self._stream.close):
            self._stream.close()

class BufferedLineReader(StreamReader):
    
    _buffer_size = -1
    _buffer = ""
    _end_of_stream = False
    
    def __init__(self, filename: str, encoding: str = 'utf-8', buffer_size = 4096):
        input_stream = open(filename, mode='r', encoding=encoding, newline='')
        super().__init__(input_stream)
        self.buffer_size = buffer_size
        
    @property
    def output_type(self) -> Type:
        return str # Retorna uma linha

    def read(self) -> str:
        """
        Lê uma linha do stream de forma eficiente usando um buffer interno.
        :return: Uma linha completa ou parte dela se EOF for atingido.
        """
        while "\n" not in self._buffer and not self._end_of_stream:
            # Ler mais dados no buffer até encontrar uma quebra de linha
            more_data = self.stream.read(self._buffer_size)
            if more_data == "":
                self._end_of_stream = True
                break
            self._buffer += more_data

        if "\n" in self._buffer:
            # Se encontramos uma linha completa no buffer, dividimos por ela
            line, self._buffer = self._buffer.split("\n", 1)
            return line
        else:
            # Se não há mais quebras de linha, retornamos o que sobrou no buffer
            line = self._buffer
            self._buffer = ""
            return line

    def eof(self):
        """
        Verifica se o fim do stream foi atingido.
        :return: True se o fim do stream foi atingido e o buffer está vazio, False caso contrário.
        """
        return self._end_of_stream and self._buffer == ""

    def __iter__(self):
        """
        Permite a iteração direta sobre as linhas do stream.
        :yield: Uma linha por vez.
        """
        while not self.eof():
            yield self.read()
            
    
    @property
    def buffer_size(self):
        return self._buffer_size
    
    @buffer_size.setter
    def buffer_size(self, buffer_size: int):
        self._buffer_size = buffer_size
        
class LineArrayReader(BufferedLineReader):
    '''
    The TxtFileReader returns a list of lines from a given text file.
    '''
    
    def __init__(self, filename: str, encoding: str = 'utf-8', number_of_lines = -1):
        """
        Inicializa o leitor de arquivos de texto com buffer.
        :param stream: Um objeto de stream que implemente o método `read`.
        :param buffer_size: Tamanho do buffer em bytes a ser lido por vez.
        """
        super().__init__(filename, encoding)
        self.number_of_lines = number_of_lines
        
    @property
    def output_type(self) -> Type:
        return list # Retorna uma lista de linhas do arquivo
    
    def read(self) -> list[str]:
        """
        Lê todas as linhas do arquivo e retorna como uma lista de strings.
        :return: Uma lista de strings, cada uma representando uma linha do arquivo.
        """
        lines = []
        while not self.eof() and (self.number_of_lines == -1 or len(lines) < self.number_of_lines):
            line = super().read().strip()  # Remove espaços e quebras de linha
            lines.append(line)
        return lines



class CSVReader(BufferedLineReader):
    '''
    The CSVReader reads a line from a given CSV file provided in the constructor.
    Each line can be readed and iterated sequentially to be transmitted to the next transformer in each iteration
    '''
            
    def __init__(self, filename: str, encoding: str = 'utf-8', buffer_size = 4096, delimiter=';'):
        super().__init__(filename, encoding, buffer_size)
        self.delimiter=delimiter
     
    @property
    def output_type(self) -> Type:
        return list  # retorna uma lista de strings
    
    def read(self) -> list[str]:
        """
        Lê uma linha do CSV e a divide em uma lista de strings.
        :return: Uma lista de strings contendo os valores da linha.
        """
        line = super().read()
        if line:
            return line.strip().split(self.delimiter)  # Remove espaços em branco e divide pelo delimitador
