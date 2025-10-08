import pandas as pd
from pathlib import Path

class Data_Cleaning:
    def __init__(self):
        self.df = None

    def load_data(self, path):
        try:
            df_readed = pd.read_csv(Path(path))
            df_readed.columns = [
                "car_name",
                "displacement_l",
                "engine_type",
                "horsepower",
                "transmission_speed",
                "top_speed_mph",
                "cost_usd"
            ]
            self.df = df_readed
        except Exception as e:
            print(e)

if __name__ == "__main__":
    data_clean = Data_Cleaning()
    data_clean.load_data('./data/raw/HyperCars2019.csv')