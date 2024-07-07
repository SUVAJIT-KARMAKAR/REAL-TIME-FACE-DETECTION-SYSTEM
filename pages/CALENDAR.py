import streamlit as stream
import calendar
import time

# PAGE CONFIGURATION
stream.set_page_config(page_title="CALENDAR", page_icon=":eye", layout="wide")

def get_reminders():
      if "reminders" not in stream.session_state:
            stream.session_state.reminders = []
      return stream.session_state.reminders

def main():
      stream.title("STUDENT CALENDAR")

      # Check session timeout
      check_session_timeout()

      # Get user input for year and month
      year = stream.number_input("ENTER YEAR:", min_value=2024, max_value=2100, step=1)
      month = stream.selectbox("SELECT MONTH:", list(calendar.month_name)[1:])

      # Get the calendar for the specified month and year
      cal = calendar.monthcalendar(year, list(calendar.month_name).index(month))

      # Display the weekdays
      weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

      # Create table data
      table_data = [weekdays] + cal

      # Display the calendar in tabular format
      stream.table(table_data)

      # Sidebar for adding reminder and refreshing
      stream.sidebar.header("ADD TASK TO DO")
      reminder_date = stream.sidebar.date_input("SELECT DATE TO ADD REMINDER:")
      reminder_text = stream.sidebar.text_input("ADD REMINDER:", key="reminder_text_input")
      add_reminder_button = stream.sidebar.button("ADD TO THE LIST")
      if add_reminder_button:
            if reminder_text:
                  stream.sidebar.write(f"REMINDER :  '{reminder_text}' ADDED FOR: {reminder_date}")
                  reminders = get_reminders()  # Ensure reminders are initialized
                  reminders.append({"date": reminder_date, "text": reminder_text})
                  stream.session_state.reminders = reminders

      # Display reminders
      display_reminders()

def display_reminders():
      reminders = get_reminders()
      if reminders:
            stream.header("REMINDERS")
            for i, reminder in enumerate(reminders):
                  stream.info(f"{i + 1}. {reminder['date']}: {reminder['text']}")
                  delete_button_key = f"delete_button_{i}"
                  if stream.button("DONE", key=delete_button_key):
                        delete_reminder(i)

def delete_reminder(index):
      reminders = get_reminders()
      reminders.pop(index)
      stream.session_state.reminders = reminders
      refresh_page()

def refresh_page():
      stream.experimental_rerun()

def check_session_timeout():
      if "last_activity_time" not in stream.session_state:
            stream.session_state.last_activity_time = time.time()
      elif time.time() - stream.session_state.last_activity_time > 300:  # 5 minutes
            stream.session_state.clear()

if __name__ == "__main__":
      main()
