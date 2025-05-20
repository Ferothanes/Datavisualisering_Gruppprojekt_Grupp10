import pandas as pd
import sys
from pathlib import Path

# Lägg till projektroten till sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.constants import DATA_DIRECTORY

# Läs in datan
df_an = pd.read_excel(DATA_DIRECTORY / "resultat_ansokning_program_2020-2024.xlsx")
df_an["År"] = df_an["År"].astype(str).str.replace(",", "").astype(int)

#------------ Hämtar KPI-värden för viss anordnare och år
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

#------------------------ Hämta/uppdatera KPI-data baserat på val 
def update_kpi(state):
    print("Vald anordnare:", state.selected_anordnare)

    år_för_anordnare = df_an[
        df_an["Utbildningsanordnare administrativ enhet"] == state.selected_anordnare
    ]["År"].unique()

    år_för_anordnare = sorted([int(år) for år in år_för_anordnare], reverse=True)
    print("Tillgängliga år för anordnaren:", år_för_anordnare)

    state.selected_year_lov = år_för_anordnare

    if state.selected_year not in år_för_anordnare:
        state.selected_year = år_för_anordnare[0]

    poäng, kommuner, län, huvudmannatyp = get_anordnare(
        df_an, state.selected_anordnare, state.selected_year
    )

    state.poäng = poäng
    state.kommuner = kommuner
    state.län = län
    state.selected_year_str = str(state.selected_year)
    state.huvudmannatyp = huvudmannatyp

    #-- Beviljade ansökningar
    beviljade, ej_beviljade = count_beslut(df_an, state.selected_anordnare, state.selected_year)
    state.beviljade = beviljade
    state.ej_beviljade = ej_beviljade
    #-- Utbildningsområden 
    utbildningsområden = get_utbildningsområden(df_an, state.selected_anordnare, state.selected_year)
    state.utbildningsområden = utbildningsområden
    state.utbildningsområden_text = ", ".join(utbildningsområden)
    #-- Procent andel av sökta
    total = beviljade + ej_beviljade
    if total > 0:
        state.beviljandegrad = round(beviljade / total * 100, 1)
    else:
        state.beviljandegrad = 0.0


#-----Räkna beslut 

def count_beslut(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare) &
        (df["År"] == år)
    ]
    beslut_counts = df_filtered["Beslut"].value_counts().to_dict()

    beviljade = beslut_counts.get("Beviljad", 0)
    ej_beviljade = beslut_counts.get("Ej beviljad", 0)
    return beviljade, ej_beviljade


#-------- Få ut utbildningsområden

def get_utbildningsområden(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare) &
        (df["År"] == år) &
        (df["Beslut"] == "Beviljad")
    ]
    return sorted(df_filtered["Utbildningsområde"].dropna().unique().tolist())