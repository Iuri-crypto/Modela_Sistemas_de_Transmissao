


from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_bus(
    net: EnlineDevEngNet,
    vn_kv: float,
    name: str,
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
    
    entries = {"name": name, "vn_kv": vn_kv, "in_service": in_service}
    _set_entries(net, "bus", entries=entries)