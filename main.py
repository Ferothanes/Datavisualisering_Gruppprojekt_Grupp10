import taipy.gui.builder as tgb
from taipy.gui import Gui
#from Gender_graph.gender_graph import gender_graph
from frontend.charts import gender_graph

# IF WE WANT PAGES
#pages = {"home": home_page, "dashboard": dashboard_page, "data": data_page}

gender_chart = gender_graph()  # Call the function and get the dict

with tgb.Page() as page:
    with tgb.part(class_name="container card stack-large"):
        tgb.text("# MYH dashboard 2023-2024", mode="md")
        with tgb.layout(columns="2 1"):
 
            # Display the gender chart using the content returned
            with tgb.part(class_name="card"):
                tgb.text(gender_chart["content"], mode="md")

if __name__ == "__main__":
    Gui(page).run(dark_mode=False, use_reloader=True, port=8080)
    
#css_file="assets/main.css

