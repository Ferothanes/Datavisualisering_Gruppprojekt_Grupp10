import pandas as pd
import sys
from pathlib import Path

# Lägg till projektroten till sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.constants import DATA_DIRECTORY


df = pd.read_excel(
    DATA_DIRECTORY / "Utbildningsansökning_age.xlsx",
    sheet_name="Education"
)

df_an = pd.read_excel(
    DATA_DIRECTORY / "resultat_ansokning_program_2020-2024.xlsx",
)

df_an["År"] = df_an["År"].astype(str).str.replace(",", "").astype(int)

def get_anordnare(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare)
        & (df["År"] == år)
        & (df["Beslut"] == "Beviljad")
    ]

    poäng = df_filtered["YH-poäng"].sum()
    kommuner = df_filtered["Kommun"].nunique()
    län = df_filtered["Län"].nunique()
    huvudmannatyp = df_filtered["Huvudmannatyp"].iloc[0] if not df_filtered.empty else "Okänd"

    return poäng, kommuner, län, huvudmannatyp

# add new paths? 
# df = pd.read_excel(
#     DATA_DIRECTORY / "new data????"
# )