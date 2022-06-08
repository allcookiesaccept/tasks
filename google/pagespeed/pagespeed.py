# https://www.danielherediamejias.com/pagespeed-insights-api-with-python/

import requests, json, datetime, os, csv
from google.pagespeed import fieldnames

class Pagespeed:

    def __init__(self):

        if not os.path.exists('../../google/pagespeed/responses/'):
            os.mkdir('../../google/pagespeed/responses/')

        if not os.path.exists(f'../../google/pagespeed/responses/{str(datetime.date.today())}/'):
            os.mkdir(f'../../google/pagespeed/responses/{str(datetime.date.today())}/')

        self.api_key = 'AIzaSyAS0T1AZklHW38u4c38j95o2LT8CkNV0j4'
        self.locale = 'locale=ru'
        self.google_api_url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='


    def get_response(self, url: str, strategy: str):

        strategy = f'strategy={strategy}'
        api_request_url = f'{self.google_api_url}{url}&{strategy}&{self.locale}&key={self.api_key}'
        print(f'Opening {url} in Pagespeed Insights API')
        name = url.split('/')
        page_name = ''
        for i in range(2, len(name)):
            page_name += f'{str(name[i])}_'

        response = requests.get(api_request_url)

        if response.status_code == 200:
            print(f'Get response for {[page_name]}')
        else:
            print(f'{page_name} response is {str(response.status_code)}')

        with open(f'../../google/pagespeed/responses/{str(datetime.date.today())}/{page_name}.json',
                  'w', encoding='utf-8') as file:
            json.dump(response.json(), file, indent=4, ensure_ascii=False)
            file.close()

        return response.json()

    def _get_listrequests(self, data):

        listrequests = []

        for x in range(len(data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"])):
            endtime = data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["endTime"]
            starttime = data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["startTime"]
            transfersize = data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["transferSize"]
            resourcesize = data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["resourceSize"]
            url = data["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["url"]
            list1 = [endtime, starttime, transfersize, resourcesize, url]
            listrequests.append(list1)

        return listrequests

    def _get_render_blocking_resources(self, data):

        listblockingresources = []
        for x in range(len(data["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"])):
            url = data["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["url"]
            totalbytes = data["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x][
                "totalBytes"]
            wastedbytes = data["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x][
                "wastedMs"]
            list1 = [url, totalbytes, wastedbytes]
            listblockingresources.append(list1)

        return listblockingresources

    def extract_results(self, data: dict):

        fieldnames = ['url', 'form_factor', 'speed_index', 'overall_score',
                      'cls', 'cls_score',
                      'fcp', 'fcp_score', 'lcp', 'lcp_score', 'inp', 'inp_score',
                      'ttfb', 'ttfb_score', 'fid', 'fid_score', 'render_blocking_resources']

        page_data = [data["loadingExperience"]["id"],
                     data["lighthouseResult"]["configSettings"]["emulatedFormFactor"],
                     data['lighthouseResult']['audits']['speed-index']['displayValue'],
                     data["lighthouseResult"]["categories"]["performance"]["score"] * 100,
                     data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"] / 100,
                     data["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["category"],
                     data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"],
                     data["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["category"],
                     data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"],
                     data["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["category"],
                     data["originLoadingExperience"]["metrics"]["EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT"]["percentile"],
                     data["originLoadingExperience"]["metrics"]["EXPERIMENTAL_INTERACTION_TO_NEXT_PAINT"]["category"],
                     data["originLoadingExperience"]["metrics"]["EXPERIMENTAL_TIME_TO_FIRST_BYTE"]["percentile"],
                     data["originLoadingExperience"]["metrics"]["EXPERIMENTAL_TIME_TO_FIRST_BYTE"]["category"],
                     data["originLoadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"],
                     data["originLoadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["category"],
                     self._get_render_blocking_resources(data)
                     ]

        with open(f'audit_results-{datetime.date.today()}.csv', 'a', newline='', encoding='utf-8') as file:
            print(f'Extracting data for {data["loadingExperience"]["id"]} in csv')
            writer = csv.writer(file, delimiter=';')
            writer.writerow(fieldnames)
            writer.writerow(page_data)
            file.close()


if __name__=='__main__':

    ps = Pagespeed()

    strategy = ['mobile', 'desktop']

    with open('../../google/pagespeed/files/urls_for_check.txt', 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
        file.close()

    for url in urls:
        for form in strategy:
            ps.extract_results(ps.get_response(url, form))
