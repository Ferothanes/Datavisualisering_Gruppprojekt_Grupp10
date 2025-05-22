import pandas as pd
import plotly.express as px
from taipy.gui import Gui
import taipy.gui.builder as tgb
from utils.constants import DATA_DIRECTORY

# Blue color palette for pie chart
blue_colors = [
    "#27C557",
    "#39B8E4",
    "#057DA8",
    "#61BDB3",
    "#2141ab",
    "#D0E89F",
    "#E09048"
]

# Load data from Excel files for 2024, 2023, and 2022
df_files = {
    "2024": pd.read_excel(DATA_DIRECTORY / "resultat-2024-for-kurser-inom-yh (1).xlsx", sheet_name="Lista ansökningar"),
    "2023": pd.read_excel(DATA_DIRECTORY / "resultat-2023-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar"),
    "2022": pd.read_excel(DATA_DIRECTORY / "resultat-2022-for-kurser-inom-yh.xlsx", sheet_name="Lista ansökningar")
}

# Default selected year
selected_year = "2024"
df_selected = df_files[selected_year]
antal_kurser = df_selected.shape[0]
antal_anordnare = df_selected["Anordnare namn"].nunique()
antal_utbildningsområden = df_selected["Utbildningsområde"].nunique()

def count_beviljade_per_utbildningsområde(df):
    df_beviljade = df[df["Beslut"] == "Beviljad"]
    return df_beviljade.groupby("Utbildningsområde").size().reset_index(name="Antal beviljade kurser")

def create_pie_chart(df):
    # Filter only 'Beviljad'
    df_beviljad = df[df["Beslut"] == "Beviljad"]

    # Count per utbildningsområde among beviljade
    fördelning_beviljad = df_beviljad["Utbildningsområde"].value_counts().reset_index()
    fördelning_beviljad.columns = ["Utbildningsområde", "Antal"]

    # Sort and pick top 8 utbildningsområden
    top_8_beviljade = fördelning_beviljad.sort_values(by="Antal", ascending=False).head(8)

    # Draw pie chart with percentage info
    fig = px.pie(
        top_8_beviljade,
        names="Utbildningsområde",
        values="Antal",
        title=f"Topp 8 beviljade utbildningsområden ({selected_year})",
        hole=0.2,
        color_discrete_sequence=blue_colors
    )

    fig.update_traces(
        textinfo='percent',
        textfont=dict(size=16, color='white', family='Arial Black')
    )
    return fig

# Initial charts
df_kurser_utbildningsområde_default = count_beviljade_per_utbildningsområde(df_selected)
fig_bar = px.bar(
    df_kurser_utbildningsområde_default,
    y="Utbildningsområde",
    x="Antal beviljade kurser",
    title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
    orientation='h'
)
fig_pie = create_pie_chart(df_selected)

def update_year(state):
    global selected_year, antal_kurser, antal_anordnare, antal_utbildningsområden, fig_bar, fig_pie
    selected_year = state.selected_year
    df_new = df_files[selected_year]

    # Update stats
    antal_kurser = df_new.shape[0]
    antal_anordnare = df_new["Anordnare namn"].nunique()
    antal_utbildningsområden = df_new["Utbildningsområde"].nunique()

    # Update charts
    df_kurser_updated = count_beviljade_per_utbildningsområde(df_new)
    fig_bar = px.bar(
        df_kurser_updated,
        y="Utbildningsområde",
        x="Antal beviljade kurser",
        title=f"Antal beviljade kurser per utbildningsområde ({selected_year})",
        orientation='h'
    )
    fig_pie = create_pie_chart(df_new)

    # Reflect new values in state
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
            tgb.selector("{selected_year}", lov=["2024", "2023", "2022"], dropdown=True, on_change=update_year)
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
                tgb.chart(figure="{fig_bar}")
            with tgb.part(class_name="card text-row"):
                tgb.chart(figure="{fig_pie}")
