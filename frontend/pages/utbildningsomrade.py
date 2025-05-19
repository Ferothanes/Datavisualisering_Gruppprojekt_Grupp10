import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px

def student_area_graph():
    # Load the data
    df = pd.read_excel("data/Antalet studerande i YH inom olika utbildningsområden 2012-2024.xlsx")

    # Drop unwanted columns if they exist
    columns_to_exclude = ['Totalt', 'Övrigt']
    df = df.drop(columns=[col for col in columns_to_exclude if col in df.columns])

    # Melt the data to long format
    df_long = df.melt(id_vars='År', var_name='Utbildningsområde', value_name='Antal studerande')

    # Create area chart
    fig = px.line(
        df_long,
        x='År',
        y='Antal studerande',
        color='Utbildningsområde',
        title='Antalet studerande i YH inom olika utbildningsområden (2012–2024)',
        labels={'År': 'År', 'Antal studerande': 'Antal studerande'},
        template='plotly_white'
    )

    # Add markers (circles) to all visible and hidden traces
    for trace in fig.data:
        trace.mode = "lines+markers"

    # Hide all traces except "Data/It"
    for trace in fig.data:
        if trace.name != "Data/It":
            trace.visible = "legendonly"


    # Improve axes appearance
    fig.update_xaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey')
    fig.update_yaxes(
    showgrid=False,
    ticks="outside",
    showline=True,
    linecolor='grey')


    fig.update_xaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey',type='category')
    fig.update_yaxes(showgrid=False, ticks="outside", showline=True, linecolor='grey')


    # Customize legend title
    fig.update_layout(
        legend_title_text='Utbildningsområde')

    return fig



#tgb.chart(figure=student_area_graph())


student_area_graph = student_area_graph()

with tgb.Page() as utbildningsomrade: #page_name
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()
        tgb.text("# MYH dashboard 2023-2024", mode="md")
        with tgb.layout(columns="2 1"):
            # Display the gender chart using the content returned
            with tgb.part(class_name="card"):
                tgb.chart(figure = '{student_area_graph}')