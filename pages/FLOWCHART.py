import streamlit as stream 


# PAGE CONFIGURATION
stream.set_page_config(page_title="FLOWCHART", page_icon=":eye", layout="wide")


def main():
      stream.header("FLOW OF EXECUTION OF THE APPLICATION")
      flow_execution_image = 'Images/FLOW-OF-EXECUTION.png'
      stream.image(flow_execution_image, width=850)



if __name__ == '__main__':
      main()