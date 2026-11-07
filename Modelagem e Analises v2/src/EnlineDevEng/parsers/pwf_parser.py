


from dataclasses import dataclass, field
from pathlib import Path 
from typing import Dict
from EnlineDevEng.core import BaseNetworkParser

from EnlineDevEng.parsers.pwf_auxiliar import *
from EnlineDevEng.utils.auxiliary import EnlineDevEngNet


@dataclass
class DadosRedePWF:
    """Dados da rede extraídos de um arquivo PWF."""
    
    codigos: Dict[str, bool] = field(default_factory=lambda: {
        "TITU": False, "DAGR": False, "DANC": False, "DARE": False, "DBAR": False, 
        "DBSH": False, "DCAR": False, "DCBA": False, "DCCV": False, "DCER": False, 
        "DCLI": False, "DCNV": False, "DCSC": False, "DCTE": False, "DCTG": False, 
        "DCTR": False, "DELO": False, "DGBT": False, "DGER": False, "DGLT": False, 
        "DINC": False, "DINJ": False, "DLIN": False, "DMET": False, "DMFL": False, 
        "DMTE": False, "DOPC": False, "DSHL": False, "DTPF": False, "DAEB": False
    })
                            
    # Palavras-chave de arquivo .pwf
    fim_linha     = "\n"
    caractere_fim = "FIM"
    fim_bloco     = ("9999", "99999", "999999")
    comentario    = "("
            
                        
    path_pwf:    Path 
    linhas: list[str] = field(default_factory=list)
    idx_linha: int = 0
    



