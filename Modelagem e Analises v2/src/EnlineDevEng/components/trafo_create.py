


from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.populate import _set_entries



def create_trafo(
    net: EnlineDevEngNet,
    from_bus: float,
    to_bus: float,
    r_percent: float,
    x_percent: float,
    b_percent: float,
    shift_degree: float,
    tap_min: float,
    tap_max: float,
    num_taps: int,
    tap_pos: float,
    name: str | None = None,
    in_service: bool = True
):
    
    """
    Adiciona um transformador na tabela net["trafo"].
    
    Parâmetros:
        net: A rede EnlineDevEng em que o elemento é criado
        name: Nome do transformador
        hv_bus: ID da barra em alta tensão que o trafo é conectado.
        lv_bus: ID da barra de baixa tensão que o trafo é conectado.
        sn_mva: Potência aparente.
        vn_hv_kv: Tensão no lado de alta tensão.
        vn_lv_kv: Tensão no lado de baixa tensão.
        vk_percent: Tensão de curto circuito relativa.
        vkr_percent: parte real da tensão de curto circuito.
        pfe_kw: Perdas no ferro em kw.
        i0_percent: Perdas em malha aberta em percentual da corrente nominal.
        shift_degree: Ângulo de defasagem do transformador.
        tap_side: Posição do comutador de taps ("hv", "lv").
        tap_neutral: Posição do tap na qual a relação de transformação é igual à relação entre as tensões nominais.
        tap_max: Posição máxima permitida para o tap.
        tap_min: Posição miníma permitida para o tap.
        tap_step_percent: Tamanho do passo do tap para a magnitude da tensão em percentual.
        tap_step_degree: Tamanho do passo do tap para o ângulo de fase.
        tap_pos: Posição atual do tap. O padrão é a posição neutra.
        in_service: True se o trafo estiver em operação, 
                    False se estiver fora de operação.
                    
    Returns:
        None 
    
    Example:
        >>> create_transformer_from_parameters(
        >>>     net, hv_bus=0, lv_bus=1, name="trafo1", sn_mva=40, vn_hv_kv=110, vn_lv_kv=10, vk_percent=10,
        >>>     vkr_percent=0.3, pfe_kw=30, i0_percent=0.1, shift_degree=30
        >>> )
    """
    
    entries = {
        "name": name,
        "from_bus": from_bus,
        "to_bus": to_bus,
        "r_percent": r_percent,
        "x_percent": x_percent,
        "b_percent": b_percent,
        "shift_degree": shift_degree,
        "tap_min": tap_min,
        "tap_max": tap_max,
        "num_taps": num_taps,
        "tap_pos": tap_pos,
        "in_service": in_service
    }
    
    _set_entries(net, "trafo", entries=entries)