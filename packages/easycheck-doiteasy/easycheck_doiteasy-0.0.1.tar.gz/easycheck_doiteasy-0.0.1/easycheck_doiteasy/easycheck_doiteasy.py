import requests
import os

MONITOR_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTUsImV4cCI6MTY4NzI5NzYxNn0.k713wpFyzMc1ZgPTJjgPuJubM_stvCsQd3vb6mL-QOU'
TEMP_DOMAIN = 'https://b0e7-38-25-12-182.sa.ngrok.io'


class Easycheck():

    def __init__(self, token):
        self.token = token

    def send_ejecution(data):

        headers = {}
        domain = TEMP_DOMAIN
        path = '/api/base/ejecution/send/'
        url = f'{domain}{path}'
        data.update({
            'register_token': MONITOR_TOKEN
        })
        res = requests.post(url, data=data, headers=headers)
        
    def update_logs_directories(logs_dir):

        headers = {}
        domain = TEMP_DOMAIN
        path = '/api/base/logs_directory/register/'
        url = f'{domain}{path}'
        directories = [element for element in os.listdir(logs_dir) if os.path.isdir(f'{logs_dir}/{element}')]
        ruta_absoluta = os.path.abspath(__file__)
        carpeta_raiz = os.path.basename(os.path.dirname(ruta_absoluta))
        data = {
            'origin': carpeta_raiz,
            'directories': directories,
            'register_token': MONITOR_TOKEN
        }
        res = requests.post(url, data=data, headers=headers)

    def register_file(log_file):

        headers = {}
        domain = TEMP_DOMAIN
        path = '/api/base/logs_file/register/'
        file_size = os.path.getsize(log_file)/1024
        log_dir = log_file.split('/')[-2]
        log_filename = log_file.split('/')[-1]
        data = {
            'name': log_filename,
            'log_directory': log_dir,
            'file_size': file_size,
            'with_errors': False,
            'register_token': MONITOR_TOKEN
        }
        url = f'{domain}{path}'
        res = requests.post(url, data=data, headers=headers)