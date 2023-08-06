def cria_list_with_dicts(data):
    result = list()

    for x in data:
        linha = dict()
        
        linha["paciente_id"] = int(x[0])
        linha["cep"] = x[2]
        linha["endereco"] = x[1]
        linha["bairro"] = x[3]
        linha["codmunicipioibge"] = x[6]
        linha["municipio"] = int(x[4])
        linha["uf"] = x[5]
        
        result.append(linha)

    return result

def for_dict(x):

    result = {}

    try:
        result["p_id"] = int(x[0])
    except:
        result["p_id"] = 0

    result["cep"] = x[2]
    result["endereco"] = x[1]
    result["bairro"] = x[3]

    try:
        result["codmunicipioibge"] = int(x[6])
    except:
        result["codmunicipioibge"] = 0
    
    result["municipio"] = x[4]
    result["uf"] = x[5]

    return result