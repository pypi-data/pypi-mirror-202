import requests, json
from tableau_api_lib import TableauServerConnection
from utilities import aws_helper

SERVER_URL='https://tableau.tools.pomelo.la'
SERVER_API_VERSION='3.15'
SITE_NAME='Pomelo'

def login_into_server():
    SECRET_TABLEAU = aws_helper.get_secrets(
        "arn:aws:secretsmanager:us-east-1:644197204120:secret:data/bi/tableau_credentials-1PfxO7",
        "us-east-1")
    print(SECRET_TABLEAU)

    config = {
        'tableau_prod': {
            'server': '{}'.format(SERVER_URL),
            'api_version': '{}'.format(SERVER_API_VERSION),
            'username': '{}'.format(SECRET_TABLEAU.get('tableau_credential_user')),
            'password': '{}'.format(SECRET_TABLEAU.get('tableau_credential_pass')),
            'site_name': '{}'.format(SITE_NAME),
            'site_url': '',
            'server_metadata_url': "lala"
        }
    }

    # Server specifications, certificates and credentials
    server_base_url = '{}'.format(config['tableau_prod']['server'])
    server_api_version = '{}'.format(config['tableau_prod']['api_version'])
    server_rest_url = server_base_url + "/api/" + server_api_version
    #server_metadata_url = server_base_url + "/api/metadata/graphql"
    name = '{}'.format(config['tableau_prod']['username'])
    password = '{}'.format(config['tableau_prod']['password'])
    ##### Sign in through the REST API first, to the default site #####
    # Which we do to obtain an access token
    print("Signing in through REST API")
    request_url = server_rest_url + "/auth/signin"
    print("URL for sign-in: \"" + request_url + "\"")
    payload = {"credentials": {"name": name,"password": password, "site": {"contentUrl": ""}}}
    headers = {"accept": "application/json", "content-type": "application/json"}
    r = requests.post(request_url, json=payload, headers=headers)
    r.raise_for_status()
    # Get the token!
    r_json = json.loads(r.content)
    token = r_json["credentials"]["token"]
    print(token)
    site_id = r_json["credentials"]["site"]["id"]
    print(site_id)

        ##### We"re done #####
    #print("Signing out")
    #request_url = server_base_url + "/auth/signout"
    #r = requests.post(request_url, headers=headers)

    print(config['tableau_prod']['api_version'])
    conn = TableauServerConnection(config, env='tableau_prod')
    conn.sign_in()
    print(conn.site_id)
    return conn

def get_data_graphql(query,conn):
   return conn.metadata_graphql_query(query).json()