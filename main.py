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
    
    body = collect(sub)
    data = [{"range": 'Статистика (ПБ)', "values": body}]
    bodydata = {"valueInputOption": 'RAW', "data": data}
    values_update_sht(subjects_data[sub]['spreadsheet_id'], bodydata)
