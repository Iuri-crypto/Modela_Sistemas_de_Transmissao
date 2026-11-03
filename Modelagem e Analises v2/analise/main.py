
 

import os
import subprocess 
subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

from modelos_eletricos import CriarRede

rede = CriarRede(
    saida_simulacoes="resultados",
    salvar_dados_barra=True,
    salvar_dados_linha=True,
    snapshot=True,
)

net = rede.despachar_modelagem()
rede.fluxo_de_potencia(net)


