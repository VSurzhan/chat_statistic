import csv
from subjects import subjects_data
from const import header_start
from const import end_of_header
from const import night_time
from const import day_time
from const import morning_veb_time
from const import evening_veb_time

worktime = {}
veb = {}


def dataSort(datas):
    may = []
    june = []
    for k in datas:
        if '.05.' in k:
            may.append(k)
        else:
            june.append(k)
    return sorted(may) + sorted(june)

def standartCount(curator, date, timetable):
    count = 0
    evt = 0
    mrvt = 0
    if date in veb['9-15']:
        mrvt = 1
    elif date in veb['15:30-21:30']:
        evt = 1
    try:
        #if date in timetable['data'].keys():
            #print('1: ', timetable['data'].keys())
            #k = timetable['data'].index(timetable['data'][date])

        if date.replace('.2024', '') in timetable['data'].keys():
            #print('2: ', timetable['data'].keys())
            #k = timetable['data'].index(timetable['data'][date.replace('.2024', '')])
            date = date.replace('.2024', '')
        elif date not in timetable['data'].keys():
            #print('Both of \'if\' are not working')
            return 0
    except KeyError:
        print('There is no such date in timetable')
        print(date)
        exit(0)

    #if curator == 'Кристина Куранда':
        #print('standart', date)

    for key in timetable.keys():
        #if curator == 'Кристина Куранда':
            #print('key', key)

        if date in timetable[key].keys():
            if mrvt:
                if (key in day_time) and (key not in morning_veb_time):
                    #if curator == 'Кристина Куранда':
                        #print(timetable[key][date])
                    for row in timetable[key][date]:
                        if curator == row:
                            count += 1
            elif evt:
                if (key in day_time) and (key not in evening_veb_time):
                    #if curator == 'Кристина Куранда':
                        #print(timetable[key][date])
                    for row in timetable[key][date]:
                        if curator == row:
                            count += 1
            else:
                if (key in day_time):
                    #if curator == 'Кристина Куранда':
                        #print(timetable[key][date])
                    for row in timetable[key][date]:
                        if curator == row:
                            count += 1
    return count

def nightCount(curator, date, timetable):
    count = 0
    #print(date)
    #print(date.replace('.2024', ''))
    #print('0: ', timetable['data'].keys())
    try:
        # if date in timetable['data'].keys():
        # print('1: ', timetable['data'].keys())
        # k = timetable['data'].index(timetable['data'][date])

        if date.replace('.2024', '') in timetable['data'].keys():
            # print('2: ', timetable['data'].keys())
            # k = timetable['data'].index(timetable['data'][date.replace('.2024', '')])
            date = date.replace('.2024', '')
        elif date not in timetable['data'].keys():
            # print('Both of \'if\' are not working')
            return 0
    except KeyError:
        print('There is no such date in timetable')
        exit(0)

    #if curator == 'Кристина Куранда':
        #print('night', date)

    for key in timetable.keys():
        #if curator == 'Кристина Куранда':
            #print('key', key)
        if (key in night_time) and (date in timetable[key].keys()):
            #if curator == 'Кристина Куранда':
                #print(timetable[key][date])
            for row in timetable[key][date]:
                if curator == row:
                    count += 1
    return count

def vebCount(curator, date, timetable):
    count = 0
    evt = 0
    mrvt = 0
    #print(veb['9-15'])
    if date in veb['9-15']:
        mrvt = 1
    elif date in veb['15:30-21:30']:
        evt = 1
    try:
        # if date in timetable['data'].keys():
        # print('1: ', timetable['data'].keys())
        # k = timetable['data'].index(timetable['data'][date])

        if date.replace('.2024', '') in timetable['data'].keys():
            # print('2: ', timetable['data'].keys())
            # k = timetable['data'].index(timetable['data'][date.replace('.2024', '')])
            date = date.replace('.2024', '')
        elif date not in timetable['data'].keys():
            # print('Both of \'if\' are not working')
            return 0
    except KeyError:
        print('There is no such date in timetable')
        exit(0)

    #if curator == 'Кристина Куранда':
        #print('veb', date)

    #if date == '05.06':
        #    print(mrvt)
    #    print(evt)

    for key in timetable.keys():
        #if curator == 'Кристина Куранда':
        #print('key', key)

        if mrvt:
            if (key in day_time) and (key in morning_veb_time):
                #if curator == 'Кристина Куранда':
                    #print(timetable[key][date])
                try:
                    for row in timetable[key][date]:
                        if curator == row:
                            count += 1
                except KeyError:
                    print(key, date, curator)
                    exit(1)
        elif evt:
            if (key in day_time) and (key in evening_veb_time):
                #if curator == 'Кристина Куранда':
                    # print(timetable[key][date])
                try:
                    for row in timetable[key][date]:
                        if curator == row:
                            count += 1
                except KeyError:
                    print(key, date, curator)
                    exit(2)
    return count

