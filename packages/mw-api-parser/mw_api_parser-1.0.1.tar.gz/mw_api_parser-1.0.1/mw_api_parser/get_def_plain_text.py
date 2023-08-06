# Retrieve the text from the MW API Response without formatting suggestions
#v1.0.1

def Get_Def_Plain_Text(data):

    import re
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

    plain_text = [re.sub(r'\{.*?\}', '', item) for item in definitions]

    return plain_text
