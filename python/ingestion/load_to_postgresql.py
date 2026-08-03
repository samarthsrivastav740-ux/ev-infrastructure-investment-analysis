import pandas as pd
from sqlalchemy import create_engine

from python.utils.file_paths import RAW_TABLES

import os
from dotenv import load_dotenv

# PostgreSQL Connection
load_dotenv()

DATABASE = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

def load_table(table_name, csv_path):
    """
    Reads a CSV file and loads it into the PostgreSQL raw schema.
    """

    print(f"\nLoading {table_name}....")

    df = pd.read_csv(csv_path)

    df.to_sql(
                name=table_name,
        con=engine,
        schema="raw",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=10000
    )

    print(f"✓ {table_name} loaded successfully ({len(df):,} rows)")

def main():

    print("="*60)
    print("Loading CSV files into PostgreSQL")
    print("=" * 60)

    for table_name, csv_path in RAW_TABLES.items():
        try:
           load_table(table_name,csv_path)
        except Exception as e:
            print(f"✗ Failed to load {table_name}")
            print(e)

    print("\nAll tables loaded successfully.")

if __name__ == "__main__":
    main()
