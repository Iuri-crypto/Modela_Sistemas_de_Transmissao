




from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_load(
    net: EnlineDevEngNet,
    name: str,
    bus: int,
    p_mw: float,
    q_mvar: float,
    const_z_p_percent: float = 0,
    const_i_p_percent: float = 0,
    const_z_q_percent: float = 0,
    const_i_q_percent: float = 0,
    in_service: bool = True
):
    
    """
    Adiciona uma carga na tabela net["load"].
    
    Todas as cargas são modeladas no sistema consumidor.
    
    Parâmetros:
        net: A rede EnlineDevEng em que o elemento é criado
        bus: A barra que a carga está conectada.
        p_mw: A potência ativa da carga
            
            - valor positivo -> carga
            - valor negativo -> geração
        
        q_mvar: A potência reativa da carga
        const_z_p_percent: percentage of p_mw that will be associated to constant impedance load at rated voltage
        const_i_p_percent: percentage of p_mw that will be associated to constant current load at rated voltage
        const_z_q_percent: percentage of q_mvar that will be associated to constant impedance load at rated voltage
        const_i_q_percent: percentage of q_mvar that will be associated to constant current load at rated voltage
        in_service: True se a carga estiver em operação, 
                    False se estiver fora de operação.
        
    Returns:
        None 
    
    Example:
        >>> create_load(net, "LOAD", 100.0, 100.0)
    """
    
    entries = {
        "name": name, 
        "bus": bus, 
        "p_mw": p_mw,
        "q_mvar": q_mvar,
        "const_z_p_percent": const_z_p_percent,
        "const_i_p_percent": const_i_p_percent,
        "const_z_q_percent": const_z_q_percent,
        "const_i_q_percent": const_i_q_percent,
        "in_service": in_service
    }
    
    _set_entries(net, "load", entries=entries)