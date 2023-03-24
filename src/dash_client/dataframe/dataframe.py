class Data:
    def __init__(self, df, df_prediction):
        self.df = df
        self.df_prediction = df_prediction
        self.features = ['Type', 'Air temperature [K]', 'Process temperature [K]', 'Rotational speed [rpm]',
                         'Torque [Nm]',
                         'Tool wear [min]', 'Target', 'Failure Type']