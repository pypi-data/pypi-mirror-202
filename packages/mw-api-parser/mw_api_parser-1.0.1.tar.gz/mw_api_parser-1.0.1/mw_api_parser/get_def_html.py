# Retrieve the definition and return it with HTML formatting
#v1.0.1

def Get_Def_HTML(data):
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

    bold_colon = '<b>:</b>'
    # Replace '{bc}' with the bold colon character in each string
    definitions = [string.replace('{bc}', bold_colon) for string in definitions]

    format_tags = {
        'b': 'b',
        'inf': 'sub',
        'it': 'i',
        'sc': 'smallcaps',
        'sup': 'sup',
    }

    # Replace the custom formatting tags with the corresponding HTML tags
    for tag, html_tag in format_tags.items():
        for i in range(len(definitions)):
            definitions[i] = re.sub(r'\{' + tag + r'\}(.*?)\{/' + tag + r'\}', r'<'+html_tag+r'>\1</'+html_tag+r'>', definitions[i])

        definitions = [string.replace('{ldquo}', '\u201C') for string in definitions]

        definitions = [string.replace('{rdquo}', '\u201D') for string in definitions]

    return definitions
