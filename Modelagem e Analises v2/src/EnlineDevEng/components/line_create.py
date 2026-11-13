


from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_line(
    net: EnlineDevEngNet,
    from_bus: int,
    to_bus: int,
    length_km: float,
    r_percent: float,
    x_percent: float,
    b_percent: float,
    name: str | None = None,
    in_service: bool = True
):
    
    """
    Adiciona uma linha na tabela net["line"].
    
    Parâmetros:
        net: Objeto que a rede pode ser criada.
        name: Nome da linha.
        from_bus: ID da barra no lado da linha.
        to_bus: ID da barra no outro lado da linha.
        length_km: O comprimento da linha em km.
        r_percent: Resistência em percentual.
        x_percent: Reatância em percentual.
        b_percent: Susceptância em percentual.
        in_service: True se a linha estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_line(net, name="LT_01", from_bus=1, to_bus=2, 
                        length_km=1, r_ohm_per_km=0.1, x_ohm_per_km=0.5,
                        c_nf_per_km=1.5)
    """
    
    entries = {
        "name": name,
        "from_bus": from_bus,
        "to_bus": to_bus,
        "length_km": length_km,
        "r_percent": r_percent,
        "x_percent": x_percent,
        "b_percent": b_percent,
        "in_service": in_service
    }
    
    _set_entries(net, "line", entries=entries)