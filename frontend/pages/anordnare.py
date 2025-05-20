import taipy.gui.builder as tgb
from backend.data_processing import df_an, get_anordnare

# -- Startvärden
selected_anordnare = df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()[0]
selected_year = int(df_an[df_an["Utbildningsanordnare administrativ enhet"] == selected_anordnare]["År"].max())
selected_year_str = str(selected_year)
selected_year_lov = sorted([int(y) for y in df_an["År"].unique()], reverse=True)

poäng, kommuner, län, huvudmannatyp = get_anordnare(df_an, selected_anordnare, selected_year)


def update_kpi(state):
    print("Vald anordnare:", state.selected_anordnare)

    år_för_anordnare = df_an[
        df_an["Utbildningsanordnare administrativ enhet"] == state.selected_anordnare
    ]["År"].unique()

    år_för_anordnare = sorted([int(år) for år in år_för_anordnare], reverse=True)
    print("Tillgängliga år för anordnaren:", år_för_anordnare)

    # Uppdatera årens lov
    state.selected_year_lov = år_för_anordnare

    # Om nuvarande år inte finns, byt till första tillgängliga
    if state.selected_year not in år_för_anordnare:
        state.selected_year = år_för_anordnare[0]

    poäng, kommuner, län, huvudmannatyp = get_anordnare(
        df_an, state.selected_anordnare, state.selected_year
    )

    state.poäng = poäng
    state.kommuner = kommuner
    state.län = län
    state.selected_year_str = str(state.selected_year)
    state.huvudmannatyp = huvudmannatyp


with tgb.Page() as page:
    with tgb.part(class_name="card"):
        tgb.text("## Filtrera utbildningsanordnare", mode="md")

        tgb.selector(
            "Anordnare",
            value="{selected_anordnare}",
            lov = sorted(df_an["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()),
            dropdown=True,
        )

        tgb.selector(
            "År",
            value="{selected_year}",
            lov="{selected_year_lov}",
            dropdown=True,
        )

        tgb.button("Visa statistik", on_action=update_kpi)

    tgb.text("### KPI:er för {selected_anordnare} - år      {selected_year_str}", mode="md")

    with tgb.layout(columns="1 1 1"):
        tgb.text("{poäng} Beviljade poäng", class_name="kpi")
        tgb.text("För {kommuner} Kommuner i {län} Län", class_name="kpi")
        tgb.text("Ägartyp: {huvudmannatyp}", class_name="kpi")
        


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
            "huvudmannatyp": huvudmannatyp

        }
    )


