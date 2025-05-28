from backend.backend_anordnare import (
    get_anordnare,
    count_beslut,
    get_utbildningsområden,
    fig_top_10_sökta, 
    fig_top_10_beviljade
)

#---  Skapar Startvärden för dashboarden
def get_start_values(df):
    selected_anordnare = df["Utbildningsanordnare administrativ enhet"].dropna().astype(str).unique()[0]
    selected_year = int(df[df["Utbildningsanordnare administrativ enhet"] == selected_anordnare]["År"].max())
    selected_year_str = str(selected_year)
    selected_year_lov = sorted([int(y) for y in df["År"].unique()], reverse=True)

    utbildningsområden = get_utbildningsområden(df, selected_anordnare, selected_year)
    poäng, kommuner, län, huvudmannatyp = get_anordnare(df, selected_anordnare, selected_year)
    beviljade, ej_beviljade = count_beslut(df, selected_anordnare, selected_year)
    utbildningsområden_text = ", ".join(utbildningsområden)
    beviljandegrad = round(beviljade / (beviljade + ej_beviljade) * 100, 1) if (beviljade + ej_beviljade) > 0 else 0.0

    fig_sökta = fig_top_10_sökta(df, selected_year)
    fig_beviljade = fig_top_10_beviljade(df, selected_year)

    return {
        "selected_anordnare": selected_anordnare,
        "selected_year": selected_year,
        "selected_year_str": selected_year_str,
        "selected_year_lov": selected_year_lov,
        "utbildningsområden": utbildningsområden,
        "utbildningsområden_text": utbildningsområden_text,
        "poäng": poäng,
        "kommuner": kommuner,
        "län": län,
        "huvudmannatyp": huvudmannatyp,
        "beviljade": beviljade,
        "ej_beviljade": ej_beviljade,
        "beviljandegrad": beviljandegrad,
        "fig_top_10_sökta": fig_sökta,
        "fig_top_10_beviljade": fig_beviljade,
    }

    
