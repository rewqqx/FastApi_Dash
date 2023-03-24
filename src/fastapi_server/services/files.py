from io import StringIO
from typing import BinaryIO
import pandas as pd


class FilesService:

    @staticmethod
    def upload(file: BinaryIO):
        df = pd.read_csv(file)
        return df

    @staticmethod
    def download(data):
        output = StringIO()
        data.to_csv(output, index=False)
        output.seek(0)
        return output

    @staticmethod
    def save_file(data, path):
        data.to_csv(path, index=False)
