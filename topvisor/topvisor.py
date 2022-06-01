import json
import requests
import os
import datetime

class Topvisor:

    def __init__(self):

        print('Authorizing Topvisor')
        self.user = '296177'
        self.key = 'c1414daa91881b0b278c'
        self.headers = {'Content-type': 'application/json', 'User-Id': self.user, 'Authorization': f'bearer {self.key}'}
        self.server = 'https://api.topvisor.com'
        self.date_today = str(datetime.date.today())
        # self.date_today = '2022-05-23'

        self.project_id = 4944800
        self.region_index = {"yandex": 3, "google": 6}
        self.dates = ['2022-01-10', '2022-05-19']


        if not os.path.exists("topvisor_data/projects/"):
            os.mkdir("topvisor_data/projects/")

        if not os.path.exists("topvisor_data/2022-05-23/summary_chart/"):
            os.mkdir("topvisor_data/2022-05-23/summary_chart/")

        if not os.path.exists("topvisor_data/folders/"):
            os.mkdir("topvisor_data/folders/")
        #
        # if not os.path.exists(f'/topvisor/topvisor_data/{self.date_today}/summary_chart/yandex/'):
        #     os.mkdir(f'/topvisor_data/{self.date_today}/summary_chart/yandex/')
        #
        # if not os.path.exists(f'/topvisor/topvisor_data/{self.date_today}/summary_chart/google/'):
        #     os.mkdir(f'/topvisor_data/{self.date_today}/summary_chart/google/')

    def get_projects(self):

        payload = {
            "show_site_stat": True,
            "show_searchers_and_regions": True
        }

        api_path = '/v2/json/get/projects_2/projects'

        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

        with open(f'topvisor_data/projects/projects-{datetime.date.today()}.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        if response:
            print(f'Data succesfully collected')

        return response.json()


    def get_summary_chart(self, search_engine: str):

        api_path = '/v2/json/get/positions_2/summary_chart'

        payload = {
            "project_id": 	self.project_id,
            "region_index": self.region_index[search_engine],
            "date1" : self.dates[0],
            "date2" : self.dates[-1],
            "type_range": 0,
            "show_visibility": True,
            "show_avg": True,
            "show_tops": True
        }

        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

        print(f'Requesting Topvisor - {search_engine}')
        if response.status_code == 200:
            print(f'Response successful')
        else:
            print(f'{str(response.status_code)} - Happens')

        with open(f'topvisor_data/{datetime.date.today()}/summary_chart/{search_engine}/summary_chart.json', "w", encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()


    def get_group_summary_chart(self, search_engine: str, group_folder_name: str, group_folder_id: int):

        api_path = '/v2/json/get/positions_2/summary_chart'

        if not os.path.exists(f'topvisor_data/{datetime.date.today()}/summary_chart/{str(search_engine)}/'):
            os.mkdir(f'topvisor_data/{datetime.date.today()}/summary_chart/{str(search_engine)}/')

        payload = {
            "project_id": 	self.project_id,
            "region_index": self.region_index[search_engine],
            "date1" : self.dates[0],
            "date2" : self.dates[-1],
            "type_range": 0,
            "show_visibility": True,
            "show_avg": True,
            "show_tops": True,
            "filters": [
                {
                    "name": "group_folder_id",
                    "operator": "EQUALS",
                    "values": [
                        group_folder_id
                    ]
                }
            ],
            "group_folder_id_depth": "1"
        }

        response = requests.post(f'{self.server}{api_path}', headers=self.headers, data=json.dumps(payload))

        print(f'Requesting Topvisor - {search_engine}: {group_folder_name}')
        if response.status_code == 200:
            print(f'Response successful')
        else:
            print(f'{str(response.status_code)} - Happens')

        with open(f'topvisor_data/{datetime.date.today()}/summary_chart/{search_engine}/summary_chart_{group_folder_name}.json', "w",
                  encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()


if __name__ == '__main__':

    tv = Topvisor()
    tv.get_summary_chart('yandex')

