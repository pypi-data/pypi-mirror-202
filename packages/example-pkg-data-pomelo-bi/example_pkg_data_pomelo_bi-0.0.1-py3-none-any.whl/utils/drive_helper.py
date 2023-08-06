import pygsheets
import json
from google.oauth2 import service_account
import numpy as np
from utilities import aws_helper


# Aclaración: Para poder acceder al archivo, se debe compartir previamente a la cuenta "datalake@datalake-344912.iam.gserviceaccount.com"
# GSheet no debe tener nombres de columnas con acentos y/o simbolos
def get_data_google_sheet(name_file, sheet_index):
    json_file = aws_helper.get_file_s3('use1-prd-infrastructure-datalake-s3','code/google/credentials.json')
    SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
    service_account_info = json.loads(json_file)
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

    gc = pygsheets.authorize(custom_credentials=my_credentials)
    #Get Gsheet file
    sh = gc.open(name_file)
    #Get page from GSheet
    wks = sh[sheet_index]
    #Convert to DataFrame
    df = wks.get_as_df()
    df = df.rename(str.lower, axis='columns')
    df.columns = df.columns.str.replace(' ', '_')
    df = df.replace(r'^\s*$', np.nan, regex=True)
    return df.astype(str)


