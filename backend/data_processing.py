import pandas as pd
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1])) 
from utils.constants import DATA_DIRECTORY



df = pd.read_excel(
    DATA_DIRECTORY / "Utbildningsansökning_age.xlsx",
    sheet_name="education"
)
