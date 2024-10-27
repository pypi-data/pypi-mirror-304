from abc import abstractmethod
from tinydataflow.core import DataConnector, DataConnectorException
from typing import List, Type
from pathlib import Path
import os


class DataSelector(DataConnector):
    
    _eof = False
    
    @abstractmethod
    def select(self, criteria: dict) -> any:
        pass
    
    def eof(self):
        return self._eof
    
    def close(self):
        self._eof = True
    
class FileListSelector(DataSelector):
    '''
    The FileListSelector returns a list of file from a given path and file extension to be selected.     
    '''
    
    def __init__(self, from_path: str, file_ext: str = '*.*'):
        self.criteria = { 'from_path': from_path, 'file_ext': file_ext }
    
    @property
    def output_type(self) -> Type:
        return list # Retorna uma lista de arquivos selecionados

    def select(self, criteria: dict) -> list[str]:
        file_list = []
        from_path = criteria.get('from_path')
        file_ext = criteria.get('file_ext', '*.*')
        if os.path.isdir(from_path):                
            for file_path in Path(from_path).rglob(file_ext):
                file_list.append(str(file_path)) # file_list.append(file_path) 
        return file_list
        
    def read(self) -> list[str]:
        try:
            return self.select(self.criteria)
        except IOError as e:
            raise DataConnectorException(e.message)
        finally:
            self.close()      
  