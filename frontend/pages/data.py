import taipy.gui.builder as tgb        
from backend.data_processing import df


# with tgb.Page() as data_page:
#     with tgb.part(class_name="container card stack-large"):
#         tgb.navbar()
#         tgb.text("# Raw data", mode="md")
#         with tgb.part(class_name="card"):
#             tgb.table("{df}")