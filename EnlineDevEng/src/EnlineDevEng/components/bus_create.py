


from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_bus(
    net: EnlineDevEngNet,
    vn : float,
    numero: int,
    tipo: str,
    barra_controlada: int,
    q_min: float,
    q_max: float,
    v_min: float,
    v_max: float,
    name: str | None = None,
    in_service: bool = True
):
    
    """
    Adiciona uma barra na tabela net["bus"].
    
    Parâmetros:
        net: A rede EnlineDevEng em que o elemento é criado
        vn_kv: O nível de tensão da rede.
        name: O nome da barra.
        in_service: True se a barra estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_bus(net, 20.0, name="bus1")
    """
    
    entries = {"name": name, "vn": vn, "numero": numero, "tipo": tipo, 
               "barra_controlada": barra_controlada,
               "q_min": q_min, "q_max": q_max, "v_min": v_min,
               "v_max": v_max, "in_service": in_service}
    _set_entries(net, "bus", entries=entries)