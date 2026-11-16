




from pathlib import Path 
from abc import ABC, abstractmethod
from typing import Dict, Type, Any




class BaseNetworkBuilder(ABC):
    
    """
    Interface abstrata para o modelador de rede.
    """
    
    @abstractmethod
    def build(
        self,
        net: Any,
        ede: Any,
        data: Any
    ):
        """
        Processa os dataframes crus e retorna o 
        GridModel limpo.
        """
        pass
    
    
    
    
class BasePowerFlowSolver(ABC):
    
    """
    Clase base abstrata para todos os métodos de 
    fluxo de potência.
    """
    
    # Registro global dos métodos disponíveis
    _registry: Dict[str, Type[BasePowerFlowSolver]] = {}
    
    # Atributo que cada subclasse deve definir
    # Ex: ['nr']
    aliases: list[str] = []

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
    def get_solver(cls, net: Any, method: str, **kwargs) -> BasePowerFlowSolver:
        """
        Instancia dinamicamente o solucionador solicitado
        via alias.
        """
        key = method.lower().replace("_", "").replace("-", "")
        return cls._registry[key](net=net, **kwargs)
    
    
    @abstractmethod
    def solve(self, grid: Any, **kwargs):
        """
        "Toda classe de fluxo de potência que
        quiser existir neste sistema É OBRIGADA
        a criar um método chamado solve(self, net, **kwargs).
        Se não criar, a biblioteca nem deixa essa 
        classe nascer."
        
        -> Resolve o fluxo de potência
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
    def get_parser(cls, file_path: Path) -> BaseNetworkParser:
        """
        Instancia o parser adequado baseado na extensão
        do arquivo.
        """
        extension = file_path.suffix.lstrip(".")
        
        return cls._registry[extension]()
    
    
    @abstractmethod
    def parse(self, net: Any, filepath: Path, encoding: str = "latin-1"):
        """
        1 - Impede que a classe base seja instanciada diretamente
        2 - Obriga as subclasses a implementarem a leitura
        3 - Garante uma interface única (Poliformismo)
        """
        
        pass 
    
    
    

class BaseNetworkFileBuilder(ABC):
    """
    Classe abstrata responsável pela seleção
    de qual file_builder a ser usado 
    para a injeção dos dados na estrutura aceita
    pela modelagem.
    
    Exemplo: Arquivos .pwf têm um conjunto de informações
             Arquivos .dss têm outro conjunto de informações
             ...
             
             Desta forma para cada escopo fornecido de informações
             seja em formato (.pwf, .dss, ...) seleciona-se file_builder
             adequado para varrer as informações.
    """
    
    _registry: Dict[str, Type[BaseNetworkFileBuilder]] = {}
    extensions: list[str] = []
    
    
    def __init_subclass__(cls, **kwargs):
        """
        Registra automaticamente os builders com base
        nas extensões suportadas.
        """
        super().__init_subclass__(**kwargs)
        
        for ext in getattr(cls, "extensions", []):
            ext_key = ext.lower().strip()
            cls._registry[ext_key] = cls 
            
    
    @classmethod
    def get_builder(cls, file_path: Path) -> BaseNetworkFileBuilder:
        """
        Instancia o modelador adequado baseado na extensão
        do arquivo. 
            
            OBS: Cada arquivo tem um conjunto de 
        informações que permite modelar a rede de determinada forma.
        """
        extension = file_path.suffix.lstrip(".")
        
        return cls._registry[extension]()
    

    @abstractmethod
    def network_build(self, net: Any, ede: Any):
        """
        Popula o objeto 'net' com todas as tabelas extraídas
        do Arquivo de entrada.
        """
        
        pass 