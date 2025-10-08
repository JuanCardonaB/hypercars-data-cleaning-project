import pandas as pd
from pathlib import Path

class Data_Cleaning:
    def __init__(self):
        self.df = None
        self.cleaning_report = {}
        self.ACCEPTED_ENGINES = {
            # Inline (straight) engines
            "I3": "Inline 3-cylinder",
            "I4": "Inline 4-cylinder",
            "I5": "Inline 5-cylinder",
            "I6": "Inline 6-cylinder",

            # V-shaped engines
            "V6": "V-shaped 6-cylinder",
            "V8": "V-shaped 8-cylinder",
            "V10": "V-shaped 10-cylinder",
            "V12": "V-shaped 12-cylinder",
            "V16": "V-shaped 16-cylinder",

            # W engines (Volkswagen Group, Bugatti, etc.)
            "W8": "W-shaped 8-cylinder",
            "W12": "W-shaped 12-cylinder",
            "W16": "W-shaped 16-cylinder",

            # Boxer (flat) engines
            "B4": "Boxer 4-cylinder",
            "B6": "Boxer 6-cylinder",
            "B8": "Boxer 8-cylinder",

            # Rotary and hybrid systems
            "R1": "Rotary (1 rotor)",
            "R2": "Rotary (2 rotors)",
            "Hybrid": "Hybrid Engine (Electric + Combustion)",
            "Electric": "Fully Electric Powertrain",

            # Special high-performance engines
            "Quad-Turbo V8": "V8 Engine with Quad-Turbocharging",
            "Twin-Turbo V12": "V12 Engine with Twin-Turbocharging",
            "Twin-Turbo V8": "V8 Engine with Twin-Turbocharging",
        }

    def load_data(self, path):
        try:
            df_readed = pd.read_csv(Path(path))
            self.df = df_readed
        except Exception as e:
            print(e)


    def engine_cleaning(self):
       
        initial_nulls = self.df['Enginee'].isnull().sum()
        print(initial_nulls)

if __name__ == "__main__":
    data_clean = Data_Cleaning()
    data_clean.load_data('./data/raw/HyperCars2019.csv')
    data_clean.engine_cleaning()