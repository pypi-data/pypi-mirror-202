# Retrieve API Response for the word you send in
# v1.0.1

def MW_Response(word):
    import os
    from dotenv import load_dotenv
    from urllib import parse, request
    import json

    # Load environment variables needed for API call

    # Set the default path for the .env file in the project directory
    DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), '.env')

    #Check system variable for custom env path
    PC_VAR = os.environ.get('MW_API_PARSER_CONFIG')

    if PC_VAR is not None:
        config_path = os.path.join(PC_VAR, ".env")
        # Make sure there are no back-slashes
        config_path = config_path.replace('\\', '/')
    else:
        config_path = DEFAULT_CONFIG_PATH

    # Load the env file
    load_dotenv(config_path)

    ref = os.getenv('MW_API_REF')
    key = os.getenv('MW_API_KEY')

    # Perform the API call
    uri = f"https://dictionaryapi.com/api/v3/references/{parse.quote(ref)}/json/{parse.quote(word)}?key={parse.quote(key)}"

    response = request.urlopen(uri)
    raw_data = response.read()
    encoding = response.info().get_content_charset('utf8')  # JSON default
    data = json.loads(raw_data.decode(encoding))
    return data
