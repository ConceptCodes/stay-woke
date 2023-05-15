import unittest
from icalendar import Calendar, Event

class ScheduleTest(unittest.TestCase):
  def test_event_scheduling(self):
    # Load the generated calendar file
    with open('personal_schedule.ics', 'rb') as f:
      calendar_data = f.read()
    cal = Calendar.from_ical(calendar_data)

    # test weekly tasks

    # test daily tasks

    # test monthly tasks
    

if __name__ == '__main__':
  unittest.main()
