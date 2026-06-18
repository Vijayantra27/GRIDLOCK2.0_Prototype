# backend/app/utils/data_loader.py

import os
import pandas as pd


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "violations.csv"
)


def load_data():

    print("\nLoading Dataset:")
    print(DATASET_PATH)

    df = pd.read_csv(DATASET_PATH)

    return df