import taipy.gui.builder as tgb
from backend.backend_anordnare import df_an, get_anordnare, update_kpi, count_beslut, get_utbildningsområden

# -- Startvärden
selected_anordnare = df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()[0]
selected_year = int(df_an[df_an["Utbildningsanordnare administrativ enhet"] == selected_anordnare]["År"].max())
selected_year_str = str(selected_year)
selected_year_lov = sorted([int(y) for y in df_an["År"].unique()], reverse=True)
utbildningsområden = get_utbildningsområden(df_an, selected_anordnare, selected_year)

poäng, kommuner, län, huvudmannatyp = get_anordnare(df_an, selected_anordnare, selected_year)
beviljade, ej_beviljade = count_beslut(df_an, selected_anordnare, selected_year)

utbildningsområden = get_utbildningsområden(df_an, selected_anordnare, selected_year)
utbildningsområden_text = "\\n".join(f"- {område}" for område in utbildningsområden)

beviljandegrad = round(beviljade / (beviljade + ej_beviljade) * 100, 1) if (beviljade + ej_beviljade) > 0 else 0.0



# -- GUI-sida
with tgb.Page() as page:
    with tgb.part(class_name="card"):
        tgb.text("## Filtrera utbildningsanordnare", mode="md")

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

        tgb.button("Visa statistik", on_action=update_kpi)

    tgb.text("### KPI:er för {selected_anordnare} - år {selected_year_str}", mode="md")
    with tgb.part(class_name="centered"):
        with tgb.layout(columns="1 1 1"):
            tgb.text("{poäng} Beviljade poäng", class_name="kpi")
            tgb.text("För {kommuner} Kommuner i {län} Län", class_name="kpi")
            tgb.text("Ägartyp: {huvudmannatyp}", class_name="kpi")

        with tgb.layout(columns="1 1"):
            tgb.text("{beviljade} Beviljade ansökningar", class_name="kpi")
            tgb.text("{ej_beviljade} Ej beviljade ansökningar", class_name="kpi")

    with tgb.part(class_name="centered"):
        tgb.text("# Beviljade utbildningsområden", mode="md")
        tgb.text("{utbildningsområden_text}", mode="md")

    with tgb.part(class_name="centered"):
        tgb.text("{beviljandegrad}% beviljandegrad", class_name="kpi")





if __name__ == "__main__":
    from taipy.gui import Gui

    Gui(page).run(
        use_reloader=False,
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


        }
    )


