import pandas as pd
from utils.constants import DATA_DIRECTORY

df = pd.read_excel(
    DATA_DIRECTORY / "Utbildningsansökning_age.xlsx",
    sheet_name="education"
)

# add new paths? 
# df = pd.read_excel(
#     DATA_DIRECTORY / "new data????"
# )