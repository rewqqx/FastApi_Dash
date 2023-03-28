import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
from fastapi import Depends
from sqlalchemy.orm import Session
from src.fastapi_server.db.db import get_session
from src.fastapi_server.models.response_history import ResponseHistory


class ModelsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

        self.data_file = "../files/data.csv"
        self.data_preproc_file = "../files/data_preproc.csv"
        self.data_predict_file = "../files/prediction_data.csv"
        self.data_all_predict_file = "../files/prediction_all_data.csv"
        self.model_file = "../files/joblib_model.csv"
        self.data_test_file = "../files/data_test.csv"

    def preprocessing(self, data: pd.DataFrame, user_id: int) -> pd.DataFrame:
        data.drop(['Failure Type'], axis='columns', inplace=True)
        data.dropna()
        data = pd.get_dummies(data, columns=['Type'], prefix='Type')
        self.write_response('preprocessing', user_id)
        return data

    def fit(self, data, user_id):
        labels2drop = ['UDI', 'Product ID', 'Target']
        data_c = data.drop(columns=labels2drop)

        X = data_c
        y = data.Target

        oversample = SMOTE()
        X_o, y_o = oversample.fit_resample(X, y)
        X_traino, X_testo, y_traino, y_testo = train_test_split(X_o, y_o, test_size=0.2)

        model = RandomForestClassifier()

        model.fit(X_traino, y_traino)

        joblib.dump(model, self.model_file)
        X_testo['Target'] = y_testo
        self.write_response('fit', user_id)
        return X_testo

    def predict(self, data, user_id):
        data_c = data.copy()
        labels2drop = ['Target']
        data_c = data_c.drop(columns=labels2drop)
        model = joblib.load(self.model_file)

        y = model.predict(data_c)

        self.write_response('predict', user_id)

        data['Predict Target'] = y
        return data

    def predict_all(self):
        data = pd.read_csv(self.data_file)
        data.drop(['Failure Type'], axis='columns', inplace=True)
        labels2drop = ['UDI', 'Product ID', 'Target']
        data = pd.get_dummies(data, columns=['Type'], prefix='Type')
        data = data.drop(columns=labels2drop)
        model = joblib.load(self.model_file)

        y = model.predict(data)

        data['Predict Target'] = y

        return data

    def download(self, type, user_id):
        self.write_response('download', user_id)
        match type:
            case 1:
                response = self.data_file
            case 2:
                response = self.data_preproc_file
            case 3:
                response = self.data_predict_file
            case 4:
                response = self.model_file
            case 5:
                response = self.data_all_predict_file
        return response

    def download_model(self, user_id):
        self.write_response('download', user_id)
        return self.model_file

    def write_response(self, name: str, user_id: int):
        response_dict = {'request': name, 'created_by': user_id}
        response = ResponseHistory(**response_dict)
        self.session.add(response)
        self.session.commit()
