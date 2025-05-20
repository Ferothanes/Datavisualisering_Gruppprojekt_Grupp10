import taipy.gui.builder as tgb
from taipy.gui import Gui
from frontend.pages.Overview import gender_age
from frontend.pages.utbildningsomrade import utbildningsomrade

#pages = {"home": home_page, "dashboard": dashboard_page, "data": data_page}
pages = {"Overview": gender_age, "Utbildningsområde": utbildningsomrade}


if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/main.css").run(dark_mode=False, use_reloader=True, port=8080) #pages = pages 


