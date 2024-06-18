import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account


CREDENTIALS_FILE = 'google_account.json'  # имя файла с закрытым ключом

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, CREDENTIALS_FILE)

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials).spreadsheets() #.values()
#------------------------------------------------------------

def clear_sht(SAMPLE_SPREADSHEET_ID, clearNote):
    #print('-------------Очистка-------------данных--------------')
    request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={"requests": clearNote})
    response = request.execute()
    #print('ok')

def update_sht(SAMPLE_SPREADSHEET_ID, body):
    #print('-------------Обновление-------------данных-------------')
    request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body)
    response = request.execute()
    #print('ok')

def values_update_sht(SAMPLE_SPREADSHEET_ID, body):
    #print('-------------Обновление-------------данных-------------')
    request = service.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body)
    response = request.execute()