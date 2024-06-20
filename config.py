import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access to the settings in the config.ini file
API_KEY = config['settings']['api_key']
AUTH_URL = config['settings']['auth_url']
CLIENT_ID = config['settings']['client_id']
CLIENT_SECRET = config['settings']['client_secret']
BASE_URL = config['settings']['base_url']