from tinydataflow.core import DataTransformer, DataTransformerException
from typing import List, Type, Union


class ListToElem(DataTransformer):
    '''
    The ListToElem handles a list and pushes its elements to the next transformer.
    '''
    
    @property
    def input_type(self) -> Type:
        return list  # espera uma lista 
    
    @property
    def output_type(self) -> Type:
        return any  # retorna qualquer coisa

    def handle(self, input_data: list) -> any: 
        outputs = []       
        for elem in input_data:
            outputs.append(self.push(elem))
        return outputs       

    def setup(self, config: dict):
        pass  # Nenhuma configuração necessária para este exemplo
    

class ListToDict(DataTransformer):
    '''
    The ListToDict transforms a list of strings into a dictionary with the specified keys in a order provided by the user.
    '''
    
    def __init__(self, k_names: list[str]):
        """
        Creates a ListToDictTransformer object.

        Args:
            k_names: The list of keys in the order they should be used to create the dictionary from a list of strings.
        """
        self.__k_names = k_names  
    
    @property
    def input_type(self) -> Type:
        return list  # Espera uma lista de strings
    
    @property
    def output_type(self) -> Type:
        return dict  # Converte em dicinário com valores em strings

    def handle(self, input_data: list[str]) -> dict[str]:
        return self.push(dict(zip(self.__k_names, input_data)))

    def setup(self, config: dict):
        pass  # Nenhuma configuração necessária para este exemplo
