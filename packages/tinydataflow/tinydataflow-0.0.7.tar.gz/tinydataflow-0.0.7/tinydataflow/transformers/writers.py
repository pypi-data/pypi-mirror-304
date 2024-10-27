from tinydataflow.core import DataTransformer, DataTransformerException
from typing import List, Type, Union


class StreamWriter(DataTransformer):
    
    _output_stream = None
    
    def __init__(self, output_stream):
        super().__init__()
        self._output_stream = output_stream  # Objeto stream para a escrita

    def handle(self, input_data: any) -> any:
        """Escreve o dado de entrada no stream e propaga o resultado para o próximo transformador."""
        # Converte o input_data para string para garantir a compatibilidade com o método write
        data_to_write = str(input_data)
        data_to_write = data_to_write + '\n' if not data_to_write[len(data_to_write) - 1] in ['\n', '\r'] else data_to_write
        self._output_stream.write(data_to_write)  # Escreve no stream com uma nova linha
        
        # Propaga para o próximo transformador, caso exista
        return self.push(input_data)
        
    @property
    def output_stream(self):
        return self._output_stream
    
    def close(self):
        if hasattr(self._output_stream, 'close') and callable(self._output_stream.close):
            self._output_stream.close()
       
class LineWriter(StreamWriter):
    '''
    The LineWriter appends a new line to the end of file provided by the user
    '''
    def __init__(self, output_file: str):     
        self._output_file = output_file   
        super().__init__(open(output_file, "a"))
    
    @property
    def input_type(self) -> Type:        
        return str  # Espera uma linha para ser escrita no arquivo

    @property
    def output_type(self) -> Type:
        return str # retorna a linha escrita

    def setup(self, params: dict):
        """Opcionalmente, configurar o arquivo de saída (por exemplo, modo de abertura)."""
        open_mode = params.get('open_mode', 'a')  # 'a' para adicionar ou 'w' para sobrescrever
        if open_mode == 'w':
            with open(self._output_file, open_mode) as f:
                pass  # Limpa o arquivo se estiver no modo 'w'
            
    def handle(self, input_data: str):
        try:
            data_to_write = input_data + "\n" if not input_data[len(input_data) - 1] in ['\n', '\r'] else input_data
            self.output_stream.write(data_to_write)  # Escreve no stream com uma nova linha
            return self.push(input_data)
        except Exception as e:
            raise DataTransformerException(f"Failed to write to file: {self._output_file}: {str(e)}")
