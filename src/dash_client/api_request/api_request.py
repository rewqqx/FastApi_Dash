from src.dash_client.core.settings import settings
import requests
import pandas as pd


class ApiRequest:
    def __init__(self):
        self.connection_str = f'http://{settings.host}:{settings.port}/'
        self.user = settings.admin_name
        self.password = settings.admin_password
        self.token = self.get_token()
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_token(self):
        url = self.connection_str + 'users/authorize'
        ck = {'username': self.user, 'password': self.password}
        with requests.Session() as s:
            p = s.post(url, data=ck)
            token = p.json()['access_token']

        return token

    def get_data(self, type_id):
        url = self.connection_str + f'models/download/{type_id}'
        path = f'../files/dash/data{type_id}.csv'
        with requests.Session() as s:
            req = s.get(url, headers=self.headers)
            open(path, 'wb').write(req.content)
            df = pd.read_csv(path)

        return df

    def save_model(self):
        url = self.connection_str + 'models/download/4'
        with requests.Session() as s:
            req = s.get(url, headers=self.headers)
            open('../files/dash/model.csv', 'wb').write(req.content)


