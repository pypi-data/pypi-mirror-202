# Creates hyperlinks for Merriam-Webster API
#v1.0.1

def Build_Audio_Links(data):
    audio_name = []
    SubDirs = []
    audio_links = []
    OtherChars = ['.', '-', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    base_url = "https://media.merriam-webster.com/audio/prons/"
    language_code = 'en'
    country_code = 'us'
    file_type = 'MP3'

    # Get name of audio file
    for i in range(len(data)):
        if 'prs' in data[i]['hwi']:
             for x in range(len(data[i]['hwi']['prs'])):
                if 'sound' in data[i]['hwi']['prs'][x]:
                    audio_name.append(data[i]['hwi']['prs'][x]['sound']['audio'])

    # Determine link for each item in "audio_name"
    for item in audio_name:
        item_list = list(item)

        f3 = item_list[:3]


        if f3 == "bix":
            SubDirs = 'bix'
        elif f3[:2] == "gg":
            SubDirs = 'gg'
        elif any(char in f3 for char in OtherChars):
            SubDirs = "number"
        else:
            SubDirs = f3[:1]

        link = base_url + language_code + '/' + country_code + '/' + file_type + '/' + str(SubDirs) + '/' + str(item) + '.' + file_type

        audio_links.append(link)

    return audio_links

