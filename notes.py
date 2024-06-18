from subjects import subjects_data
from statistics_collection import dataSort
from const import header_start
from const import end_of_header
worktime = {}
veb = {}

def clearNote(sht_id):
    note = [
    {
      "updateCells": {
        "range": {
          "sheetId": sht_id
        },
        "fields": "userEnteredFormat"
      }
    },
    {
      "updateCells": {
        "range": {
          "sheetId": sht_id
        },
        "fields": "userEnteredValue"
      }
    },
        {'unmergeCells': {"range": {
          "sheetId": sht_id
        }}}
    ]
    return note

def Notestart(sub):
    note = [{'mergeCells':
          {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                     'startRowIndex': 0,
                     'endRowIndex': 2,
                     'startColumnIndex': 0,
                     'endColumnIndex': 3
                     },
           'mergeType': 'MERGE_COLUMNS'
           }
      },
      {'repeatCell':
          {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                     'startRowIndex': 0,
                     'endRowIndex': 2,
                     'startColumnIndex': 0,
                     'endColumnIndex': 3
                     },

           'cell': {'userEnteredFormat':
                        {'backgroundColor': {'red': 1, 'green': 0.749, 'blue': 0.5019},
                         'horizontalAlignment': 'CENTER',
                         'verticalAlignment': 'MIDDLE',
                         'textFormat': {'bold': True}
                         }},
           'fields': 'userEnteredFormat'}
      }
    ]
    return note

def Notemake(sub, start_col, flag, note):
    if flag > 0:
        note.append(
            {'mergeCells': {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                                      'startRowIndex': 0,
                                      'endRowIndex': 1,
                                      'startColumnIndex': start_col,
                                      'endColumnIndex': start_col + 3
                                      },
                            'mergeType': 'MERGE_ALL'}
             }
        )
        note.append(
            {'repeatCell':
                 {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                            'startRowIndex': 0,
                            'endRowIndex': 2,
                            'startColumnIndex': start_col,
                            'endColumnIndex': start_col + 3
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
    elif flag < 0:
        note.append(
            {'mergeCells': {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                                      'startRowIndex': 0,
                                      'endRowIndex': 2,
                                      'startColumnIndex': start_col,
                                      'endColumnIndex': start_col + 1
                                      },
                            'mergeType': 'MERGE_ALL'}
             }
        )
        note.append(
            {'repeatCell':
                 {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                            'startRowIndex': 0,
                            'endRowIndex': 2,
                            'startColumnIndex': start_col,
                            'endColumnIndex': start_col + 1
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
        note.append(
            {'mergeCells': {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                                      'startRowIndex': 0,
                                      'endRowIndex': 2,
                                      'startColumnIndex': start_col,
                                      'endColumnIndex': start_col + 1
                                      },
                            'mergeType': 'MERGE_ALL'}
             }
        )
        note.append(
            {'repeatCell':
                 {'range': {'sheetId': subjects_data[sub]['STAT_SHEET_ID'],
                            'startRowIndex': 0,
                            'endRowIndex': 2,
                            'startColumnIndex': start_col,
                            'endColumnIndex': start_col + 1
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

def note_collect(sub):
    global worktime, veb

    worktime = subjects_data[sub]['worktime']
    veb = subjects_data[sub]['veb']

    wrk_tm_for_header = worktime["24/7"] + worktime["11-20"] + worktime["09-00"]
    sort_wrk_tm_for_header = dataSort(wrk_tm_for_header)
    header = header_start + sort_wrk_tm_for_header + end_of_header
    under_header = ['', '', '']
    start_col = 3

    setNote = Notestart(sub)

    for head in header:
        if (head in veb["9-15"]) or (head in veb["15:30-21:30"]) or (head in worktime["24/7"]):
            under_header = under_header + ['ночь', 'ВЕБ', 'ПБ без веба']
            Notemake(sub, start_col, 1, setNote)
            start_col += 3
            header.insert(header.index(head) + 1, '')
            header.insert(header.index(head) + 1, '')
        elif head > '' and header.index(head) > 2:
            under_header += ['']
            if head in sort_wrk_tm_for_header:
                Notemake(sub, start_col, -1, setNote)
            else:
                Notemake(sub, start_col, 0, setNote)
            start_col += 1
    return setNote