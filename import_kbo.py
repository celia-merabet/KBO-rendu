import zipfile
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend import models

POSTGRES_USER = "kbo"
POSTGRES_PASSWORD = "kbopass"
POSTGRES_DB = "kbo_db"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

models.Base.metadata.create_all(bind=engine)

csv_table_mapping = {
    "activity.csv": "activity",
    "enterprise.csv": "enterprise",
    "establishment.csv": "establishment",
    "denomination.csv": "denomination",
    "address.csv": "address",
    "contact.csv": "contact",
    "branch.csv": "branch",
    "code.csv": "code",
    "meta.csv": "meta"
}

columns_mapping = {
    "enterprise": ["EnterpriseNumber", "Status", "JuridicalForm", "Type", "Language", "StartDate"],
    "establishment": ["EnterpriseNumber", "EstablishmentNumber", "Status", "StartDate"],
    "activity": ["EntityNumber", "ActivityGroup", "NaceVersion", "NaceCode", "Classification"]
}

def parse_date(date_str):
    try:
        return pd.to_datetime(date_str, errors='coerce').date()
    except:
        return None

def import_csv_to_table(filelike, table_name):
    CHUNKSIZE = 100_000 
    for chunk in pd.read_csv(filelike, sep=';', dtype=str, chunksize=CHUNKSIZE):
        chunk = chunk.fillna('')
        if table_name == "activity":
            chunk = chunk[columns_mapping["activity"]]
        elif table_name == "enterprise":
            chunk = chunk[columns_mapping["enterprise"]]
            chunk = chunk.rename(columns={
                "EnterpriseNumber": "enterprise_number",
                "Status": "status",
                "JuridicalForm": "juridical_form",
                "Type": "type",
                "Language": "language",
                "StartDate": "start_date"
            })
            chunk["start_date"] = chunk["start_date"].apply(parse_date)
        elif table_name == "establishment":
            chunk = chunk[columns_mapping["establishment"]]
            chunk = chunk.rename(columns={
                "EnterpriseNumber": "enterprise_number",
                "EstablishmentNumber": "establishment_number",
                "Status": "status",
                "StartDate": "start_date"
            })
            chunk["start_date"] = chunk["start_date"].apply(parse_date)

        # Insérer dans PostgreSQL
        chunk.to_sql(table_name, engine, if_exists="append", index=False)
        print(f"Importé {len(chunk)} lignes dans {table_name}")

def main(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for csv_name, table_name in csv_table_mapping.items():
            if csv_name in zf.namelist():
                print(f"Import de {csv_name} dans {table_name}...")
                with zf.open(csv_name) as f:
                    import_csv_to_table(f, table_name)
            else:
                print(f"{csv_name} non trouvé dans le ZIP, skipped.")
    print("Import KBO terminé !")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python import_kbo.py <KboOpenData_XXXX.zip>")
    else:
        main(sys.argv[1])
