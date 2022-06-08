from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import json


def update(url: str):

    SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

    # service_account_file.json is the private key that you created for your service account.
    JSON_KEY_FILE = ""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    # Define contents here as a JSON string.
    # This example shows a simple update request.
    # Other types of requests are described in the next step.

    payload = {
        "url": f"{url}",
        "type": "URL_UPDATED"
    }

    payload_string = json.dumps(payload)

    response, content = http.request(ENDPOINT, method="POST", body=payload_string)
    print(f'push {url}')
    return f'Response\n{response}\n\n{content}\n_________________________________________________________\n'


def get_notification_response(url: str):

    SCOPES = [ "https://www.googleapis.com/auth/indexing" ]
    # service_account_file.json is the private key that you created for your service account.
    JSON_KEY_FILE = ""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)

    http = credentials.authorize(httplib2.Http())

    meta_url = url.replace('/', '%2F').replace(":", '%3A')
    service_url = 'https://indexing.googleapis.com/v3/urlNotifications/metadata?url='
    request_url = f'{service_url}{meta_url}'

    response = http.request(request_url, method="GET")

    return response


def main():

    with open('../../google/search_console/data/url_for_index.txt', 'r', encoding='utf-8') as file:
        urls = file.read().splitlines()
        file.close()

    with open('../../google/search_console/data/log_indexing_api.txt', 'a', encoding='utf-8') as file:
        for url in urls:
            file.write(update(url))
        file.close()



if __name__ == '__main__':

    main()

