# IMPORTING THE REQUIRED MODULES IN THE WORKSPACE
import uuid as uid
from streamlit_option_menu import option_menu

# IMPORTING THE functionalities.py 
from functionalities import * 
from records import *


#NAVIGATION LAYOUT
stream.set_page_config(page_title="RTFD", page_icon=":eye", layout="wide")


# DISABLING ALL THE WARNINGS 
stream.set_option('deprecation.showPyplotGlobalUse', False)
stream.set_option('deprecation.showfileUploaderEncoding', False)


user_color = '#ffffff'
title_webapp = "ATTENDANCE SYSTEM"

stream.header("REAL TIME FACE DETECTION APPLICATION")
html_temp = f"""
      <div style="background-color:{user_color}; padding:12px>
      <h1 style="color:white; text-align:center;">{title_webapp}
"""

stream.markdown(html_temp, unsafe_allow_html=True)


# DEFINING THE STATIC PATHS
if stream.sidebar.button("CLEAR DATABASE"):
      
      rtfd_warning_message = stream.sidebar.warning("ALL DATA WOULD BE DELETED")
      time.sleep(2)
      rtfd_warning_message.empty()

      shutil.rmtree(VISITOR_DB, ignore_errors=True)
      os.mkdir(VISITOR_DB)

      #CLEARING THE HISTORY
      shutil.rmtree(VISITOR_HISTORY, ignore_errors=True)
      os.mkdir(VISITOR_HISTORY)


if not os.path.exists(VISITOR_HISTORY):
      os.mkdir(VISITOR_HISTORY)


if not os.path.exists(VISITOR_DB):
      os.mkdir(VISITOR_DB)


#CREATING A BUTTON FOR DOWNLOAD THE CSV FILE 
csv_filename = 'visitor_history/visitors_history.csv'


if os.path.exists(csv_filename):
      dframe = panda.read_csv(csv_filename)
      dframe = dframe.loc[:, ~dframe.columns.str.contains('^Unnamed')]
      excel_file = 'attendancereport.xlsx'
      excel_generation = dframe.to_excel(excel_file, index=False)
else:
      excel_file = 'attendancereport.xlsx'



# CREATING DOWNLOAD BUTTON FOR DOWNLOADING THE EXCEL FILE <- CSV FILE 
with open(excel_file, 'rb') as output:
      excel_bytes = output.read()
      stream.sidebar.download_button (
            label='GENERATE EXCEL',
            data= excel_bytes,
            file_name=excel_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
      )


