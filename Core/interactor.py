from abc import ABC, abstractmethod
from Utils import load_from_cfg, add_logger

class Interactor(ABC):
    @abstractmethod
    def __init__(self, cfg) -> None:
        load_from_cfg(self, cfg)
    
