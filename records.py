import streamlit as stream
import pandas as panda
import shutil
import time
import os



#FUNCTION DEFINITION 
def save_uploaded_files(uploaded_files):
      for uploaded_file in uploaded_files:
            with open(os.path.join("records", uploaded_file.name), "wb") as save:
                  save.write(uploaded_file.getbuffer())

def display_excel_table(file_path):
      dframe = panda.read_excel(file_path)
      stream.write(dframe)


def delete_uploaded_files():
      folder = "records"
      for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)

            try:
                  if os.path.isfile(file_path):
                        os.unlink(file_path)
            except Exception as e:
                  stream.error(f"ERROR DELETING {file_path}: {e}")


