import pandas as pd
import duckdb
import numpy as np
import json
from difflib import get_close_matches
import plotly.graph_objects as go
from pathlib import Path
import taipy.gui.builder as tgb

# ======= Filvägar =======

DATA_PATH = Path("data/sammanfogad_kurser_inom_yh_2020-2024.xlsx")
GEO_PATH = Path("data/swedish_regions.geojson")
fig_map = go.Figure()



def load_map_data():
    global fig_map
    df = pd.read_excel(DATA_PATH)
    df["År"] = df["År"].astype(str).str.replace(",", "").astype(int)
    df_filtered = df[df["År"] == 2024]

    df_regions = duckdb.query("""
        SELECT 
            län, 
            COUNT_IF(beslut = 'Beviljad') AS Beviljade
        FROM df_filtered
        WHERE 
            län NOT IN ('Flera kommuner', 'Se "Lista flera kommuner"')
        GROUP BY län
        ORDER BY Beviljade DESC
    """).df()

    df_regions.columns = [col.strip().capitalize() for col in df_regions.columns]

    with open(GEO_PATH, encoding="utf-8") as file:
        geojson = json.load(file)

    properties = [feature.get("properties") for feature in geojson.get("features")]
    region_codes = {prop.get("name"): prop.get("ref:se:länskod") for prop in properties}

    region_codes_map = []
    for region in df_regions["Län"]:
        match = get_close_matches(region, region_codes.keys(), n=1)
        region_codes_map.append(region_codes[match[0]] if match else "")

    df_regions["Länskod"] = region_codes_map
    df_regions["log_beviljade"] = np.log(df_regions["Beviljade"] + 1)

    fig_map = go.Figure(go.Choropleth(
        geojson=geojson,
        locations=df_regions["Länskod"],
        z=df_regions["log_beviljade"],
        featureidkey="properties.ref:se:länskod",
        colorscale="Blues",
        customdata=df_regions["Beviljade"],
        text=df_regions["Län"],
        hovertemplate="<b>%{text}</b><br>Beviljade: %{customdata}<extra></extra>",
        marker_line_width=0.5,
        marker_line_color="white",
        showscale=False
    ))

    fig_map.update_geos(
        visible=False,
        showcountries=False,
        showsubunits=False,
        fitbounds="locations",
        lataxis_range=[54.5, 69.2],
        lonaxis_range=[10, 25]
    )

    fig_map.update_layout(
        geo=dict(
            scope="europe",
            projection_type="mercator",
            bgcolor="#ffffff",
        ),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        width=800,
        height=700,
        title={
            "x": 0.5,
            "font": dict(size=22, color="#050505", family="Arial, sans-serif")
        },
        paper_bgcolor="#ffffff",
    )

# Kör direkt
load_map_data()

# ======= Taipy-sida =======
# ======= Taipy-sida med layout och textbeskrivning =======
with tgb.Page() as map_page:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        tgb.text("## Karta över beviljade YH-kurser per län (2024)", mode="md")
        with tgb.layout(columns="70% 30%"):  # karta till vänster, text till höger
            tgb.chart(figure="{fig_map}")
            tgb.text("""
**Om kartan:**  
Den här kartan visar hur många YH-kurser som blivit beviljade i varje län under 2024.  
Ju mörkare färg, desto fler kurser.
            """, mode="md")