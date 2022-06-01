import json
import pandas as pd
import pygsheets
import datetime



def push_data(search_engine, group_folder=None):


    service_file_path = 'pysheets-347309-e1fa5df88a49.json'
    spreadsheet_id = '1eGyrkQiRhY3evJdmVo4czQHLJ3w6uRSn3pffXLvTLdA'
    data_path, sheet_name = '', ''

    if group_folder == None:
        sheet_name = search_engine
        data_path = f'topvisor_data/summary_chart/None_summary_chart-{search_engine}-{datetime.date.today()}.json'
    else:
        sheet_name = str(f'{search_engine}-{group_folder}')
        data_path = f'topvisor_data/summary_chart/{group_folder}_summary_chart-{search_engine}-{datetime.date.today()}.json'

    data = json.load(open(data_path, encoding='utf-8'))

    avg_fix = []
    vis_fix = []

    for item in data['result']['seriesByProjectsId']['4944800']['avg']:
        change = str(item).replace('.', ',')
        avg_fix.append(change)

    for item in data['result']['seriesByProjectsId']['4944800']['visibility']:
        change = str(item).replace('.', ',')
        vis_fix.append(change)

    df = pd.DataFrame(
        {   "dates": data['result']['dates'],
            "vis_fix": vis_fix,
            "avg_fix": avg_fix,
            "all": data['result']['seriesByProjectsId']['4944800']['tops']['all'],
            "1_3": data['result']['seriesByProjectsId']['4944800']['tops']['1_3'],
            "1_10": data['result']['seriesByProjectsId']['4944800']['tops']['1_10'],
            "11_30": data['result']['seriesByProjectsId']['4944800']['tops']['11_30']
            }
        )


    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1',None,'*')
    wks_write.set_dataframe(df, (1,1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1

def main():

    group_folders_id = {"iphone": 861539, "ipad": 861590, "mac": 861565, "airpods": 861562, "iwatch": 861584,
                        "accs": 861573}

    search_engines = ['yandex', 'google']

    for engine in search_engines:
        push_data(engine)
        print(f'complete adding total {engine} data')

    for key in group_folders_id:
        for engine in search_engines:
            push_data(engine, key)
            print(f'complete adding {engine}-{key} data')


if __name__ == '__main__':
    main()