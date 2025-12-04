import zipfile
from io import TextIOWrapper

import pandas as pd

zip_path = "KboOpenData_0200_2025_12_03_Full.zip"
csv_name = "activity.csv"

with zipfile.ZipFile(zip_path, 'r') as zf:
    if csv_name in zf.namelist():
        with zf.open(csv_name) as f:
            df = pd.read_csv(
                TextIOWrapper(f, encoding='utf-8'),
                sep=',',       # ou ';' si ton CSV est séparé par des points-virgules
                quotechar='"', 
                nrows=5
            )
            print("Colonnes dans activity.csv :")
            print(df.columns)
    else:
        print(f"{csv_name} non trouvé dans le ZIP")
