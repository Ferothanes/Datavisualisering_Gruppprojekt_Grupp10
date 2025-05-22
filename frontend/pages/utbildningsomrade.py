import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px


def student_area_graph():
    df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")
    df_long = df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')

    blue_colors = [
        "#057DA8", 
        "#39B8E4",  
        "#839CF1",  
        "#667fd2",
        "#2141ab",
        "#61BDB3",
        "#27C557"
    ]

    fig = px.line(
        df_long,
        x='År',
        y='Antal studerande',
        color='Utbildningsområde',
        labels={'År': 'År', 'Antal studerande': 'Antal studerande'},
        template='plotly_white',
        color_discrete_sequence = blue_colors # Bättre färger än default 
    )

    # Visade linjer vid start
    visible_areas = [
        "Ekonomi, administration och försäljning",
        "Teknik och tillverkning",
        "Hälso- och sjukvård samt socialt arbete",
        "Data/It"
    ]

    # Show the four areas by default, others hidden in legend onl
    for trace in fig.data:
        #trace.mode = "lines+markers"
        if trace.name in visible_areas: 
            trace.visible = True
        else:
            trace.visible = "legendonly"

    # Improve axes appearance
    fig.update_xaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey', type='category')
    fig.update_yaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey')

    fig.update_layout(
        legend_title_text='Utbildningsområde',
        xaxis_title='')

    return fig

student_area_graph = student_area_graph()




# ---------- Second dynamic graph with dropdown (bar chart)

df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")

df_long = df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')
df_long['Utbildningsområde'] = df_long['Utbildningsområde'].astype(str).str.strip()

years = sorted(df_long['År'].dropna().astype(str).unique().tolist())
selected_year = years[0]

def make_figure(year):
    filtered_df = df_long[df_long['År'].astype(str) == year].copy()

    fig = px.bar(
        filtered_df,
        y='Utbildningsområde',
        x='Antal studerande',
        orientation='h',
        labels={'Utbildningsområde': 'Utbildningsområde', 'Antal studerande': 'Antal studerande'},
        template='plotly_white'
    )

    # Set bar color
    for trace in fig.data:
        trace.marker.color = '#51abcb'

    fig.update_layout(
        xaxis=dict(title='Antal studerande', showgrid=False, showline=True, linecolor='grey'),
        yaxis=dict(type='category', showgrid=False, showline=True, linecolor='grey'),
        margin=dict(t=40, b=40),
        yaxis_title=''
    )

    return fig

fig = make_figure(selected_year)

def update_figure(state):
    state.fig = make_figure(state.selected_year)




# ---------- Page
with tgb.Page() as utbildningsomrade:
    with tgb.part(class_name="container card stack-large utbildning-page"):
        tgb.navbar()

        tgb.text("## Studerande i YH – utveckling över tid\n"
                 "Detta linjediagram visualiserar trender i antalet studerande inom olika utbildningsområden (2005-2024)."
                  "Fyra områden med flest studerande visas som standard för att ge en tydlig överblick, medan övriga områden finns tillgängliga via legendens urval.", mode="md")

        # --- First card: Static line chart
        with tgb.part(class_name="card"):
            tgb.chart(figure="{student_area_graph}")

        # --- Second card: Dynamic bar chart with dropdown
        with tgb.part(class_name="card"):
            tgb.text("## Antalet studerande för valt år inom alla utbildningsområden (2005-2024)\n" 
            "Stapeldiagrammet är kategoriserat efter utbildningsområde och visualiserar förändringar i antalet studerande", mode="md")

            tgb.selector(
                label="Välj år",
                value="{selected_year}",
                lov=years,
                dropdown=True,
                on_change=update_figure
            )
            tgb.chart(figure="{fig}")

        with tgb.part(class_name="card"):
            tgb.image("assets/images/storytelling_Data_It.png", width="1000px")
