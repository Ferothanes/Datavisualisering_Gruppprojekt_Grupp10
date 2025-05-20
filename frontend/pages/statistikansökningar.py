import pandas as pd
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from utils.constants import DATA_DIRECTORY

# Ladda in data från Excel-filer för 2024 och 2023
df_2024 = pd.read_excel(
    DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh (1).xlsx",
    sheet_name="Lista ansökningar"
)
df_2023 = pd.read_excel(
    DATA_DIRECTORY / "resultat-2023-for-kurser-inom-yh.xlsx",
    sheet_name="Lista ansökningar"
)

# Beräkna statistik för 2024 (default)
antal_kurser_default = df_2024.shape[0]
antal_anordnare_default = df_2024["Anordnare namn"].nunique()
antal_utbildningsområden_default = df_2024["Utbildningsområde"].nunique()


selected_year = "2024"
antal_kurser = antal_kurser_default
antal_anordnare = antal_anordnare_default
antal_utbildningsområden = antal_utbildningsområden_default

def count_beviljade_per_utbildningsområde(df):
    df_beviljade = df[df["Beslut"] == "Beviljad"]
    resultat = df_beviljade.groupby("Utbildningsområde").size().reset_index(name="Antal beviljade kurser")
    return resultat

# Skapa standarddiagrammet med 2024-data
df_kurser_utbildningsområde_default = count_beviljade_per_utbildningsområde(df_2024)
fig_default = px.bar(
    df_kurser_utbildningsområde_default,
    y="Utbildningsområde",
    x="Antal beviljade kurser",
    title="Antal beviljade kurser per utbildningsområde (2024)",
    labels={
        "Utbildningsområde": "Utbildningsområde",
        "Antal beviljade kurser": "Antal beviljade kurser"
    },
    orientation='h'
)
fig = fig_default  # Standarddiagramet

def update_year(state):
    global selected_year, antal_kurser, antal_anordnare, antal_utbildningsområden, fig
    if state.selected_year == "2023":
        df_new = df_2023
        year_text = "2023"
    else:
        df_new = df_2024
        year_text = "2024"
    
    # Uppdatera statistik
    antal_kurser = df_new.shape[0]
    antal_anordnare = df_new["Anordnare namn"].nunique()
    antal_utbildningsområden = df_new["Utbildningsområde"].nunique()
    
    # Uppdatera diagrammet
    df_kurser_updated = count_beviljade_per_utbildningsområde(df_new)
    fig = px.bar(
        df_kurser_updated,
        y="Utbildningsområde",
        x="Antal beviljade kurser",
        title=f"Antal beviljade kurser per utbildningsområde ({year_text})",
        labels={
            "Utbildningsområde": "Utbildningsområde",
            "Antal beviljade kurser": "Antal beviljade kurser"
        },
        orientation='h'
    )
    
    
    # återspeglar de nya värdena.
    state.antal_kurser = antal_kurser
    state.antal_anordnare = antal_anordnare
    state.antal_utbildningsområden = antal_utbildningsområden
    state.fig = fig

with tgb.Page() as ansökningar:
    with tgb.part(class_name="container card"):
        tgb.navbar(rebuild = True)
        with tgb.part(class_name="card"):
            tgb.text(
                "# MYH dashboard",
                class_name="center-text red-text",
                mode="md"
            )
            # Lägg till dropdown (selector) för att välja år
            tgb.selector("{selected_year}", lov=["2024", "2023"], dropdown=True, on_change=update_year)
            tgb.text(
                "## Dashboard för att visa statistik och information om ansökningsomgångar",
                class_name="center-text",
                mode="md"
            )
            # Visa statistik (antal kurser, anordnare, utbildningsområden)
            with tgb.part(class_name="card text-row"):
                with tgb.part(class_name="text-container"):
                    tgb.text("Antalet Beviljade Kurser", class_name="bold-italic", mode="md")
                    tgb.text("{antal_kurser}", class_name="bold-italic", mode="md")
                with tgb.part(class_name="text-container"):
                    tgb.text("Antalet Anordnare", class_name="bold-italic", mode="md")
                    tgb.text("{antal_anordnare}", class_name="bold-italic", mode="md")
                with tgb.part(class_name="text-container"):
                    tgb.text("Antalet Utbildningsområden", class_name="bold-italic", mode="md")
                    tgb.text("{antal_utbildningsområden}", class_name="bold-italic", mode="md")
            # Visa diagrammet (diagrammet uppdateras via callback-funktionen)
            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig}")

