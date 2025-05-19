import taipy.gui.builder as tgb
from taipy.gui import Gui
from frontend.pages.gender_age import gender_age

#pages = {"home": home_page, "dashboard": dashboard_page, "data": data_page}
pages = {"gender_age": gender_age}


if __name__ == "__main__":
    Gui(pages=pages).run(dark_mode=False, use_reloader=True, port=8080) #pages = pages 
#css_file="assets/main.css