class PWFNetworkParser(BaseNetworkParser):
    """
    Parser para arquivos de rede no formato ANAREDE (.pwf)
    """
    
    extensions = ["pwf"]
    
    def parse(
        self,
        net: EnlineDevEngNet,
        filepath: Path,
        encoding: str = "latin-1"
    ):
        
        filepath = Path(filepath)
        self.rede = DadosRedePWF(path_pwf=filepath)
        
        # Anexa o objeto de dados 
        net.DadosRede = self.rede
        
        
        # Ler Arquivo
        self.rede.linhas = self.rede.path_pwf.read_text(
                            encoding=encoding).splitlines()
        
        
        # Extração 
        while self.rede.linhas[self.rede.idx_linha] != self.caractere_fim:
            linha = self.rede.linhas[self.rede.idx_linha].strip()
            linha_atual_completa = self.rede.linhas[self.rede.idx_linha][:]
            linha_proxima_completa = self.rede.linhas[self.rede.idx_linha + 1][:]
            linha_proxima_3 = self.rede.linhas[self.rede.idx_linha + 3][:]
            
            
          
                   
            # # Dados de fatores de alteração do nível de geração ativa do sistema
            # if linha in ("DBSH", "DBSH IMPR"):
                
            #     self.rede.dbsh  = dict()
            #     self.rede.dbsh1  = dict()
            #     self.rede.dbsh2  = dict()
            #     self.rede.dbsh["dbsh"]   = linha
            #     self.rede.dbsh1["ruler"] = linha_proxima_completa
            #     self.rede.dbsh2["ruler"] = linha_proxima_3
            #     self.rede.idx_linha += 1
            #     dbsh(self.rede)
                            
            
            # # Dados de fatores de alteração do nível de geração ativa do sistema
            # elif linha in ("DAGA", "DAGA IMPR"):
                
            #     self.rede.daga  = dict()
            #     self.rede.daga["daga"]   = linha
            #     self.rede.daga["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     daga(self.rede)
                
                            
            # # Dados Barra CA
            # elif linha in ("DAEB", "DAEB IMPR"):
                
            #     self.rede.daeb  = dict()
            #     self.rede.daeb["daeb"]   = linha
            #     self.rede.daeb["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     daeb(self.rede)
                            
                            
            # # Dados agregadores genéricos
            # elif linha in ("DAGR", "DAGR IMPR"):
                
            #     self.rede.dagr  = dict()
            #     self.rede.dagr1 = dict()
            #     self.rede.dagr2 = dict()
            #     self.rede.dagr["dagr"]   = linha
            #     self.rede.dagr1["ruler"] = linha_proxima_completa
            #     self.rede.dagr2["ruler"] = linha_proxima_3
            #     self.rede.idx_linha += 1
            #     dagr(self.rede)
                
            
            # # Dados de Alteração do Nível de Carregamento
            # elif linha in ("DANC", "DANC IMPR", "DANC ACLS", "DANC ACLS IMPR"):
                
            #     self.rede.danc = dict()
            #     self.rede.danc["danc"]  = linha_atual_completa
            #     self.rede.danc["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
                
            #     if "ACLS" in linha:
            #         danc_acls(self.rede)
                
            #     else:
            #         danc(self.rede)
                
            # # Dados de Intercâmbio de Potência Ativa entre areas
            # elif linha in ("DARE", "DARE IMPR"):
                
            #     self.rede.dare          = dict()
            #     self.rede.dare["dare"]  = linha_atual_completa
            #     self.rede.dare["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dare(self.rede)
                
            # Dados de Barra
            if linha in ("DBAR", "DBAR IMPR"):
                
                self.rede.dbar          = dict()
                self.rede.dbar["dbar"]  = linha_atual_completa
                self.rede.dbar["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dbar(self.rede)
            
            # # Dados de Args de Dados de carga
            # elif linha in ("DCAR", "DCAR IMPR"):
                
            #     self.rede.dcar = dict()
            #     self.rede.dcar["dcar"] = linha_atual_completa
            #     self.rede.dcar["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcar(self.rede)
                
            # # Dados de Barras CC
            # elif linha in ("DCBA", "DCBA IMPR"):
                
            #     self.rede.dcba = dict()
            #     self.rede.dcba["dcba"] = linha_atual_completa
            #     self.rede.dcba["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcba(self.rede)
                
            # # Dados de Controle de Conversor CA/CC
            # elif linha in ("DCCV", "DCCV IMPR"):

            #     self.rede.dccv = dict()
            #     self.rede.dccv["dccv"] = linha_atual_completa
            #     self.rede.dccv["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dccv(self.rede)
            
            # # Dados de Compensadores Estaticos de Potencia Reativa
            # elif linha in ("DCER", "DCER IMPR"):
                
            #     self.rede.dcer = dict()
            #     self.rede.dcer["dcer"] = linha_atual_completa
            #     self.rede.dcer["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcer(self.rede)
                
            # # Dados de Linha CC
            # elif linha in ("DCLI", "DCLI IMPR"):
                
            #     self.rede.dcli = dict()
            #     self.rede.dcli["dcli"] = linha_atual_completa
            #     self.rede.dcli["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcli(self.rede)
            
            # # Dados de Conversor CA/CC
            # elif linha in ("DCNV", "DCNV IMPR"):
                
            #     self.rede.dcnv = dict()
            #     self.rede.dcnv["dcnv"] = linha_atual_completa
            #     self.rede.dcnv["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcnv(self.rede)
                
            # # Dados de Compensador Serie Controlavel
            # elif linha in ("DCSC", "DCSC IMPR"):
                
            #     self.rede.dcsc = dict()
            #     self.rede.dcsc["dcsc"] = linha_atual_completa
            #     self.rede.dcsc["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dcsc(self.rede)
                
            # Dados de Constantes
            elif linha in ("DCTE", "DCTE IMPR"):
                
                self.rede.dcte = dict()
                self.rede.dcte["dcte"] = linha_atual_completa
                self.rede.dcte["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dcte(self.rede)
        
            # # Dados de Contingências
            # elif linha in ("DCTG", "DCTG IMPR"):
                
            #     self.rede.dctg = dict()
            #     self.rede.dctg1 = dict()
            #     self.rede.dctg2 = dict()
            #     self.rede.dctg["dctg"] = linha_atual_completa
            #     self.rede.dctg1["ruler"] = linha_proxima_completa
            #     self.rede.dctg2["ruler"] = linha_proxima_3
            #     self.rede.idx_linha += 1
            #     dctg(self.rede)
                
            # # Dados Complementares de Transformadores
            # elif linha in ("DCTR", "DCTR IMPR"):
                
            #     self.rede.dctr = dict()
            #     self.rede.dctr["dcte"] = linha_atual_completa
            #     self.rede.dctr["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dctr(self.rede)
                
            # # Dados de Elo CC
            # elif linha in ("DELO", "DELO IMPR"):
                
            #     self.rede.delo = dict()
            #     self.rede.delo["delo"] = linha_atual_completa
            #     self.rede.delo["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     delo(self.rede)
                
            # Dados de Grupo de Base de Tensão de Barras CA
            elif linha in ("DGBT", "DGBT IMPR"):
                
                self.rede.dgbt = dict()
                self.rede.dgbt["dgbt"] = linha_atual_completa
                self.rede.dgbt["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dgbt(self.rede)
                
            # Dados de Geradores
            elif linha in ("DGER", "DGER IMPR"):
                
                self.rede.dger = dict()
                self.rede.dger["dger"] = linha_atual_completa
                self.rede.dger["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dger(self.rede)
                
            # Dados de Grupos de Limite de Tensão
            elif linha in ("DGLT", "DGLT IMPR"):
                
                self.rede.dglt = dict()
                self.rede.dglt["dglt"] = linha_atual_completa
                self.rede.dglt["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dglt(self.rede)
                
            # # Dados de Incremento do Nível de Carregamento
            # elif linha in ("DINC", "DINC IMPR"):
                
            #     self.rede.dinc = dict()
            #     self.rede.dinc["dinc"] = linha_atual_completa
            #     self.rede.dinc["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dinc(self.rede)
                
            # # Dados de Injecoes de Potencias, Shunts e Fatores de Participacao de Geracao do Modelo Equivalente
            # elif linha in ("DINJ", "DINJ IMPR"):
                
            #     self.rede.dinj = dict()
            #     self.rede.dinj["dinj"] = linha_atual_completa
            #     self.rede.dinj["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dinj(self.rede)

            # Dados de Barra CA
            elif linha in ("DLIN", "DLIN IMPR"):
                
                self.rede.dlin = dict()
                self.rede.dlin["dlin"] = linha_atual_completa
                self.rede.dlin["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dlin(self.rede)
            
            # # Dados de Monitoração para Estabilidade de tensão em Barra CA
            # elif linha in ("DMET", "DMET IMPR"):
                
            #     self.rede.dmet = dict()
            #     self.rede.dmet["dmet"] = linha_atual_completa
            #     self.rede.dmet["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dmet(self.rede)
                
            # # Dados de Monitoração de Fluxo em Circuito CA
            # elif linha in ("DMFL", "DMFL IMPR", "DMFL CIRC", "DMFL CIRC IMPR"):
                
            #     self.rede.dmfl = dict()
            #     self.rede.dmfl["dmfl"] = linha_atual_completa
            #     self.rede.dmfl["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     if "CIRC" in linha_atual_completa.strip():
            #         dmfl_circ(self.rede)
            #     else:
            #         dmfl(self.rede)
            
            # Dados de Opcoes de Controle e Execucao Padrao
            elif linha in ("DOPC", "DOPC IMPR"):
                
                self.rede.dopc = dict()
                self.rede.dopc["dopc"] = linha_atual_completa
                self.rede.dopc["ruler"] = linha_proxima_completa
                self.rede.idx_linha += 1
                dopc(self.rede)
                
            # # Dados de Dispositivos Shunt de Circuito CA
            # elif linha in ("DSHL", "DSHL IMPR"):
                
            #     self.rede.dshl = dict()
            #     self.rede.dshl["dshl"] = linha_atual_completa
            #     self.rede.dshl["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     dshl(self.rede)
                
            # # Dados de controle de tensão por variação de tap
            # elif linha in ("DTPF", "DTPF IMPR", "DTPF CIRC", "DTPF CIRC IMPR"):
                
            #     self.rede.dtpf = dict()
            #     self.rede.dtpf["dtpf"] = linha_atual_completa
            #     self.rede.dtpf["ruler"] = linha_proxima_completa
            #     self.rede.idx_linha += 1
            #     if "CIRC" in linha_atual_completa:
            #         dtpf_circ(self.rede)
            #     else:
            #         dtpf(self.rede)
            
            # # Título do Sistema/Caso em Estudo
            # elif linha in ("TITU", "TITU IMPR"):
                
            #     self.rede.titu = dict()
            #     self.rede.titu["titu"] = linha_atual_completa
            #     self.rede.titu["ruler"] = linha_proxima_completa
            #     self.rede.codigos["TITU"] = True
            #     self.rede.idx_linha += 1
            
            self.rede.idx_linha += 1 
        
            if linha_proxima_3 == "FIM":
                break
        
        print(f"\033[32mSucesso na leitura de arquivo '{self.rede.path_pwf.name}'!\033[0m")
        
        # Checa alteração do nível de carregamento
        # checkdanc(self.rede)
        
        # Tratamento dos dados
        PosProcessadorPWF().processar(rede=self.rede)
        
        
        
        
        
        
        
        