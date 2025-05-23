import pandas as pd
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from utils.constants import DATA_DIRECTORY

# Ladda in data från Excel-filer för 2020, 2021, 2022, 2023 och 2024
df_files = {
    "2024": pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh (1).xlsx", sheet_name="Lista ansökningar"),
    "2023": pd.read_excel(DATA_DIRECTORY / "resultat-2023-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    "2022": pd.read_excel(DATA_DIRECTORY / "resultat-2022-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    "2021": pd.read_excel(DATA_DIRECTORY / "resultat-juni-2021-for-korta-utbildningar-kurser-och-kurspaket.xlsx", sheet_name="Lista beviljade ansökningar"),
    "2020": pd.read_excel(DATA_DIRECTORY / "ANS_L12_Beviljade-korta-utb-kurser-kurspaket-YH-juli-2020-2.xlsx", sheet_name="Lista beviljade utbildningar")
}

# Funktion för att räkna antalet unika anordnare, ta hänsyn till att kolumnnamnet kan vara "Anordnare namn" eller "Anordnare"
def get_anordnare_count(df):
    if "Anordnare namn" in df.columns:
        return df["Anordnare namn"].nunique()
    elif "Anordnare" in df.columns:
        return df["Anordnare"].nunique()
    else:
        return 0

# Beräkna statistik för valt år (default = 2024)
selected_year = "2024"
df_selected = df_files[selected_year]
antal_kurser = df_selected.shape[0]
antal_anordnare = get_anordnare_count(df_selected)
antal_utbildningsområden = df_selected["Utbildningsområde"].nunique()

def count_beviljade_per_utbildningsområde(df):
    # Om kolumnen "Beslut" finns, filtrera på "Beviljad"; annars anta att alla rader är beviljade.
    if "Beslut" in df.columns:
        df_filtered = df[df["Beslut"] == "Beviljad"]
    else:
        df_filtered = df
    # Grupppera efter "Utbildningsområde" och räkna antalet kurser
    return df_filtered.groupby("Utbildningsområde").size().reset_index(name="Antal beviljade kurser")

# Skapa standarddiagrammet med 2024-data
df_kurser_utbildningsområde_default = count_beviljade_per_utbildningsområde(df_selected)
fig_bar = px.bar(
    df_kurser_utbildningsområde_default,
    y="Utbildningsområde",
    x="Antal beviljade kurser",
    title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
    orientation='h',
    width=950
)
fig_bar.update_layout(
    paper_bgcolor="white",
    plot_bgcolor="white"
)


fig_pie = px.pie(
    df_kurser_utbildningsområde_default,
    names="Utbildningsområde",
    values="Antal beviljade kurser",
    title=f"Andel beviljade kurser per utbildningsområde ({selected_year})",
    width=950
)

def update_year(state):
    global selected_year, antal_kurser, antal_anordnare, antal_utbildningsområden, fig_bar, fig_pie
    # Uppdatera det valda året enligt användarens val i selektorn
    selected_year = state.selected_year
    df_new = df_files[selected_year]
    
    # Uppdatera statistik
    antal_kurser = df_new.shape[0]
    antal_anordnare = get_anordnare_count(df_new)
    antal_utbildningsområden = df_new["Utbildningsområde"].nunique()
    
    # Uppdatera diagrammen med data för det valda året
    df_kurser_updated = count_beviljade_per_utbildningsområde(df_new)
    fig_bar = px.bar(
        df_kurser_updated,
        y="Utbildningsområde",
        x="Antal beviljade kurser",
        title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
        orientation='h',
        width=950
    )
    fig_pie = px.pie(
        df_kurser_updated,
        names="Utbildningsområde",
        values="Antal beviljade kurser",
        title=f"Andel beviljade kurser per utbildningsområde ({selected_year})",
        width=950
    )
    
    # Återspegla de nya värdena i state-objektet så att de visas i dashboarden
    state.antal_kurser = antal_kurser
    state.antal_anordnare = antal_anordnare
    state.antal_utbildningsområden = antal_utbildningsområden
    state.fig_bar = fig_bar
    state.fig_pie = fig_pie

with tgb.Page() as ansökningar:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="card"):
            tgb.text("# MYH dashboard", class_name="center-text red-text", mode="md")
            tgb.selector("{selected_year}", lov=["2024", "2023", "2022", "2021", "2020"], dropdown=True, on_change=update_year)
            tgb.text("## Dashboard för statistik och ansökningar", class_name="center-text", mode="md")
            
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
            

            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig_pie}")
            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig_bar}")
            # Visa bilden som finns i assets/images (donut_chart.png) under pie-charten.
            with tgb.part(class_name="card text-row"):
                tgb.image("../assets/images/donut_chart.png", width="800px", style="display: block; margin-left: auto; margin-right: 0;")
