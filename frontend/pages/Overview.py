import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px


def gender_graph():
    df = pd.read_excel("data/Utbildningsansökning_age.xlsx", sheet_name='Education')

    for col in ['Total', 'Women', 'Men']:
        df[col] = df[col].astype(str).str.replace(' ', '').astype(int)

    df_filtered = df[df['Year'].isin([2023, 2024])].copy()
    df_filtered['TotalApplicants'] = df_filtered['Women'] + df_filtered['Men']

    df_grouped = df_filtered.groupby('Education').agg(
        Women=('Women', 'sum'),
        Men=('Men', 'sum'),
        TotalApplicants=('TotalApplicants', 'sum')
    ).reset_index()

    top_10 = df_grouped.sort_values(by='TotalApplicants', ascending=True).tail(10)

    melted = top_10.melt(
        id_vars=['Education'],
        value_vars=['Women', 'Men'],
        var_name='Gender',
        value_name='Applicants'
    )

    fig = px.bar(
        melted,
        x='Applicants',
        y='Education',
        color='Gender',
        barmode='overlay',
        orientation='h',
        color_discrete_map={'Women': 'lightblue', 'Men': 'grey'}
    )

    fig.update_layout(
        height=600,
        xaxis_title='',
        yaxis_title='',
        legend_title='Gender',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showline=True, linewidth=1, linecolor='black', ticks='outside'),
        yaxis=dict(tickfont=dict(color='#334850', size=13)),
        hoverlabel=dict(font=dict(color='#0b2d39', family="Inter", size=15))
    )

    return fig

#Age graph---------------------------

def age_graph():
    # Read the data
    df = pd.read_excel("data/Utbildningsansökning_age.xlsx", sheet_name="Age")
    df.columns = df.columns.str.strip()  # Remove any leading/trailing spaces in column names

    # Reshape data for grouped bar chart
    df_melted = df.melt(
        id_vars=["Age groups"],
        value_vars=["Women", "Men"],
        var_name="Gender",
        value_name="Applications"
    )

    # Create grouped bar chart
    fig = px.bar(
        df_melted,
        x="Age groups",
        y="Applications",
        color="Gender",
        barmode="group",
        labels={"Applications": "Antal ansökningar"},
        color_discrete_map={"Women": "lightblue", "Men": "grey"}
    )

    fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    hoverlabel=dict(font=dict(color='#0b2d39', family="Inter", size=15)),
    yaxis=dict(
        showline=True,
        linecolor='grey',
        ticks="outside") 
        ),
    

    return fig  



gender_chart = gender_graph()  # Call the function and get the dict
age_graph = age_graph()



with tgb.Page() as gender_age:  # page_name
    with tgb.part(class_name="container card stack-large overview-page"):
        tgb.navbar()

        tgb.text("## Demografisk översikt: Kön och ålder ", mode="md")
        with tgb.part(class_name="card"):
            tgb.text(
                "## Män vs. Kvinnor som sökt per utbildningsområde (2023 & 2024) – Topp 10", mode="md")
            tgb.chart(figure='{gender_chart}')

        with tgb.part(class_name="card"):
            tgb.text(
                "## Män vs. Kvinnor per åldersgrupp (2022-2024)\n"
                "Detta diagram visar könsfördelningen bland utbildningsansökningar uppdelat på olika åldersgrupper.\n"
                "X-axeln representerar de olika åldersgrupperna, medan Y-axeln visar antal inkomna ansökningar.\n"
                "Färgerna visualiserar kön: **ljusblå för kvinnor** och **grå för män**.",
                mode="md")
            tgb.chart(figure='{age_graph}')
