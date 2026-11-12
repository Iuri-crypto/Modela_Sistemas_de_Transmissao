


from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_shunt(
    net: EnlineDevEngNet,
    bus: int,
    q_mvar: float,
    vn_kv: float | None = None,
    p_mw: float = 0.0,
    name: str | None = None,
    in_service: bool = True
):
    
    """
    Adiciona um shunt na tabela net["shunt"].
    
    Parâmetros:
        net: A rede EnlineDevEng em que o elemento é criado
        bus: O índice da barra que o shunt está conectado.
        q_mvar: Potência reativa na tensão 1.o pu.
        vn_kv: Tensão nominal do shunt.
        p_mw: Potência ativa na tensão 1.0 pu
        name: Nome do shunt
        in_service: True se a barra estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_shunt(net, bus=1, q_mvar=2.0)
    """
    
    entries = {
        "bus": bus,
        "q_mvar": q_mvar,
        "vn_kv": vn_kv,
        "p_mw": p_mw,
        "name": name,
        "in_service": in_service
    }
    
    _set_entries(net, "shunt", entries=entries)