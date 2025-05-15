from taipy.gui import Gui
from Gender_graph import gender_graph

if __name__ == "__main__":
    pages = {
        "/": gender_graph()
    }

    gui = Gui(pages=pages)
    gui.run(title="Gender Graph", dark_mode=False, use_reloader=True, port=8080)

