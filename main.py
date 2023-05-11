from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz
import random

# Side projects
side_projects = [
]

# Books to read
books = [
]

# Courses
courses = [
]

def create_event(summary, start_time, duration, freq, byday=None, interval=None, until=None):
  event = Event()
  event.add('summary', summary)
  event.add('dtstart', start_time)
  event.add('duration', duration)
  
  rrule_dict = {'FREQ': freq}
  if byday:
    rrule_dict['BYDAY'] = ','.join(byday)
  if interval:
    rrule_dict['INTERVAL'] = interval
  if until:
    rrule_dict['UNTIL'] = until
  
  event.add('rrule', rrule_dict)
  return event



def main():
  tz = pytz.timezone('America/New_York')

  cal = Calendar()
  cal.add('prodid', '-//GPT Schedule//')
  cal.add('version', '2.0')
  cal.add('X-WR-TIMEZONE', 'America/New_York')

  start_date = datetime(2023, 5, 8, tzinfo=tz)

  daily_tasks = [
    ('Wake up', timedelta(minutes=5), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Brush teeth', timedelta(minutes=5), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Shower', timedelta(minutes=10), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Meditate', timedelta(minutes=15), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Read the Bible', timedelta(minutes=15), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Morning Workout', timedelta(minutes=30), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Morning Journal', timedelta(minutes=15), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Review goals and tasks', timedelta(minutes=15), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Work', timedelta(hours=8), 'DAILY', 'MO,TU,WE,TH,FR'),
    (f'Work on {random.choice(side_projects)[0]}', timedelta(hours=2), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    (f'Read {random.choice(books)}', timedelta(hours=1), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Evening reflection', timedelta(minutes=15), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    (f'Take your {random.choice(courses)[0]}', timedelta(minutes=60), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']),
    ('Maintain a clean environment', timedelta(minutes=10), 'DAILY', ['MO', 'TU', 'WE', 'TH', 'FR', 'SA'])
  ]

  weekly_tasks = [
    ('Clean room and bathroom', timedelta(hours=1), 'WEEKLY', 'SA'),
    ('Work out with dad', timedelta(hours=1), 'WEEKLY', 'SA'),
    ('Reach out to mentors', timedelta(hours=1), 'WEEKLY', 'SA'),
    ('Church service', timedelta(hours=2), 'WEEKLY', 'SU'),
    ('Plan the upcoming week', timedelta(hours=1), 'WEEKLY', 'SU'),
    ('Review and update goals', timedelta(hours=1), 'WEEKLY', 'SU'),
    ('Connect with friends or family', timedelta(hours=2), 'WEEKLY', 'SU'),
    ('Invest in personal growth (read, listen to podcasts, etc.)', timedelta(hours=3), 'WEEKLY', ['SA','SU'])
  ]
    
  for task in daily_tasks:
    event = create_event(task[0], start_date + timedelta(hours=task[1].seconds // 3600, minutes=task[1].seconds // 60 % 60), task[1], task[2], task[3])
    cal.add_component(event)

  for task in weekly_tasks:
    start_day = start_date
    days_to_add = 0
    while start_day.strftime('%a') != task[3]:
      start_day += timedelta(days=1)
      days_to_add += 1
      if days_to_add > 6:
        break
    event = create_event(task[0], start_day + timedelta(hours=task[1].seconds // 3600, minutes=task[1].seconds // 60 % 60), task[1], task[2], task[3])
    cal.add_component(event)

  course_start_date = start_date
  for course in courses:
    event = create_event(course[0], course_start_date, timedelta(days=30), 'DAILY', until=course_start_date + timedelta(days=29))
    cal.add_component(event)
    course_start_date += timedelta(days=30)

  checkup_start_date = start_date + timedelta(days=30)
  for _ in range(len(courses)):
    event = create_event('Evaluate Side Projects Progress', checkup_start_date, timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    event = create_event('Evaluate Milestones', checkup_start_date + timedelta(hours=1), timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    checkup_start_date += timedelta(days=30)

  with open('personal_schedule.ics', 'wb') as f:
    f.write(cal.to_ical())

if __name__ == '__main__':
  main()

