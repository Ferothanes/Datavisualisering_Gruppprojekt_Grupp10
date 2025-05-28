import taipy.gui.builder as tgb
from backend.backend_anordnare import (
    df_an,
    get_anordnare,
    update_kpi,
    count_beslut,
    get_utbildningsområden,
    fig_top_10_sökta,
    fig_top_10_beviljade
)
from backend.startvalues import get_start_values


#-- Hämtar startvärden från get_start_values
start_values = get_start_values(df_an)

selected_anordnare = start_values["selected_anordnare"]
selected_year = start_values["selected_year"]
selected_year_str = start_values["selected_year_str"]
selected_year_lov = start_values["selected_year_lov"]

utbildningsområden = start_values["utbildningsområden"]
utbildningsområden_text = start_values["utbildningsområden_text"]

poäng = start_values["poäng"]
kommuner = start_values["kommuner"]
län = start_values["län"]
huvudmannatyp = start_values["huvudmannatyp"]

beviljade = start_values["beviljade"]
ej_beviljade = start_values["ej_beviljade"]
beviljandegrad = start_values["beviljandegrad"]


fig_top_10_sökta = start_values["fig_top_10_sökta"]
fig_top_10_beviljade = start_values["fig_top_10_beviljade"]

#-- Bygger dashboarden
with tgb.Page() as anordnare:
    with tgb.part(class_name="container card stack-large anordnare-page"):
        tgb.navbar()

        # -- Huvudrubrik
        with tgb.part(class_name="card centered"):
            tgb.text("# Filtrera utbildningsanordnare", mode="md")
            tgb.selector(
                "Anordnare",
                value="{selected_anordnare}",
                lov=sorted(df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()),
                dropdown=True,
            )
            tgb.selector(
                "År",
                value="{selected_year}",
                lov="{selected_year_lov}",
                dropdown=True,
            )
            tgb.button("Visa statistik", on_action=update_kpi, class_name="filled-button")


#--- Row: Information + Ansökningar
    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card center-text"):
            tgb.text("## Information gällande {selected_anordnare} - år {selected_year_str}", mode="md")
            tgb.text("**{selected_anordnare} har ansökt om att bedriva utbildningar på följande platser:**", mode="md")
            tgb.text("**Kommun(er): {kommuner}**", mode="md")
            tgb.text("**Län: {län}**", mode="md")

        with tgb.part(class_name="card center-text"):
            tgb.text("## Ansökningar:", mode="md")
            tgb.text("**{beviljade} Stycken beviljade**", class_name="kpi", mode="md")
            tgb.text("**{ej_beviljade} Stycken ej beviljade**", class_name="kpi", mode="md")

    #--- Row: Statistik + Utbildningsområden
    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card center-text"):
            tgb.text("## Beviljade utbildningsområden:", mode="md")
            tgb.text("**{utbildningsområden_text}**", class_name="kpi", mode="md")

        with tgb.part(class_name="card center-text"):
            tgb.text("## Statistik:", mode="md")
            tgb.text("**Ägartyp: {huvudmannatyp}**", class_name="kpi", mode="md")
            tgb.text("**{beviljandegrad}% Beviljandegrad för sina ansökningar**", class_name="kpi", mode="md")
            tgb.text("**Erhöll {poäng} beviljade poäng**", class_name="kpi", mode="md")

    #---Top 10 sökta och beviljade 

    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card center-text"):
            tgb.chart(figure="{fig_top_10_sökta}")
        with tgb.part(class_name="card center-text"):
            tgb.chart(figure="{fig_top_10_beviljade}")

    
            











   





    