# MAIN FUNCTION DEFINITION 
def main():

      stream.sidebar.header("WHAT DOES THIS APPLICATION DO ?")

      stream.sidebar.info(" This WebApplication uses OpenCV in order to track the faces of the students for attendance, the face-recognition modules encodes all the faces that are trained to this model and matches with the one facing the camera in order to find similarities and face-distance, thus enabling a easeful way of marking attendance.")

      stream.sidebar.warning("The lower the face-distance, better the confidence value")

      stream.sidebar.success("The better is the confidence value, the better is the match")

      # DEFINING THE STATIC DATA 
      stream.sidebar.image('Images/SIDEBAR-LOGO.png')
      stream.sidebar.markdown("""
      MADE BY [*SUVAJITKARMAKAR*](https://github.com/SUVAJITKARMAKAR/opencv-realtime-face-detection-application)
      """)


      # MENU 
      selected_menu = option_menu(None, ['VALIDATION', 'HISTORY', 'DATABASE', 'RECORDS'], icons=['camera', 'clock-history', 'person-plus', 'book'], menu_icon="cast", default_index=0, orientation='horizontal')


      # FUNCTIONALITIES BASED ON USER SELECTION 
      # USER SELECTION AS VALIDATION
      if selected_menu == 'VALIDATION':
            #GENERATING A RANDOM ID USING UUID
            visitor_id = uid.uuid1()
            #READING CAMERA IMAGE
            image_file_buffer = stream.camera_input("TAKE A PICTURE")

            if image_file_buffer is not None:
                  bytes_data = image_file_buffer.getvalue()
                  image_array = cv.imdecode(num.frombuffer(bytes_data, num.uint8), cv.IMREAD_COLOR)
                  image_array_copy = cv.imdecode(num.frombuffer(bytes_data, num.uint8), cv.IMREAD_COLOR)

                  #SAVING STUDENT HISTORY
                  with open(os.path.join(VISITOR_HISTORY, f'{visitor_id}.jpg'), 'wb') as file:
                        file.write(image_file_buffer.getbuffer())
                        image_success_message = stream.success("IMAGE SAVED SUCCESSFULLY !")
                        time.sleep(2)
                        image_success_message.empty()

                        #VALIDATING IMAGE
                        maximum_faces = 0
                        rois = []

                        #GETTING THE LOCATIONS OF THE FACE FROM THE IMAGE
                        face_locations = face_recognition.face_locations(image_array)
                        #ENCODING THE IMAGE TO A NUMERIC FORMAT
                        encodesCursorFrame = face_recognition.face_encodings(image_array, face_locations)
                        
                        #GENERATING RECTANGLE BOX OVER THE IMAGE
                        for idx, (top, right, bottom, left) in enumerate(face_locations):
                              #SAVE FACE'S REGION OF INTEREST
                              rois.append(image_array[top:bottom, left:right].copy())

                              #DRAWING A BOX AROUND THE FACE AND LABEL IT
                              cv.rectangle(image_array, (left,top), (right,bottom), COLOR_DARK, 2)
                              cv.rectangle(image_array, (left,bottom + 35), (right,bottom), COLOR_DARK, cv.FILLED)
                              font = cv.FONT_HERSHEY_DUPLEX
                              cv.putText(image_array, f"#{idx}", (left + 5, bottom +25), font, 0.88, COLOR_WHITE, 1)

                        #SHOWING THE IMAGE 
                        stream.image(BGR_TO_RGB(image_array), width=720)

                        #FACES THAT ARE IDENTIFIED 
                        maximum_faces = len(face_locations)

                        if maximum_faces > 0:
                              col1, col2 = stream.columns(2)

                              #SELECT THE SELECTED FACES FROM THE PICTURE
                              face_idxs = col1.multiselect("SELECT FACE #", range(maximum_faces), default=range(maximum_faces))

                              #FILTERING FOR SIMILARLY BEYOND THRESHOLD
                              similarity_threshold = col2.slider("SELECT THRESHOLD FOR SIMILARITY", min_value=0.0, max_value=1.0, value=0.7)

                              flag_show = False

                              if (( col1.checkbox("CLICK TO PROCEED")) and (len(face_idxs) > 0 )):
                                    dataframe_new = panda.DataFrame()

                                    #INTERACTING FACES ONE BY ONE 
                                    for face_idx in face_idxs:
                                          roi = rois[face_idx]
                                          database_data = initialize_data()

                                          face_encodings = database_data[COLS_ENCODE].values
                                          dataframe = database_data[COLS_INFO]

                                          faces = face_recognition.face_encodings(roi)

                                          if len(faces) < 1:
                                                try_again_error_message =  stream.error(f"PLEASE TRY AGAIN FOR FACE #{face_idx}!")
                                                time.sleep(2)
                                                try_again_error_message.empty()

                                          else:
                                                face_to_compare = faces[0]

                                                dataframe['distance'] = face_recognition.face_distance(face_encodings, face_to_compare)
                                                
                                                dataframe['distance'] = dataframe['distance'].astype(float)

                                                dataframe['similarity'] = dataframe.distance.apply(lambda distance: f"{face_detection_to_conf(distance):0.2}")

                                                dataframe['similarity'] = dataframe['similarity'].astype(float)

                                                dataframe_new =  dataframe.drop_duplicates(keep='first')
                                                dataframe_new.reset_index(drop=True, inplace=True)
                                                dataframe_new.sort_values(by="similarity", ascending=True)

                                                dataframe_new = dataframe_new[dataframe_new['similarity'] > similarity_threshold].head(1)
                                                dataframe_new.reset_index(drop=True, inplace=True)

                                                if dataframe_new.shape[0] > 0:
                                                      (top,right,bottom,left) = (face_locations[face_idx])

                                                      #SAVING THE FACE REGION INTEREST INFORMATION LIST\
                                                      rois.append(image_array_copy[top:bottom, left:right].copy())

                                                      #DRAWING A RECTANGLE BOX AROUND THE FACE AND LABEL IT
                                                      cv.rectangle(image_array_copy, (left,top), (right,bottom), COLOR_DARK, 2)
                                                      cv.rectangle(image_array_copy, (left,bottom+35), (right,bottom), COLOR_DARK, cv.FILLED)
                                                      font = cv.FONT_HERSHEY_DUPLEX
                                                      cv.putText(image_array_copy, f"#{dataframe_new.loc[0,'Name']}", (left+5, bottom+25), font, 0.55, COLOR_WHITE,1)

                                                      student_visitor = dataframe_new.loc[0,'Name']
                                                      attendance(visitor_id, student_visitor)

                                                      flag_show = True

                                                else:
                                                      no_match_error_message = stream.error(f"NO MATCH FOUND FOR THE GIVEN SIMILARITY THRESHOLD FOR FACE #{face_idx}")
                                                      time.sleep(2)
                                                      no_match_error_message.empty()

                                                      update_notification_message = stream.info("PLEASE UPDATE THE DATABASE FOR NEW STUDENT AND CLICK AGAIN")
                                                      time.sleep(2)
                                                      update_notification_message.empty()
                                                      attendance(visitor_id, 'Unknown')

                                    if flag_show == True:
                                          stream.image(BGR_TO_RGB(image_array_copy), width=720)

                        else:
                              no_human_face_detected_error_message = stream.error("NO HUMAN FACE DETECTED")
                              time.sleep(2)
                              no_human_face_detected_error_message.empty()
            

      # USER SELECTION AS HISTORY
      if selected_menu == 'HISTORY':
            view_attendance()


      # USER SELECTION AS DATABASE
      if selected_menu == 'DATABASE':
            col1, col2, col3 = stream.columns(3)

            face_name = col1.text_input('NAME', '')
            picture_option = col2.radio("UPLOAD PICTURE", options = [
                  "UPLOAD A PICTURE",
                  "CLICK A PICTURE"
            ])
            
            if picture_option == "UPLOAD A PICTURE":
                  image_file_buffer = col3.file_uploader("UPLOAD A PICTURE", type=allowed_image_type)

                  if image_file_buffer is not None:
                        #TO READ THE IMAGE FILE FORM THE BUFFER WITH OPENCV
                        file_bytes = num.asarray(bytearray(image_file_buffer.read()), dtype=num.uint8)

            elif picture_option == "CLICK A PICTURE":
                  image_file_buffer = col3.camera_input("CLICK A PICTURE")

                  if image_file_buffer is not None:
                        #TO READ THE IMAGE FILE BUFFER WITH OPENCV
                        file_bytes = num.frombuffer(image_file_buffer.getvalue(), num.uint8)

            if (( image_file_buffer is not None) and (len( face_name ) > 1 ) and stream.button("CLICK TO SAVE")):
                  #CONVERT IMAGE FROM THE OPENED FILE TO num.array
                  image_array = cv.imdecode(file_bytes, cv.IMREAD_COLOR)


                  with open(os.path.join(VISITOR_DB, f'{face_name}.jpg'), 'wb') as file:
                        file.write(image_file_buffer.getbuffer())

                  face_locations = face_recognition.face_locations(image_array)
                  encodesCursorFrame = face_recognition.face_encodings(image_array, face_locations)

                  dataframe_new = panda.DataFrame(data=encodesCursorFrame, columns=COLS_ENCODE)

                  dataframe_new[COLS_INFO] = face_name

                  dataframe_new = dataframe_new[COLS_INFO + COLS_ENCODE].copy()

                  DB = initialize_data()
                  add_data_db(dataframe_new)


      if selected_menu == 'RECORDS':

            #CREATING A DIRECTORY FOR UPLOADED RECORD FILES 
            if not os.path.exists("records"):
                  os.mkdir("records")

            #CREATING A FILE UPLOADER
            uploaded_files = stream.file_uploader("UPLOAD THE STUDENT RECORDS FILE", type=["xlsx"], accept_multiple_files=True)

            #CHECK 
            if uploaded_files:
                  save_uploaded_files(uploaded_files)
                  
                  #DISPLAYING THE UPLOADED FILES 
                  success_message = stream.success("RECORDS UPLOADED SUCCESSFULLY")
                  time.sleep(3)
                  success_message.empty()
                  
            #SELECTING THE RECORD TO DISPLAY
            selected_file = stream.selectbox("SELECT A RECORD : ", os.listdir("records"))

            if selected_file:
                  stream.markdown("### TABLE : ")
                  display_excel_table(os.path.join("records", selected_file))

            #DELETE BUTTON TO DELETE THE FOLDER STRUCTURE
            if stream.button("DELETE ALL RECORDS"):
                  delete_uploaded_files()
                  deleted_warning__message = stream.warning("ALL UPLOADED FILES DELETED SUCCESSFULLY")
                  time.sleep(3)
                  deleted_warning__message.empty()



#INITIALIZATION POINT FOR THE APPLICATION
if __name__ == '__main__':
      main()