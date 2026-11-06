




def _set_entries(
    net, table, entries: dict
):
    
    """
    Adiciona as informações de entries na tabela table.
    """
    
    for col, val in entries.items():
        index = net[table].index.max() + 1
        net[table].at[index, col] = val 