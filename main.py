import csv
import gspread
import httplib2
import googleapiclient.discovery
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from statistics_collection import collect
from subjects import eng
from subjects import subjects_data
from data_download import downloader
from data_upload import clear_sht
from data_upload import update_sht
from data_upload import values_update_sht
from notes import clearNote
from notes import note_collect





#gc = gspread.service_account(filename='google_account.json')
'''
CREDENTIALS_FILE = 'google_account.json'  # имя файла с закрытым ключом

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, CREDENTIALS_FILE)

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials).spreadsheets() #.values()
'''
#------------------------------------------------------------

for sub in subjects_data.keys():
    flag = 0
    print(subjects_data[sub]['find_info'])
    downloader(subjects_data[sub]['spreadsheet_id'], 'Кураторы', f'{subjects_data[sub]["file_path"]}/cur.csv')

    for i in range(len(subjects_data[sub]['sheet_names'])):
        if flag == 0:
            flag = downloader(subjects_data[sub]['spreadsheet_id'], subjects_data[sub]["sheet_names"][i], f'{subjects_data[sub]["file_path"]}/{subjects_data[sub]["sheet_names"][i]}.csv')

    clear_sht(subjects_data[sub]['spreadsheet_id'], clearNote(subjects_data[sub]['STAT_SHEET_ID']))


    note = note_collect(sub)
    bodynote = {"requests": note}
    update_sht(subjects_data[sub]['spreadsheet_id'], bodynote)
    #data = [{"range": 'Статистика (ПБ)', "values": body}]
    #bodydata = {"valueInputOption": 'RAW', "data": data}



    #if sub != 'phys' and sub != 'rus_oge':
    body = collect(sub)
    data = [{"range": 'Статистика (ПБ)', "values": body}]
    bodydata = {"valueInputOption": 'RAW', "data": data}
    values_update_sht(subjects_data[sub]['spreadsheet_id'], bodydata)

