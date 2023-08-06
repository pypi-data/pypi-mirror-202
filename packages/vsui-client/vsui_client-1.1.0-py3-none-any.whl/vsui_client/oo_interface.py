# oo interface for vsui client, idea is to allow better control over enabling/disabling

import logging
from abc import ABC, abstractmethod
import vsui_client.vsui_client as vsui_client

class VSUIClient(ABC):
    ''' Wrapper for vsui_client that allows for better control over enabling/disabling '''
    _handler = None
    @abstractmethod
    def connect(self, host : str = 'localhost', port : str = '8000') -> None:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def edit_element(self, data : dict) -> None:
        pass

    @abstractmethod
    def deactivate_task(self) -> None:
        pass

    @abstractmethod
    def notify(self, txt : str, type : str) -> None:
        pass

    @abstractmethod
    def set_task_id(self, id : str) -> None:
        pass

    @abstractmethod
    def set_logging_target(self, key : str) -> None:
        pass

    @abstractmethod
    def encode_image(
        self,
        arr,
        title: str = '',
        format : str = 'jpg',
        figsize: tuple = (8, 8),
        cmap: str = "gray"
    ) -> str:
        pass

    @abstractmethod
    def get_handler(self) -> logging.Handler:
        pass

class VSUIEnabled():
    def connect(self, host : str = 'localhost', port : str = '8000') -> None:
        return vsui_client.connect(host, port)
    
    def disconnect(self) -> None:
        return vsui_client.disconnect()
    
    def edit_element(self, data : dict) -> None:
        return vsui_client.edit_element(data)
    
    def deactivate_task(self) -> None:
        return vsui_client.deactivate_task()

    def notify(self, txt : str, type : str) -> None:
        return vsui_client.notify(txt, type)

    def set_task_id(self, id : str) -> None:
        return vsui_client.set_task_id(id)
    
    def set_logging_target(self, key : str) -> None:
        return vsui_client.set_logging_target(key)

    def encode_image(
        self,
        arr,
        title: str = '',
        format : str = 'jpg',
        figsize: tuple = (8, 8),
        cmap: str = "gray"
    ) -> str:
        return vsui_client.encode_image(
            arr=arr,
            title=title,
            format=format,
            figsize=figsize,
            cmap=cmap
        )
    
    def get_handler(self) -> logging.Handler:
        if self.get_handler is None:
            self._handler = vsui_client.RequestHandler()
        return self._handler

class VSUIDisabled():
    def connect(self, host : str = 'localhost', port : str = '8000') -> None:
        ''' do nothing - not in UI mode '''
        pass
    
    def disconnect(self) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def edit_element(self, data : dict) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def deactivate_task(self) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def notify(self, txt : str, type : str) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def set_task_id(self, id : str) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def set_logging_target(self, key : str) -> None:
        ''' do nothing - not in UI mode '''
        pass

    def encode_image(
        self,
        arr,
        title: str = '',
        format : str = 'jpg',
        figsize: tuple = (8, 8),
        cmap: str = "gray"
    ) -> str:
        ''' do nothing - not in UI mode '''
        pass

    def get_handler(self) -> logging.Handler:
        ''' return null handler - not in UI mode '''
        if self._handler is None:
            self._handler = logging.NullHandler()
        return self._handler