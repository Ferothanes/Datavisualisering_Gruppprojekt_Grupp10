import taipy.gui.builder as tgb
from taipy.gui import Gui
from backend.backend_anordnare import (
    df_an,
    get_anordnare,
    update_kpi,
    count_beslut,
    get_utbildningsområden,
)
# from backend.get_statsbidrag import count_statsbidrag

# Initiera startvärden
selected_anordnare = df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()[0]
selected_year = int(df_an[df_an["Utbildningsanordnare administrativ enhet"] == selected_anordnare]["År"].max())
selected_year_str = str(selected_year)
selected_year_lov = sorted([int(y) for y in df_an["År"].unique()], reverse=True)
utbildningsområden = get_utbildningsområden(df_an, selected_anordnare, selected_year)

poäng, kommuner, län, huvudmannatyp = get_anordnare(df_an, selected_anordnare, selected_year)
beviljade, ej_beviljade = count_beslut(df_an, selected_anordnare, selected_year)

utbildningsområden_text = ", ".join(utbildningsområden)
beviljandegrad = round(beviljade / (beviljade + ej_beviljade) * 100, 1) if (beviljade + ej_beviljade) > 0 else 0.0
# statsbidrag_mkr = count_statsbidrag(selected_anordnare, selected_year)

#-- Göra GUI
with tgb.Page() as anordnare:
    with tgb.part(class_name="container card stack-large anordnare-page"):
        tgb.navbar()

        #-- Huvurubrik
        with tgb.part(class_name="card centered"):
            tgb.text("# Filtrera utbildningsanordnare", mode="md")
            tgb.selector("Anordnare", value="{selected_anordnare}",
                         lov=sorted(df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()),
                         dropdown=True,)
            tgb.selector("År", value="{selected_year}",
                         lov="{selected_year_lov}",
                         dropdown=True)
            tgb.button("Visa statistik", on_action=update_kpi, class_name="filled-button")

        #-- Inforubrik
        with tgb.part(class_name="card centered"):
            tgb.text("### Information gällande {selected_anordnare} - år {selected_year_str}", mode="md")
            tgb.text("**{selected_anordnare} har ansökt om att bedriva utbildningar på följande platser:**", mode="md")
            tgb.text("**Kommun(er):** {kommuner}", mode="md")
            tgb.text("**Län:** {län}", mode="md")

        # --Ansökningar
        with tgb.part(class_name="card centered"):
            tgb.text("#### Ansökningar:", mode="md")
            tgb.text("**{beviljade} Stycken beviljade**", class_name="kpi", mode="md")
            tgb.text("**{ej_beviljade} Stycken ej beviljade**", class_name="kpi", mode="md")

        # BeviljadeUtbildningsområden
        with tgb.part(class_name="card centered"):
            tgb.text("#### Beviljade utbildningsområden:", mode="md")
            tgb.text("**{utbildningsområden_text}**", class_name="kpi", mode="md")

        # Statistik
        with tgb.part(class_name="card centered"):
            tgb.text("#### Statistik:", mode="md")
            tgb.text("**Ägartyp:** {huvudmannatyp}", class_name="kpi", mode="md")
            tgb.text("**{beviljandegrad}% Beviljandegrad för sina ansökningar**", class_name="kpi", mode="md")
            # tgb.text("**Erhöll {statsbidrag_mkr} miljoner kronor i statliga medel**", class_name="kpi", mode="md")
            tgb.text("**Erhöll {poäng} beviljade poäng**", class_name="kpi", mode="md")

#-- applikationen
if __name__ == "__main__":
    Gui(anordnare).run(
        use_reloader=False,
        debug=True,
        variables={
            "selected_anordnare": selected_anordnare,
            "selected_year": selected_year,
            "selected_year_str": selected_year_str,
            "selected_year_lov": selected_year_lov,
            "poäng": poäng,
            "kommuner": kommuner,
            "län": län,
            "huvudmannatyp": huvudmannatyp,
            "beviljade": beviljade,
            "ej_beviljade": ej_beviljade,
            "utbildningsområden": utbildningsområden,
            "utbildningsområden_text": utbildningsområden_text,
            "beviljandegrad": beviljandegrad,
            # "statsbidrag_mkr": statsbidrag_mkr,
        },
        functions={
            "update_kpi": update_kpi
        }
    )


