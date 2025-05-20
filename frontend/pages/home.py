import taipy.gui.builder as tgb


with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large"):
        tgb.navbar()

        with tgb.part(class_name="max-text-width"):
            tgb.text("# Skool´s YH dashboard", mode="md")
            tgb.text(
                """
            Här kommer du finna filtreringsbar information om beviljade kurser, program, utbildningsområden, statliga bidragsnivåer med mera. 
            """
            )

        with tgb.part(class_name="max-text-width"):
            tgb.text("# Skool´s YH dashboard", mode="md")
            tgb.text(
                """
            Dashboarden innehåller även information om ansökningsmönster och hur det går för YH studenterna efter avslutade studier.
            """
            )