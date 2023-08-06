# Retrieve the native text from the definitions section of the MW API Response
#v1.0.1

def Get_Def_Original(data):
    definitions = []
    for i in range(0, len(data)):
        for y in range(0, (len(data[i]['def']))):
            for sense in data[i]['def'][y]['sseq']:
                for item in sense:
                    if item[0] == "sense":
                        for subitem in item[1]['dt']:
                            if subitem[0] == "text":
                                definitions.append(subitem[1])
                            elif subitem[0] == "vis":
                                for subsubitem in subitem[1]:
                                    if subsubitem.get('t'):
                                        definitions.append(subsubitem['t'])

    return definitions
