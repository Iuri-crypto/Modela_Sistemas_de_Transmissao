


from EnlineDevEng.utils.auxiliary import PowerSystemsNet
from EnlineDevEng.utils.populate import _set_entries



def create_ext_grid(
    net: PowerSystemsNet,
    name: str | None,
    bus: int,
    vm_pu: float = 1.0,
    va_degree: float = 0.0
):
    
    """
    Adiciona uma Conexão com a rede externa.
    
    Redes externas representam a rede do sistema de potência
    considerada uma fonte infinita, sendo assim modelado como uma barra
    slack no cálculo do fluxo de potência.
    
    Parâmetros:
        net: A rede PowerSystems em que o elemento é criado
        bus: A barra que a rede externa se conecta
        name: O nome da rede externa.
        vm_pu: A tensão de referência da rede externa.
        va_degree: O ângulo de fase da rede externa em graus.
         
    Returns:
        None 
    
    Example:
        >>> create_ext_grid(net, bus=1, name=REDE_EXT, vm_pu=1.0, va_degree=0.0) 
    """
    
    entries = {
        "name": name, 
        "bus": bus,
        "vm_pu": vm_pu,
        "va_degree": va_degree,
    }
    
    _set_entries(net, "ext_grid", entries=entries)