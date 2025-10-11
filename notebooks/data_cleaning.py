import pandas as pd
import re
import logging
import warnings
from pathlib import Path
from typing import Dict, Any

# TODO Add logs to each function
# TODO Add type hints for function returns
# TODO Add function info to reports

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore", category=FutureWarning)

class Data_Cleaning:
    def __init__(self, path):
        self.df = None
        self.file_path = path
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

    def load_data(self):
        try:
            df_readed = pd.read_csv(Path(self.file_path))
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
            logger.info(f"Data loaded successfully from {self.file_path}")
            return self.df
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise

    def generate_initial_report(self) -> Dict[str, Any]:
        report = {
            "num_rows": int(len(self.df)),
            "num_columns": int(len(self.df.columns)),
            "missing_values": {k: int(v) for k, v in self.df.isnull().sum().to_dict().items()},
            "data_types": {k: str(v) for k, v in self.df.dtypes.to_dict().items()},
            "duplicates": int(self.df.duplicated().sum())
        }

        logger.info("Initial data report generated")
        return report

    def car_name_cleaning(self) -> None:
        intial_nulls = self.df['car_name'].isnull().sum()
        duplicates = self.df["car_name"].duplicated().sum()

        def format_car_name(car_name: str) -> str:
            if pd.isna(car_name):
                return None
            
            # Basic cleanup
            name = str(car_name).strip()
            if not name:
                return None
            
            # Chain all regex operations
            transformations = [
                (r'(.)\1{2,}', r'\1\1'),  # Remove excessive repeated chars
                (r'(\w+)re$', r'\1'),     # Fix "Veyronre" -> "Veyron"
                (r'(\w+)aa+$', r'\1a'),   # Fix "Sennaaaa" -> "Senna"
                (r'\s+', ' ')             # Normalize spacing
            ]
            
            for pattern, replacement in transformations:
                name = re.sub(pattern, replacement, name)
            
            # Brand corrections (case-insensitive)
            brands = {
                r'\bmclaren\b': 'McLaren', r'\bbuggatti?\b': 'Bugatti',
                r'\bmercedes\b': 'Mercedes', r'\bferrari\b': 'Ferrari',
                r'\bporsche\b': 'Porsche', r'\bkoenigse+g+\b': 'Koenigsegg',
                r'\bpaga+ni\b': 'Pagani', r'\baston\b': 'Aston', r'\bmartin\b': 'Martin'
            }
            
            for pattern, replacement in brands.items():
                name = re.sub(pattern, replacement, name, flags=re.IGNORECASE)
            
            # Smart title case
            uppercase_words = {'AMG', 'ONE', 'BC', 'GT', 'RS', 'SLS', 'SLR'}
            prepositions = {'von', 'de', 'la', 'le', 'du'}
            roman_pattern = re.compile(r'^[IVX]+$')
            
            words = []
            for word in name.split():
                word_upper = word.upper()
                if word_upper in uppercase_words or roman_pattern.match(word_upper):
                    words.append(word_upper)
                elif word.lower() in prepositions:
                    words.append(word.lower())
                else:
                    words.append(word.title())
            
            return ' '.join(words)

        self.df["car_name"] = self.df["car_name"].apply(
            lambda car_name: format_car_name(car_name)
        )

        self.report["car_name"] = {
            "initial_nulls": intial_nulls,
            "duplicates": duplicates
        }

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

    def displacement_cleaning(self):
        initial_nulls = self.df['displacement_l'].isnull().sum()

        self.df['displacement_l'] = pd.to_numeric(self.df['displacement_l'], errors="coerce")

        valid_values = self.df['displacement_l'].dropna()

        if len(valid_values) > 0:
            mean_displacement = valid_values.mean()
        else:
            mean_displacement = 4.0

        self.df['displacement_l'] = self.df['displacement_l'].apply(
            lambda x: x if 0.8 <= x <= 9.0 else mean_displacement
        )
        self.df['displacement_l'] = self.df['displacement_l'].fillna(mean_displacement)

        print(self.df['displacement_l'])


if __name__ == "__main__":
    data_clean = Data_Cleaning('./data/raw/HyperCars2019.csv')
    data_clean.load_data()
    data_clean.generate_initial_report()
    # data_clean.engine_cleaning()
    # data_clean.car_name_cleaning()
    data_clean.displacement_cleaning()