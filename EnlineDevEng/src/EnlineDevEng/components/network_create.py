

from EnlineDevEng.utils.auxiliary import EnlineDevEngNet
from EnlineDevEng.utils.network_structure import get_struture_dict



def create_empty_network(
    name: str | None = None,
    f_hz: float = 60.0,
    sn_mva: float = 100.0 
) -> EnlineDevEngNet:
    
    
    """
    Esta Função inicializa a estrutura de dados do EnlineDevEng.
    
    Parâmetros:
        f_hz: frequência do sistema em Hertz
        name: nome do sistema
        sn_mva: Potência aparente base
    
    Returns:
        net = dicionário de atributos EnlineDevEng com tabelas
        vazias
    
    Example:
        >>> net = create_empty_network()
    """
    
    
    network_structure_dict = get_struture_dict()
    network_structure_dict["name"]   = name 
    network_structure_dict["f_hz"]   = f_hz
    network_structure_dict["sn_mva"] = sn_mva

    net = EnlineDevEngNet(EnlineDevEngNet.create_dataframes(network_structure_dict))
    
    return net