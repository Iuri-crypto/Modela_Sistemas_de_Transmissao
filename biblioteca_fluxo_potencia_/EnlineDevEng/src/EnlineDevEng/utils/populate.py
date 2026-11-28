




def _set_entries(
    net, table, entries: dict
):
    
    """
    Adiciona as informações de entries na tabela table.
    """
    
    if net[table].empty:
        index = 0
    else:
        index = int(net[table].index.max()) + 1

    for col, val in entries.items():
        net[table].at[index, col] = val