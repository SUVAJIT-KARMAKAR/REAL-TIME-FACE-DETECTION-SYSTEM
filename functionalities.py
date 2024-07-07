# IMPORTING THE REQUIRED MODULES IN THE WORK SPACE
import os, pathlib
import streamlit as stream
import os, datetime, json, sys, pathlib, shutil
import pandas as panda
import streamlit as stream
import cv2 as cv
import face_recognition
import numpy as num
import time
from PIL import Image


# THE ROOT DIRECTORY OF THE PROJECT 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_CONFIG = os.path.join(ROOT_DIR, 'logging.yml')
STREAMLIT_STATIC_PATH = pathlib.Path(stream.__path__[0])

# WRITING THE OUTPUTS INTO THE DIRECTORY 
DOWNLOADS_PATH = (STREAMLIT_STATIC_PATH / "downloads")
if not DOWNLOADS_PATH.is_dir():
      DOWNLOADS_PATH.mkdir()


LOG_DIR = (STREAMLIT_STATIC_PATH / "logs")
if not LOG_DIR.is_dir():
      LOG_DIR.mkdir()


OUT_DIR = (STREAMLIT_STATIC_PATH / "output")
if not OUT_DIR.is_dir():
      OUT_DIR.mkdir()


VISITOR_DB = os.path.join(ROOT_DIR, "visitor_database")
if not os.path.exists(VISITOR_DB):
      os.mkdir(VISITOR_DB)


VISITOR_HISTORY = os.path.join(ROOT_DIR, "visitor_history")
if not os.path.exists(VISITOR_HISTORY):
      os.mkdir(VISITOR_HISTORY)



# DEFINING THE PARAMETERS 
COLOR_DARK = (0,0,153)
COLOR_WHITE = (255,255,255)
COLS_INFO = ['Name']
COLS_ENCODE = [f'v{i}' for i in range(128)]


# DEFINING THE DATABASE
data_path = VISITOR_DB
file_db = 'visitors_db.csv'
file_history = 'visitors_history.csv'

# IMAGE FORMATS
allowed_image_type = ['.png', '.jpg', '.jpeg']


# DEFINING THE FUNCTIONALITIES 
def initialize_data():
      if os.path.exists(os.path.join(data_path, file_db)):
            dataframe = panda.read_csv(os.path.join(data_path, file_db))
      else:
            dataframe = panda.DataFrame(columns=COLS_INFO + COLS_ENCODE)
            dataframe.to_csv(os.path.join(data_path, file_db), index=False)

      return dataframe


def add_data_db(dataframe_visitor_details):
      try:
            dataframe_all = panda.read_csv(os.path.join(data_path, file_db))

            if not dataframe_all.empty:
                  dataframe_all = panda.concat([dataframe_all, dataframe_visitor_details], ignore_index=False)
                  dataframe_all.drop_duplicates(keep='first', inplace=True)
                  dataframe_all.reset_index(inplace=True, drop=True)
                  dataframe_all.to_csv(os.path.join(data_path, file_db), index=False)
                  details_success_message = stream.success("DETAILS HAVE BEEN ADDED SUCCESSFULLY !")
                  time.sleep(2)
                  details_success_message.empty()
                  
            else:
                  dataframe_visitor_details.to_csv(os.path.join(data_path, file_db), index=False)
                  initiated_success_message = stream.success("INITIATED DATA SUCCESSFULLY !")
                  time.sleep(2)
                  initiated_success_message.empty()

      except Exception as e:
            stream.error(e)



# CONVERTING THE COLOR MODE OF THE IMAGE FROM BGR -> RGB MODE
def BGR_TO_RGB(image_in_array):
      return cv.cvtColor(image_in_array, cv.COLOR_BGR2RGB)


def findEncodings(images):
      encode_list = []

      for image in images:
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(image)[0]
            encode_list.append(encode)

      return encode_list


# CHECKING THE FACE DISTANCE FOR FACE DETECTION
def face_detection_to_conf(face_distance, face_match_threshold=0.6):
      if face_distance > face_match_threshold:
            range = (1.0 - face_match_threshold)
            linear_value = (1.0 - face_distance) / (range * 2.0)
            return linear_value

      else:
            range = face_match_threshold
            linear_value = 1.0 - (face_distance / (range *2.0))
            return linear_value + ((1.0 - linear_value) * num.power((linear_value - 0.5) * 2, 0.2))
      


# MARKING THE ATTENDANCE 
def attendance(id, name):
      student = os.path.join(VISITOR_HISTORY, file_history)
      now = datetime.datetime.now()
      dateString = now.strftime('%Y-%m-%d %H:%M:%S')
      dataframe_attendance_temp = panda.DataFrame(data= {
            "id" : [id],
            "visitor_name": [name],
            "Timings": [dateString]
      })

      if not os.path.isfile(student):
            dataframe_attendance_temp.to_csv(student, index=False)

      else:
            dataframe_attendance = panda.read_csv(student)
            dataframe_attendance = panda.concat([dataframe_attendance, dataframe_attendance_temp], ignore_index=True)
            dataframe_attendance.to_csv(student, index=True)


# VIEWING THE ATTENDANCE 
def view_attendance():
      stream.write("ATTENDANCE SHEET")
      student = os.path.join(VISITOR_HISTORY, file_history)
      dataframe_attendance_temp = panda.DataFrame(columns=["id", "visitor_name", "Timings"])

      if not os.path.isfile(student):
            dataframe_attendance_temp.to_csv(student, index=False)
      else:
            dataframe_attendance_temp = panda.read_csv(student)
            dataframe_attendance_temp = dataframe_attendance_temp.loc[:, ~dataframe_attendance_temp.columns.str.contains('^Unnamed')]
            

      dataframe_attendance = dataframe_attendance_temp.sort_values(by="Timings", ascending=False)
      dataframe_attendance.reset_index(inplace=True, drop=True)
      stream.write(dataframe_attendance)

      if dataframe_attendance.shape[0] > 0:
            id_chunk = dataframe_attendance.loc[0, 'id']
            id_name = dataframe_attendance.loc[0, 'visitor_name']

            selected_image = stream.selectbox("SEARCH IMAGE USING ID", options=['SELECT']+list(dataframe_attendance['id']))

            available_files = [file for file in list(os.listdir(VISITOR_HISTORY)) if ((file.endswith(tuple(allowed_image_type))) and (file.startswith(selected_image) == True))]


            if len(available_files) > 0:
                  selected_image_path = os.path.join(VISITOR_HISTORY, available_files[0])
                  stream.image(Image.open(selected_image_path))
            






