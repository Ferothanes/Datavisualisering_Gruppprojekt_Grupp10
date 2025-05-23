import pandas as pd
import sys
from pathlib import Path
from backend.get_statsbidrag import count_statsbidrag

# Lägg till projektroten till sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.constants import DATA_DIRECTORY

# Läs in datan
df_an = pd.read_excel(DATA_DIRECTORY / "resultat_ansokning_program_2020-2024.xlsx")
df_an["År"] = df_an["År"].astype(str).str.replace(",", "").astype(int)

# Hämtar KPI-värden för viss anordnare och år
def get_anordnare(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare)
        & (df["År"] == år)
    ]

    poäng = df_filtered[df_filtered["Beslut"] == "Beviljad"]["YH-poäng"].sum()

    kommuner_lista = df_filtered["Kommun"].dropna().unique()
    kommuner_rensade = sorted([k for k in kommuner_lista if "flera" not in k.lower()])
    kommuner = ", ".join(kommuner_rensade) if kommuner_rensade else "Okänt"

    län_lista = df_filtered["Län"].dropna().unique()
    län_rensade = sorted([l for l in län_lista if "flera" not in l.lower()])
    län = ", ".join(län_rensade) if län_rensade else "Okänt"

    huvudmannatyp = df_filtered["Huvudmannatyp"].iloc[0] if not df_filtered.empty else "Okänd"

    return poäng, kommuner, län, huvudmannatyp

# Uppdaterar alla KPI:er baserat på state
def update_kpi(state):
    print("Vald anordnare:", state.selected_anordnare)

    år_för_anordnare = df_an[
        df_an["Utbildningsanordnare administrativ enhet"] == state.selected_anordnare
    ]["År"].unique()
    år_för_anordnare = sorted([int(år) for år in år_för_anordnare], reverse=True)
    state.selected_year_lov = år_för_anordnare

    if state.selected_year not in år_för_anordnare:
        state.selected_year = år_för_anordnare[0]

    poäng, kommuner, län, huvudmannatyp = get_anordnare(df_an, state.selected_anordnare, state.selected_year)
    state.poäng = poäng
    state.kommuner = kommuner
    state.län = län
    state.selected_year_str = str(state.selected_year)
    state.huvudmannatyp = huvudmannatyp

    beviljade, ej_beviljade = count_beslut(df_an, state.selected_anordnare, state.selected_year)
    state.beviljade = beviljade
    state.ej_beviljade = ej_beviljade

    utbildningsområden = get_utbildningsområden(df_an, state.selected_anordnare, state.selected_year)
    state.utbildningsområden = utbildningsområden
    state.utbildningsområden_text = ", ".join(utbildningsområden)

    total = beviljade + ej_beviljade
    state.beviljandegrad = round(beviljade / total * 100, 1) if total > 0 else 0.0

    state.statsbidrag_mkr = count_statsbidrag(state.selected_anordnare, state.selected_year)

# Räkna antal beviljade/ej beviljade
def count_beslut(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare) &
        (df["År"] == år)
    ]
    beslut_counts = df_filtered["Beslut"].value_counts().to_dict()
    return beslut_counts.get("Beviljad", 0), beslut_counts.get("Ej beviljad", 0)

# Hämta utbildningsområden
def get_utbildningsområden(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare)
        & (df["År"] == år)
        & (df["Beslut"] == "Beviljad")
    ]
    return sorted(df_filtered["Utbildningsområde"].dropna().unique().tolist())







