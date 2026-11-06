


from EnlineDevEng.utils.auxiliary import PowerSystemsNet
from EnlineDevEng.utils.populate import _set_entries



def create_gen(
    net: PowerSystemsNet,
    name: str | None,
    bus: int,
    p_mw: float,
    vm_pu: float = 1.0,
    sn_mva: float | None = None,
    in_service: bool = True
):
    
    """
    Adiciona um gerador a rede.
    
    Geradores  (síncronos) são sempre modelados como 
    barras PV com controle de tensão.
    
    Parâmetros:
        net: A rede PowerSystems em que o elemento é criado
        bus: A barra que o gerador se conecta
        vn_kv: O nível de tensão da rede.
        name: O nome do gerador.
        p_mw: A Potência ativa do gerador
        vm_pu: A tensão de referência do gerador.
        sn_mva: Potência nominal do gerador.
        in_service: True se a barra estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_gen(net, bus=1, p_mw=10.0, vm_pu=1.0) 
    """
    
    entries = {
        "name": name, 
        "bus": bus,
        "p_mw": p_mw,
        "vm_pu": vm_pu,
        "sn_mva": sn_mva,
        "in_service": in_service
    }
    
    _set_entries(net, "gen", entries=entries)