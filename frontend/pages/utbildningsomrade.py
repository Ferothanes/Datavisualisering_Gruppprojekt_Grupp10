import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px


def student_area_graph():
    df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")

    df_long = df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')

    fig = px.line(
        df_long,
        x='År',
        y='Antal studerande',
        color='Utbildningsområde',
        labels={'År': 'År', 'Antal studerande': 'Antal studerande'},
        template='plotly_white'
    )

    # Visade linjer vid start
    visible_areas = [
        "Ekonomi, administration och försäljning",
        "Teknik och tillverkning",
        "Hälso- och sjukvård samt socialt arbete",
        "Data/It"
    ]

    # Set color for all lines and markers and manage visibility
    for trace in fig.data:
        #trace.mode = "lines+markers"
        trace.line.color = '#23afe0'      # set line color
        #trace.marker.color = '#51abcb'    # set marker color
        if trace.name in visible_areas: # Show the four areas by default, others hidden in legend onl
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

education_areas = sorted(df_long['Utbildningsområde'].dropna().unique().tolist())
selected_education = education_areas[0]

def make_figure(area):
    filtered_df = df_long[df_long['Utbildningsområde'] == area].copy()
    filtered_df['År'] = filtered_df['År'].astype(str)  # Convert to string for categorical x-axis
    
    fig = px.bar(
        filtered_df,
        x='År',
        y='Antal studerande',
        labels={'År': 'År', 'Antal studerande': 'Antal studerande'},
        template='plotly_white'
    )

    # Set bar color
    for trace in fig.data:
        trace.marker.color = '#51abcb'

    fig.update_layout(
        xaxis=dict(type='category', showgrid=False, showline=True, linecolor='grey'),
        yaxis=dict(title='Antal studerande', showgrid=False, showline=True, linecolor='grey'),
        margin=dict(t=40, b=40),
        xaxis_title=''
    )
    
    return fig

fig = make_figure(selected_education)

def update_figure(state):
    state.fig = make_figure(state.selected_education)




# ---------- Page
with tgb.Page() as utbildningsomrade:
    with tgb.part(class_name="container card stack-large utbildning-page"):
        tgb.navbar()

        tgb.text("## Studerande i YH – utveckling över tid\n"
                 "Detta linjediagram visualiserar trender i antalet studerande inom olika utbildningsområden (2005-2024).\n"
                  "Fyra områden med flest studerande visas som standard för att ge en tydlig överblick, medan övriga områden finns tillgängliga via legendens urval..", mode="md")

        # --- First card: Static line chart
        with tgb.part(class_name="card"):
            tgb.chart(figure="{student_area_graph}")

        # --- Second card: Dynamic bar chart with dropdown
        with tgb.part(class_name="card"):
            tgb.text("## Denna figur visar antalet studerande för ett valt utbildningsområde över flera år.\n" 
            "Stapeldiagrammet är kategoriserat efter år och visualiserar förändringar i antalet studerande", mode="md")

            tgb.selector(
                label="Välj utbildningsområde",
                value="{selected_education}",
                lov=education_areas,
                dropdown=True,
                on_change=update_figure
            )
            tgb.chart(figure="{fig}")

        with tgb.part(class_name="card"):
            tgb.image("assets/images/storytelling_Data_It.png", width="1000px")




            