def tablebegin(sub):
    table = []
    with open(f'files/{sub}/cur.csv', "r", newline="") as file:
        curators = csv.reader(file)
        for row in curators:
            try:
                if row[0] != '' and row[0] != ' ' and row[0] != 'ФИО':
                    table.append([subjects_data[sub]['find_info']+str(row[0]), row[0], row[1]])
            except IndexError:
                break
    return table





def collect(sub):
    global worktime, veb

    worktime = subjects_data[sub]['worktime']
    veb = subjects_data[sub]['veb']
    table = tablebegin(sub)



    wrk_tm_for_header = worktime["24/7"] + worktime["11-20"] + worktime["09-00"]
    sort_wrk_tm_for_header = dataSort(wrk_tm_for_header)
    header = header_start + sort_wrk_tm_for_header + end_of_header
    under_header = ['','','']
    start_col = 3
    #print(header)
    #print(under_header)


    voc_for_sheet = {}
    for head in header:
        '''
        if (head in veb["9-15"]) or (head in veb["15:30-21:30"]) or (head in worktime["24/7"]):
            # print('1')
            under_header = under_header + ['ночь', 'ВЕБ', 'ПБ без веба']
            
            # print(len(setNote))
            start_col += 3
            header.insert(header.index(head) + 1, '')
            header.insert(header.index(head) + 1, '')
        elif head > '' and header.index(head) > 2:
            # print('2')
            under_header += ['']
            start_col += 1
        '''
        voc_for_sheet.update({head: head})

    #returntable = []
    #returntable.append(header)
    #returntable.append(under_header)
    #header = header_start + sort_wrk_tm_for_header + end_of_header
    #under_header = ['', '', '']
    #start_col = 3

    #print(voc_for_sheet)
    sht = []
    sht.append(voc_for_sheet)

    voc = {}
    for key in voc_for_sheet.keys():
        if (key in veb["9-15"]) or (key in veb["15:30-21:30"]) or (key in worktime['24/7']):
            under_header = under_header + ['ночь', 'ВЕБ', 'ПБ без веба']
            voc.update({key: ['ночь', 'ВЕБ', 'ПБ без веба']})
            #start_col += 3
            header.insert(header.index(key)+1, '')
            header.insert(header.index(key) + 1, '')
        #elif key > '' and header.index(key) > 2:
        else:
            if key > '' and header.index(key) > 2:
                under_header += ['']
            voc.update({key: ''})
            #start_col += 1

    sht.append(voc)
    #print(sht)
    #print(voc)
    #print(under_header)


    timetable = {'data': {}}
    for i in range(len(subjects_data[sub]['sheet_names'])):
        with open(f'files/{sub}/{subjects_data[sub]["sheet_names"][i]}.csv', 'r') as file:
            #print(subjects_data[sub]["sheet_names"][i])
            reader = csv.reader(file)
            next(reader)  # Пропускаем заголовок файла
            time = None
            #timetable = {}
            #subtimetable = {}
            flag = 1
            for row in reader:
                subtimetable = {}

                if subjects_data[sub]["sheet_names"][i] == '03.06-09.06 - ПБ ЕГЭ':
                    t = row
                if flag:
                    dates = row[1:]
                    flag = 0
                    for date in dates:
                        subtimetable.update({date: [row[dates.index(date)+1]]})
                    timetable['data'].update(subtimetable)
                    continue

                while len(row) < len(dates) + 1:
                    row.append('')

                try:
                    if row[0] != '':
                        for date in dates:               # проблема в том, что если последний столбец пуст в некотрой строке, то row становится короче на один столбец и в результате срабатывает исключение, time не обновляется
                            subtimetable.update({date: [row[dates.index(date)+1]]})
                        if row[0] in timetable.keys():
                            timetable[row[0]].update(subtimetable)
                        else:
                            timetable.update({row[0]: subtimetable})
                        time = row[0]
                    else:
                        for date in dates:
                            timetable[time][date].append(row[dates.index(date)+1])
                except IndexError:
                    #with open('files/error.csv', 'w+', newline='') as file:
                        #writer = csv.writer(file)
                        #writer.writerow('there was exception IndexError in file: ' + f'files/{sub}/{subjects_data[sub]["sheet_names"][i]}.csv' + '; the row was: ' + row)
                        #file.close()
                    #print('there was exception IndexError in file: ', f'files/{sub}/{subjects_data[sub]["sheet_names"][i]}.csv', '; the row was: ', row)
                    continue
                except KeyError:
                    #with open('files/error.csv', 'w+', newline='') as file:
                        #writer = csv.writer(file)
                        #writer.writerow('there was exception KeyError in timetable, file: ' + f'files/{sub}/{subjects_data[sub]["sheet_names"][i]}.csv' + '; the row was: ' + row)
                        #    file.close()
                    #print('there was exception KeyError in timetable, file: ', f'files/{sub}/{subjects_data[sub]["sheet_names"][i]}.csv', '; the row was: ', row)
                    continue

    #print(timetable)

    for row in table:
        vocab = {'find_info': row[0],
                 'ФИО': row[1],
                 'ИФ из вк': row[2]
                 }
        i = 0
        for key in voc.keys():
            if key in vocab.keys():
                #print('key: ', key)
                #print('vocab.keys(): ', vocab.keys())
                week = 0
                weekcount = 0
                no_pb_pay = 0
                night_pay = 0
                veb_pay = 0
                no_veb_pay = 0
                up_pay = 0
                continue
            elif key in wrk_tm_for_header:
                if voc[key] == '':                                                                                          # здесь заполняется кол-во смен в обычное время
                    a = standartCount(row[2], key, timetable)
                    vocab.update({key: a})
                    week += 1
                    weekcount += a
                    no_pb_pay += a
                else:                                                                                                       # здесь заполняется кол-во смен в разное время суток
                    a = nightCount(row[2], key, timetable)
                    b = vebCount(row[2], key, timetable)
                    c = standartCount(row[2], key, timetable)
                    vocab.update({key:
                                      {'ночь': a,
                                        'ВЕБ': b,
                                        'ПБ без веба': c
                                    }
                    })
                    week += 1
                    weekcount = weekcount + a + b + c
                    night_pay += a
                    veb_pay += b
                    no_veb_pay += c

                #if row[2] == 'Полина Артемова':
                    #print(week, weekcount, up_pay)
                if week == 7:
                    week = 0
                    if weekcount > 10:
                        up_pay = weekcount - 10
                    weekcount = 0
                end_list = [night_pay, veb_pay, no_veb_pay, no_pb_pay, up_pay, 125*night_pay+veb_pay*75+no_veb_pay*100+no_pb_pay*75+up_pay*25]
            else:
                vocab.update({key: end_list[i]})                                                                                      # здесь заполняется ИТОГ строки
                i += 1
        sht.append(vocab)




    subreturntable = []
    flag = 2
    for row in sht:
        if flag:
            flag -= 1
            continue
        subsubreturntable = []
        for key in row.keys():
            if isinstance(row[key], dict):

                for key2 in row[key].keys():
                    subsubreturntable.append(str(row[key][key2]))
            else:

                subsubreturntable.append(str(row[key]))
        subreturntable.append(subsubreturntable)

    returntable = []
    returntable.append(header)
    returntable.append(under_header)
    #print(header)
    #print(under_header)

    for row in subreturntable:
        returntable.append(row)

    return returntable


