import streamlit as stream


# PAGE CONFIGURATION
stream.set_page_config(page_title="APPLICATION", page_icon=":eye", layout="wide")

def main():
      stream.header("ABOUT THE APPLICATION")
      stream.write("WORKFLOW")
      stream.info("The application utilizes a combination of powerful technologies to streamline the process of marking attendance for students. OpenCV serves as the backbone, providing robust computer vision capabilities for image processing tasks. Integrated with Streamlit, a user-friendly framework for building interactive web applications, the solution offers a seamless and intuitive interface for users to interact with. Leveraging the face-recognition machine model, the application harnesses the power of machine learning for face detection and facial feature extraction. This enables accurate identification of students within images or video streams. The face-recognition model further enhances the system by matching detected faces to a database of known students, enabling automatic attendance tracking.")

      stream.success("By combining these technologies, the application simplifies the traditionally cumbersome task of attendance management, reducing administrative overhead and ensuring accurate record-keeping. Students benefit from a streamlined process that saves time and eliminates manual errors, while educators gain valuable insights into attendance patterns and trends.")

      stream.warning("Overall, the innovative solution represents a cutting-edge approach to attendance management in educational settings, leveraging the latest advancements in computer vision and machine learning to optimize efficiency and accuracy.")

if __name__ == '__main__':
      main()