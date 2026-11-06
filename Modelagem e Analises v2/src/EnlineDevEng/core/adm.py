




from pathlib import Path 
from abc import ABC, abstractmethod
from typing import Dict, Type, Any
from EnlineDevEng.models.grid_model import GridModel


class BasePowerFlowSolver(ABC):
    
    """
    Clase base abstrata para todos os métodos de 
    fluxo de potência.
    """
    
    # Registro global dos métodos disponíveis
    _registry: Dict[str, Type[BasePowerFlowSolver]] = {}
    
    # Atributo que cada subclasse deve definir
    # Ex: ['nr']
    aliases = list[str] = []

    def __init_subclass__(cls, **kwargs):
        """
        Registra automaticamente qualquer classe que herdar
        de BasePowerFlowSolver.
        """
        super().__init_subclass__(**kwargs)
         
        for alias in getattr(cls, "aliases", []):
            name_key = alias.lower().replace("_", "").replace("-", "")
            cls._registry[name_key] = cls 
    
    
    @classmethod
    def get_solver(cls, method: str, **kwargs) -> BasePowerFlowSolver:
        """
        Instancia dinamicamente o solucionador solicitado
        via alias.
        """
        key = method.lower().replace("_", "").replace("-", "")
        return cls._registry[key](**kwargs)
    
    
    @abstractmethod
    def solve(self, grid: GridModel, **kwargs):
        """
        "Toda classe de fluxo de potência que
        quiser existir neste sistema É OBRIGADA
        a criar um método chamado solve(self, net, **kwargs).
        Se não criar, a biblioteca nem deixa essa 
        classe nascer."
        
        -> Resolve o fluxo de potência
        """
        pass
        



class BaseNetworkBuilder(ABC):
    
    """
    Interface abstrata para o modelador de rede.
    """
    
    @abstractmethod
    def build(self, net: Any) -> GridModel:
        """
        Processa os dataframes crus e retorna o 
        GridModel limpo.
        """
        pass
    
    


class BaseNetworkParser(ABC):
    
    """
    Classe base abstrata para leitores linha por 
    linha de arquivos de rede.
    """
    
    _registry: Dict[str, Type[BaseNetworkParser]] = {}
    extensions: list[str] = [] # Ex: ["pwf", "dss", ...]
    
    def __init_subclass__(cls, **kwargs):
        """
        Registra automaticamente os parsers com base
        nas extensões suportadas.
        """
        super().__init_subclass__(**kwargs)
        
        for ext in getattr(cls, "extensions", []):
            ext_key = ext.lower().strip()
            cls._registry[ext_key] = cls 
            
    
    @classmethod
    def get_parser(cls, extension: str) -> BaseNetworkParser:
        """
        Instancia o parser adequado baseado na extensão
        do arquivo.
        """
        
        return cls._registry[extension]()
    
    
    @abstractmethod
    def parse(self, net: Any, filepath: Path, encoding: str = "latin-1"):
        """
        Executa a leitura linha por linha do arquivo e 
        envia as informações para 'net'
        """
        
        pass 