'''



#-------------------------чисто англ-------------------------


# The ID and range of a sample spreadsheet.

SAMPLE_SPREADSHEET_ID = eng['spreadsheet_id']
SAMPLE_RANGE_NAME = 'Кураторы'
STAT_RANGE_NAME = 'Статистика (ПБ)'

# Call the Sheets API
result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
data_from_sheet = result.get('values', [])
with open('files/eng/cur.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data_from_sheet)
    file.close()

for i in range(len(eng['sheet_names'])):
    result = service.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=eng['sheet_names'][i]).execute()
    timetable_of_lists = result.get('values', [])
    with open(f'files/eng/{eng["sheet_names"][i]}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(timetable_of_lists[1:])
        file.close()


worktime = eng['eng_worktime']
veb = eng['eng_veb']

#---------------------------------------------------------------

clearNote = [
    {
      "updateCells": {
        "range": {
          "sheetId": 1234649449
        },
        "fields": "userEnteredFormat"
      }
    },
{
      "updateCells": {
        "range": {
          "sheetId": 1234649449
        },
        "fields": "userEnteredValue"
      }
    }
  ]
  
request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={"requests": clearNote})
response = request.execute()
#---------------------------------------------------------------


header = ["find_info", "ФИО", "ИФ из вк"]
end_of_header = ['Всего ночных', 'Всего во время веба', 'Всего ПБ без веба', 'Всего во время перерыва ПБ', 'Всего повышенных', 'Итоговая сумма']
wrk_tm_for_header = worktime["24/7"] + worktime["11-20"] + worktime["09-00"]
sort_wrk_tm_for_header = dataSort(wrk_tm_for_header)
header = header + sort_wrk_tm_for_header + end_of_header
under_header = ['','','']
start_col = 3

setNote =[{'mergeCells':
               {'range': {'sheetId': 1234649449,
                          'startRowIndex': 0,
                          'endRowIndex': 2,
                          'startColumnIndex': 0,
                          'endColumnIndex': 3
                          },
                'mergeType': 'MERGE_COLUMNS'
                }
           },
          {'repeatCell':
               {'range': {'sheetId': 1234649449,
                          'startRowIndex': 0,
                          'endRowIndex': 2,
                          'startColumnIndex': 0,
                          'endColumnIndex': 3
                          },

               'cell' : {'userEnteredFormat':
                     {'backgroundColor': {'red': 1, 'green': 0.749, 'blue': 0.5019},
                      'horizontalAlignment': 'CENTER',
                      'verticalAlignment': 'MIDDLE',
                      'textFormat': {'bold': True}
                      }},
               'fields': 'userEnteredFormat'}
           }
]


for head in header:
    #print(head)
    if (head in veb["9-15"]) or (head in veb["15:30-21:30"]) or (head in worktime["24/7"]):
        #print('1')
        under_header = under_header + ['ночь', 'ВЕБ', 'ПБ без веба']
        setNote.append(
            {'mergeCells': {'range': {'sheetId': 1234649449,
                                      'startRowIndex': 0,
                                      'endRowIndex': 1,
                                      'startColumnIndex': start_col,
                                      'endColumnIndex': start_col + 3
                                      },
                            'mergeType': 'MERGE_ALL'}
             }
        )
        
        setNote.append(
            {'repeatCell':
                 {'range': {'sheetId': 1234649449,
                            'startRowIndex': 0,
                            'endRowIndex': 2,
                            'startColumnIndex': start_col,
                            'endColumnIndex': start_col+3
                            },

                  'cell': {'userEnteredFormat':
                               {'backgroundColor': {'red': 1, 'green': 1, 'blue': 0.6},
                                'horizontalAlignment': 'CENTER',
                                'verticalAlignment': 'MIDDLE',
                                'textFormat': {'bold': True}
                                }},
                  'fields': 'userEnteredFormat'}
             }
        )
        #print(len(setNote))
        start_col += 3
        header.insert(header.index(head) + 1, '')
        header.insert(header.index(head) + 1, '')
    elif head > '' and header.index(head) > 2:
        #print('2')
        under_header += ['']
        setNote.append(
            {'mergeCells': {'range': {'sheetId': 1234649449,
                                      'startRowIndex': 0,
                                      'endRowIndex': 2,
                                      'startColumnIndex': start_col,
                                      'endColumnIndex': start_col + 1
                                      },
                            'mergeType': 'MERGE_ALL'}
             }
        )
        
        if head in sort_wrk_tm_for_header:
            setNote.append(
                {'repeatCell':
                     {'range': {'sheetId': 1234649449,
                                'startRowIndex': 0,
                                'endRowIndex': 2,
                                'startColumnIndex': start_col,
                                'endColumnIndex': start_col+1
                                },

                      'cell': {'userEnteredFormat':
                                   {'backgroundColor': {'red': 1, 'green': 1, 'blue': 0.6},
                                    'horizontalAlignment': 'CENTER',
                                    'verticalAlignment': 'MIDDLE',
                                    'textFormat': {'bold': True}
                                    }},
                      'fields': 'userEnteredFormat'}
                 }
            )
        else:
            setNote.append(
                {'repeatCell':
                     {'range': {'sheetId': 1234649449,
                                'startRowIndex': 0,
                                'endRowIndex': 2,
                                'startColumnIndex': start_col,
                                'endColumnIndex': start_col+1
                                },

                      'cell': {'userEnteredFormat':
                                   {'backgroundColor': {'red': 0.3254, 'green': 0.7764, 'blue': 0.549},
                                    'horizontalAlignment': 'CENTER',
                                    'verticalAlignment': 'MIDDLE',
                                    'wrapStrategy': 'WRAP',
                                    'textFormat': {'bold': True}
                                    }},
                      'fields': 'userEnteredFormat'}
                 }
            )
        #print(len(setNote))
        start_col += 1


#print(len(setNote))
#print(len(header))
#print(len(under_header))
request = service.batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body={"requests": setNote})
response = request.execute()



table = []
table.append(header)
table.append(under_header)


a = collect()

for row in a:
    table.append(row)


#table.append([3,4])
data = [{"range": STAT_RANGE_NAME, "values": table}]
body = {"valueInputOption": 'RAW', "data": data}
request = service.values().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body)
response = request.execute()
#eng_stat.update(table)


'''