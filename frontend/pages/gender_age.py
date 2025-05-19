# Gender_graph.py
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
        title='Men vs Women Applicants per Education Field (2023 & 2024) - Top 10',
        color_discrete_map={'Women': 'lightblue', 'Men': 'grey'}
    )

    fig.update_layout(
        height=700,
        xaxis_title='',
        yaxis_title='',
        legend_title='Gender',
        paper_bgcolor='white',
        plot_bgcolor='white',
        title=dict(text='Men vs Women Applicants per Education Field (2023 & 2024) - Top 10',
                   font=dict(color='#334850', size=20)),
        xaxis=dict(showline=True, linewidth=1, linecolor='black', ticks='outside'),
        yaxis=dict(tickfont=dict(color='#334850', size=13)),
        hoverlabel=dict(font=dict(color='white', size=15), bgcolor='darkblue', bordercolor='black')
    )

    return fig


gender_chart = gender_graph()  # Call the function and get the dict

with tgb.Page() as gender_age: #page_name
    with tgb.part(class_name="container card stack-large"):
        tgb.text("# MYH dashboard 2023-2024", mode="md")
        with tgb.layout(columns="2 1"):
            # Display the gender chart using the content returned
            with tgb.part(class_name="card"):
                tgb.chart(figure = '{gender_chart}')

