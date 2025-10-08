import pandas as pd
import re
from pathlib import Path

class Data_Cleaning:
    def __init__(self):
        self.df = None
        self.report = {}
        self.ENGINE_PATTERN = r'([IVW])(\d{1,2})'
        self.VALID_ENGINES = (
            # Inline (straight) engines
            "I3",
            "I4",
            "I5",
            "I6",

            # V-shaped engines
            "V6",
            "V8",
            "V10",
            "V12",
            "V16",

            # W engines (Volkswagen Group, Bugatti, etc.)
            "W8",
            "W12",
            "W16",
        )       

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

    def engine_cleaning(self):
        initial_nulls = self.df["engine_type"].isnull().sum()
        self.report["engine_type_initial_nulls"] = initial_nulls

        def extract_valid_engine(engine_type: str):
            if pd.isna(engine_type):
                return None
            
            match = re.search(self.ENGINE_PATTERN, engine_type)
            if match:
                extracted = match.group(1) + match.group(2)

                if extracted in self.VALID_ENGINES:
                    return extracted
                else:
                    return None # Infer missing engines from horsepower and displacement.
            else:
                return None # Infer missing engines from horsepower and displacement.

        self.df["engine_type"] = self.df["engine_type"].apply(
            lambda engine: extract_valid_engine(engine)
        )

        print(self.df["engine_type"])

if __name__ == "__main__":
    data_clean = Data_Cleaning()
    data_clean.load_data('./data/raw/HyperCars2019.csv')
    data_clean.engine_cleaning()