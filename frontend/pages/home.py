import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container card stack-large home-page"):
        tgb.navbar()
        tgb.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM200Z3Nya3QwZ2p2Nnk0NmVhb2ZuMWxmejdnY3V0dmt3aGRzejUwcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/Vf3ZKdillTMOOaOho0/giphy.gif", width="200px") 

        with tgb.part(class_name="max-text-width"):

            tgb.text("# Skool´s YH dashboard", mode="md")
            tgb.text(
"""
Här kommer du finna filtreringsbar information om beviljade kurser, program, utbildningsområden, statliga bidragsnivåer med mera.

---

## Välkommen till YH-kollen

Ett datadrivet beslutsstöd utvecklat för utbildningsanordnaren **The Skool**.  
Detta interaktiva verktyg ger en tydlig överblick över yrkeshögskoleutbildningar i Sverige, baserat på data från bland annat Myndigheten för Yrkeshögskolan (MYH) och SCB.

**Syftet med projektet är att:**

- Hjälpa utbildningsledare och skolpersonal att fatta informerade beslut.  
- Visualisera trender och ansökningsdata för både program och kurser.  
- Möjliggöra filtrering på utbildningsanordnare, geografiska områden och utbildningstyper.  
- Ge en helhetsbild av hur utbildningar är förankrade i arbetslivet och hur statsbidrag fördelas.
""",
mode="md"
            )
