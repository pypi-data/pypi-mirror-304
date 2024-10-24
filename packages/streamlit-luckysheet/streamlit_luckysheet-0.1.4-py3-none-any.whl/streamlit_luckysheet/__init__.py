import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_luckysheet",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_luckysheet", path=build_dir)


def streamlit_luckysheet(name="",height=0, file=None, file_type=None, showtoolbarConfig={
        "save": True,
        "download": True,
        "undoRedo": True,
        "paintFormat": True,
        "currencyFormat": False,
        "percentageFormat": False,
        "numberDecrease": False,
        "numberIncrease": False,
        "moreFormats": False,
        "font": True,
        "fontSize": True,
        "bold": True,
        "italic": True,
        "strikethrough": True,
        "underline": True,
        "textColor": True,
        "fillColor": True,
        "border": True,
        "mergeCell": True,
        "horizontalAlignMode": True,
        "verticalAlignMode": True,
        "textWrapMode": True,
        "textRotateMode": True,
        "image": False,
        "link": False,
        "chart": False,
        "postil": False,
        "pivotTable": False,
        "function": False,
        "frozenMode": False,
        "sortAndFilter": False,
        "conditionalFormat": False,
        "dataVerification": False,
        "splitColumn": False,
        "screenshot": False,
        "findAndReplace": False,
        "protection": False,
        "print": False,
        "exportXlsx": False,
      }, key="", default=0):
    component_value = _component_func(name=name,height=height, file=file, file_type=file_type, showtoolbarConfig=showtoolbarConfig, key=key, default=default)
    return component_value



# import streamlit as st
# from streamlit_luckysheet import streamlit_luckysheet
# import base64
# import os
# import json
# import time
# from datetime import datetime

# st.set_page_config(layout="wide")
# st.subheader("Component with constant args")

# name = "Streamlit_Excelsheet"
# key = "Streamlit_Excelsheet"
# height = 1000
# file_name = "Config_Test_Output"
# file_path = r".\\excel\\Employee Sample Data_Rev2.xlsx"
# file_path_dir = ".\\excel\\"
# save_path = file_path_dir + file_name
# file_type = None

# file_path = r".\excel\SampleDocs-SampleXLSFile_6800kb.xlsx" 
# save_path = r'.\{excel}\.' + file_name

# template_working
# Unuse empty row will affect the performance.    | Result
# Speed 400kRow9Column.xlsx 25,430 KB             | Time out
# Speed 400kRow9Column_Reduce.xlsx 20,129 KB      | Time out @ 2 minutes
# Speed 200kRow9Column.xlsx 15,680 kB             | 1min 04:68
# Speed 100kRow9Column.xlsx 10,806 kB time            | 31.72 second
# Speed 50kRow9Column.xlsx 3,192 kB               | 16.33 second

# Luckyexcel Simulation
# Unuse empty row will affect the performance.    | Result
# Speed 400kRow9Column.xlsx 25,430 KB             | Time out
# Speed 400kRow9Column_Reduce.xlsx 20,129 KB      | Time out @ 1:53.94
# Speed 200kRow9Column.xlsx 15,680 kB             | 1min 03.30
# Speed 100kRow9Column.xlsx 10,806 kB             | 30.67
# Speed 50kRow9Column.xlsx 3,192 kB               | 16.12 



# Converting File Into Base64 
# def excel_to_file(path):
#     try:
#         if not os.path.exists(path):
#             return ""
#         with open(path, 'rb') as file:
#             file_data = file.read() 
#             if file_data:
#                 return base64.b64encode(file_data).decode('utf-8')
#             else:
#                 st.warning("File is empty or could not be read.")
#                 return ""
#     except Exception as e:
#         st.warning(f"An error occurred while processing the file: {e}")
#         return ""

# # Non-Conversion Forwarding File directly into Luckysheet
# def read_file(path):
#     try:
#         if not os.path.exists(path):
#             return ""
        
#         # Check if the file is a JSON file based on its extension
#         if path.endswith(".json"):
#             with open(path, 'r') as file:  # Open in text mode
#                 try:
#                     # Parse the JSON file and return as a Python object
#                     return json.load(file)
#                 except json.JSONDecodeError:
#                     st.warning("Invalid JSON file.")
#                     return None
#         else:
#             # For binary or non-JSON files, read in binary mode
#             with open(path, 'rb') as file:
#                 file_data = file.read()
#                 if file_data:
#                     return file_data
#                 else:
#                     st.warning("File is empty or could not be read.")
#                     return None
#     except Exception as e:
#         st.error(f"An error occurred while reading the file: {e}")
#         return None
            
#     except Exception as e:
#         st.warning(f"An error occurred while processing the file: {e}")
#         return ""

# # Converting Base64 Into File.
# def base64_to_file(base64_string, save_path):
#     try:
#         output_dir = os.path.dirname(save_path)
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#         file_data = base64.b64decode(base64_string)
#         with open(save_path, 'wb') as file:
#             file.write(file_data)
#         now = datetime.now()
#         dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
#         st.toast(f"[{dt_string}] File successfully created at: {save_path}")
#     except Exception as e:
#         st.warning(f"An error occurred while converting to Excel file: {e}")

# # Get all files in the directory with latest modification timestamp.
# def get_latest_file(directory):
#     files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
#     if not files:
#         return None  
#     search_result = max(files, key=os.path.getmtime)
#     file_path, file_type = os.path.splitext(search_result)
#     return file_path, file_type


# with st.spinner():
#     # Selected the Latest File
#     try:
#         file_path, file_type = get_latest_file(file_path_dir)
#         file = read_file(file_path + file_type)
#     except:
#         pass

#     # Debugging & Testing Purpose
#     st.warning(file_path) 
#     st.warning(file_type)
#     # file = read_file(file_path)
#     time.sleep(1)
   

# showtoolbarConfig = {
#         "save": True,
#         "download": False,
#         "undoRedo": True,
#         "paintFormat": True,
#         "currencyFormat": False,
#         "percentageFormat": False,
#         "numberDecrease": False,
#         "numberIncrease": False,
#         "moreFormats": False,
#         "font": True,
#         "fontSize": True,
#         "bold": True,
#         "italic": True,
#         "strikethrough": True,
#         "underline": True,
#         "textColor": True,
#         "fillColor": True,
#         "border": True,
#         "mergeCell": True,
#         "horizontalAlignMode": True,
#         "verticalAlignMode": True,
#         "textWrapMode": True,
#         "textRotateMode": True,
#         "image": False,
#         "link": False,
#         "chart": False,
#         "postil": False,
#         "pivotTable": False,
#         "function": False,
#         "frozenMode": False,
#         "sortAndFilter": False,
#         "conditionalFormat": False,
#         "dataVerification": False,
#         "splitColumn": False,
#         "screenshot": False,
#         "findAndReplace": False,
#         "protection": False,
#         "print": False,
#         "exportXlsx": False,
#       }
    

# return_result = streamlit_luckysheet(name=name, height=height, file=file, file_type=file_type, showtoolbarConfig=showtoolbarConfig, key=key, default=[])
# if isinstance(return_result, dict):
#     if "output_xlsx" in return_result:
#         base64_to_file(return_result["output_xlsx"], save_path + ".xlsx")  
#     if "output_json" in return_result:
#         base64_to_file(return_result["output_json"], save_path + ".json")


