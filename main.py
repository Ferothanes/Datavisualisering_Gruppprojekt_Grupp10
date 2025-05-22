import taipy.gui.builder as tgb
from taipy.gui import Gui
from frontend.pages.utbildningsomrade import utbildningsomrade
from frontend.pages.statistikansökningar import ansökningar
from frontend.pages.Overview import gender_age
from frontend.pages.home import home_page
from frontend.pages.anordnare import anordnare

#pages = {"home": home_page, "dashboard": dashboard_page, "data": data_page}
pages = {"Home": home_page, "Anordnare":anordnare, "Kursansokningar": ansökningar, "Utbildningsomraden": utbildningsomrade, "Demografi": gender_age}


if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/main.css").run(dark_mode=False, use_reloader=True, port=8080) 



