import pandas as pd
import sys
from pathlib import Path
import frontend.pages.anordnare as anordnare_gui

# Lägg till projektroten till sys.path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils.constants import DATA_DIRECTORY

# Läs in datan
df_an = pd.read_excel(DATA_DIRECTORY / "resultat_ansokning_program_2020-2024.xlsx")
df_an["År"] = df_an["År"].astype(str).str.replace(",", "").astype(int)

# --Hämtar data för anordnare och år
def get_anordnare(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare)
        & (df["År"] == år)
    ]

    poäng = df_filtered[df_filtered["Beslut"] == "Beviljad"]["YH-poäng"].sum()

    #-- Kommuner, bort med Nans och dubletter
    kommuner_lista = df_filtered["Kommun"].dropna().unique()
    kommuner_rensade = sorted(kommuner_lista)
    kommuner = ", ".join(kommuner_rensade) if kommuner_rensade else "Okänt"

    #--Län
    län_lista = df_filtered["Län"].dropna().unique()
    län_rensade = sorted(län_lista)
    län = ", ".join(län_rensade) if län_rensade else "Okänt"


    huvudmannatyp = df_filtered["Huvudmannatyp"].iloc[0] if not df_filtered.empty else "Okänd"

    return poäng, kommuner, län, huvudmannatyp

# Uppdaterar alla KPI:er baserat på klicka statstik/state
def update_kpi(state):
    print("Vald anordnare:", state.selected_anordnare)

    # Selekterar/skriver ut anorndare/år i dropdownen
    år_för_anordnare = df_an[
        df_an["Utbildningsanordnare administrativ enhet"] == state.selected_anordnare
    ]["År"].unique()
    år_för_anordnare = sorted([int(år) for år in år_för_anordnare], reverse=True)
    state.selected_year_lov = år_för_anordnare


    # Säkerställer att selected year inte kraschar 
    if state.selected_year not in år_för_anordnare:
        state.selected_year = år_för_anordnare[0]

    poäng, kommuner, län, huvudmannatyp = get_anordnare(df_an, state.selected_anordnare, state.selected_year)
    state.poäng = poäng
    state.kommuner = kommuner
    state.län = län

    #-- Få utskrivet selekterat år i sträng
    state.selected_year_str = str(state.selected_year)
    state.huvudmannatyp = huvudmannatyp

    #- Antal beviljanden
    beviljade, ej_beviljade = count_beslut(df_an, state.selected_anordnare, state.selected_year)
    state.beviljade = beviljade
    state.ej_beviljade = ej_beviljade

    #- Utbildningsområden
    utbildningsområden = get_utbildningsområden(df_an, state.selected_anordnare, state.selected_year)
    state.utbildningsområden = utbildningsområden
    state.utbildningsområden_text = ", ".join(utbildningsområden)


    #- Andelsgrad
    total = beviljade + ej_beviljade
    state.beviljandegrad = round(beviljade / total * 100, 1) if total > 0 else 0.0

    #-  Botten KPIer för sökningar
    state.fig_top_10_sökta = fig_top_10_sökta(df_an, state.selected_year)
    state.fig_top_10_beviljade = fig_top_10_beviljade(df_an, state.selected_year)


# -- För att kunna få ut beviljade/obeviljade ansökningar
def count_beslut(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare) &
        (df["År"] == år)
    ]
    beviljade = df_filtered[df_filtered["Beslut"] == "Beviljad"].shape[0]
    ej_beviljade = df_filtered[df_filtered["Beslut"] != "Beviljad"].shape[0]
    return beviljade, ej_beviljade


# -- Hämta utbildningsområden
def get_utbildningsområden(df, anordnare, år):
    df_filtered = df[
        (df["Utbildningsanordnare administrativ enhet"] == anordnare)
        & (df["År"] == år)
        & (df["Beslut"] == "Beviljad")
    ]
    return (df_filtered["Utbildningsområde"].dropna().unique().tolist())

import plotly.express as px

#-- Hämta mest sökta utbildningsområden

def fig_top_10_sökta(df, år):
    df_filtered = df[df["År"] == år]
    counts = df_filtered["Utbildningsområde"].value_counts().head(10).sort_values()
    df_counts = counts.reset_index()
    df_counts.columns = ["Utbildningsområde", "Antal ansökningar"]

    fig = px.bar(
        df_counts,
        x="Antal ansökningar",
        y="Utbildningsområde",
        orientation='h',
        template='plotly_white',
        title=f"Top 10 mest sökta utbildningsområden ({år})"
    )
    fig.update_traces(marker_color="#51abcb", width=0.5)
    fig.update_layout(margin=dict(t=30, b=30))
    return fig


#-- Hämta mest beviljade utbildningsområden

def fig_top_10_beviljade(df, år):
    df_filtered = df[(df["År"] == år) & (df["Beslut"] == "Beviljad")]
    counts = df_filtered["Utbildningsområde"].value_counts().head(10).sort_values()
    df_counts = counts.reset_index()
    df_counts.columns = ["Utbildningsområde", "Antal beviljanden"]

    fig = px.bar(
        df_counts,
        x="Antal beviljanden",
        y="Utbildningsområde",
        orientation='h',
        template='plotly_white',
        title=f"Top 10 mest beviljade utbildningsområden ({år})"
    )
    fig.update_traces(marker_color="#51abcb", width=0.5)
    fig.update_layout(margin=dict(t=30, b=30))
    return fig








