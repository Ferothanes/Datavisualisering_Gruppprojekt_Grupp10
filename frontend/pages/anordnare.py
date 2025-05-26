import taipy.gui.builder as tgb
from backend.backend_anordnare import (
    df_an,
    get_anordnare,
    update_kpi,
    count_beslut,
    get_utbildningsområden,
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
# statsbidrag_mkr = start_values.get("statsbidrag_mkr", 0)


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

        # -- Information
        with tgb.part(class_name="card centered"):
            tgb.text("### Information gällande {selected_anordnare} - år {selected_year_str}", mode="md")
            tgb.text("**{selected_anordnare} har ansökt om att bedriva utbildningar på följande platser:**", mode="md")
            tgb.text("**Kommun(er):** {kommuner}", mode="md")
            tgb.text("**Län:** {län}", mode="md")

        # -- Ansökningar
        with tgb.part(class_name="card centered"):
            tgb.text("#### Ansökningar:", mode="md")
            tgb.text("**{beviljade} Stycken beviljade**", class_name="kpi", mode="md")
            tgb.text("**{ej_beviljade} Stycken ej beviljade**", class_name="kpi", mode="md")

        # -- Utbildningsområden
        with tgb.part(class_name="card centered"):
            tgb.text("#### Beviljade utbildningsområden:", mode="md")
            tgb.text("**{utbildningsområden_text}**", class_name="kpi", mode="md")

        # -- Statistik
        with tgb.part(class_name="card centered"):
            tgb.text("#### Statistik:", mode="md")
            tgb.text("**Ägartyp:** {huvudmannatyp}", class_name="kpi", mode="md")
            tgb.text("**{beviljandegrad}% Beviljandegrad för sina ansökningar**", class_name="kpi", mode="md")
            # tgb.text("**Erhöll {statsbidrag_mkr} miljoner kronor i statliga medel**", class_name="kpi", mode="md")
            tgb.text("**Erhöll {poäng} beviljade poäng**", class_name="kpi", mode="md")
