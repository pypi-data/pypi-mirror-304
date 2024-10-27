from abc import ABC, abstractmethod
from typing import Union, List, Type


class DataFlowStrategy(ABC):
    
    @property
    def input_type(self) -> Type:
        return None
  
    @property
    def output_type(self) -> Type:
        return None
    
    def setup(self, params: dict):
        pass
 
        
class DataConnector(DataFlowStrategy):
   
    @abstractmethod
    def read(self) -> any:
        """Lê a fonte de dados."""
        pass
    
    @abstractmethod
    def eof(self):
        pass

    def close(self):
        """Fecha a conexão com a fonte de dados."""
        pass


class DataTransformer(DataFlowStrategy):   
    
    _next_transformer = None 
    
    def set_next(self, transformer: "DataTransformer") -> "DataTransformer":
        """Define o próximo transformador da cadeia."""
        self._next_transformer = transformer
        return transformer

    @abstractmethod
    def handle(self, input_data: any) -> any:
        """Método abstrato que deve ser implementado nas subclasses para transformar o dado de entrada."""
        pass

    def push(self, output_data: any) -> any:
        """Propaga o dado de saída para o próximo transformador da cadeia."""
        if self._next_transformer:
            return self._next_transformer.handle(output_data)
        else:
            return output_data  
        
    def close(self):
        """Fecha a conexão com a fonte de dados."""
        pass

# Classe TinyFlow que utiliza um conector de dados e uma sequência de transformadores que serão executados na ordem determinada. 
class TinyDataFlow:
    
    __flow_outputs = []
    
    def __init__(self, connector: DataConnector, transformers: List[DataTransformer]):        
        self.transformers = transformers
        self.connector = connector
        self._validate_transformer_sequence()

    @property
    def outputs(self) -> List[any]:
        """Retorna os resultados do fluxo após as transformações."""
        if len(self.__flow_outputs) == 0:
            return None 
        elif len(self.__flow_outputs) == 1:
            return self.__flow_outputs[0]
        else:
            return self.__flow_outputs

    def _validate_transformer_sequence(self):
        
        """Verifica se a sequência de transformadores é compatível."""
        for i in range(len(self.transformers) - 1):
            current_transformer = self.transformers[i]
            
            if i == 0:
                if current_transformer.input_type != any and current_transformer.input_type != self.connector.output_type:
                    raise TypeError(f"Incompatibilidade entre conector e primeiro transformador: "
                                    f"{self.connector.__class__.__name__} produz {self.connector.output_type.__name__} como saída."
                                    f" Mas {current_transformer.__class__.__name__} espera {current_transformer.input_type.__name__} como entrada.")                                    
            
            next_transformer = self.transformers[i + 1]
                    
            if current_transformer.output_type != any and next_transformer.input_type != any and current_transformer.output_type != next_transformer.input_type:
                raise TypeError(f"Incompatibilidade entre tipos de dados de entrada/saída: "
                    f"{current_transformer.__class__.__name__} produz {current_transformer.output_type.__name__} com saída, "
                    f"mas {next_transformer.__class__.__name__} espera {next_transformer.input_type.__name__} como entrada.")
            current_transformer.set_next(next_transformer)


    def run(self) -> None:
        """Executa o fluxo de leitura da fonte de dados e transformação."""
        current_output = None
        try:
            while not self.connector.eof():
                input_data = self.connector.read()
                if not input_data:
                    break
                if len(self.transformers) > 0:
                    current_output = self.transformers[0].handle(input_data)                 
                if current_output is not None:
                    self.__flow_outputs.append(current_output)            
                
        except DataConnectorException as e:
            raise e
        finally:
            self.connector.close()
            for transformer in self.transformers:
                transformer.close()
        
    def setup(self, params: dict = {}):
        """Configura os parâmetros do conector e dos transformadores."""
        if self.connector is not None:  
            self.connector.setup(params)
            
        for transformer in self.transformers:
            transformer.setup(params)


class DataConnectorException(Exception):
    pass

class DataTransformerException(Exception):
    pass
