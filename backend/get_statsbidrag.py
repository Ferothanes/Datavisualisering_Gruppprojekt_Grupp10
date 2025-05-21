import pandas as pd
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))

from utils.constants import DATA_DIRECTORY

def count_statsbidrag(anordnare, år):
    
    df_bidrag = pd.read_excel(DATA_DIRECTORY / "resultat_ansokning_program_2020-2024.xlsx")
    df_bidrag["År"] = df_bidrag["År"].astype(str).str.replace(",", "").astype(int)
    df_bidrag = df_bidrag[(df_bidrag["Beslut"] == "Beviljad") & (df_bidrag["År"] == år)]

    #-- Läser statsbidrag
    df_stats = pd.read_excel(DATA_DIRECTORY / "Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")
    df_stats_melted = df_stats.melt(id_vars=["År"], var_name="Utbildningsområde", value_name="Utbetalda_mkr")
    df_stats_melted["År"] = df_stats_melted["År"].astype(int)

    #--Räknar antal utbildningar per utbildningsområde
    total_per_område = df_bidrag.groupby("Utbildningsområde").size().reset_index(name="Total_utb")
    per_anordnare = df_bidrag[df_bidrag["Utbildningsanordnare administrativ enhet"] == anordnare]
    per_anordnare_grouped = per_anordnare.groupby("Utbildningsområde").size().reset_index(name="Antal_anordnare_utb")

    #-- Räkna bidragsandel av utbildningarna som en anordnare har per område
    df_merged = pd.merge(per_anordnare_grouped, total_per_område, on="Utbildningsområde", how="left")
    df_merged["Andel"] = df_merged["Antal_anordnare_utb"] / df_merged["Total_utb"]

    #-- Läggertill statsbidrag
    df_merged = pd.merge(df_merged, df_stats_melted[df_stats_melted["År"] == år], on="Utbildningsområde", how="left")
    df_merged["Anordnarens_bidrag_mkr"] = df_merged["Andel"] * df_merged["Utbetalda_mkr"]

    total_mkr = df_merged["Anordnarens_bidrag_mkr"].sum()
    
    return round(total_mkr, 2)

