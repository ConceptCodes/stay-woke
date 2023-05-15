from icalendar import Calendar, Event
from datetime import datetime, timedelta, time, date
import pytz
import yaml

config_path = 'config.yaml'

def readYamlFile():
  with open(config_path, 'r') as stream:
    try: return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)


def create_event(summary, start_time, duration, freq, by_day=None, interval=None, until=None):
  event = Event()
  event.add('summary', summary)
  event.add('dtstart', start_time)
  event.add('duration', duration)
  
  rrule_dict = {'FREQ': freq}
  if by_day: rrule_dict['BYDAY'] = by_day
  if interval: rrule_dict['INTERVAL'] = interval
  if until: rrule_dict['UNTIL'] = until
  event.add('rrule', rrule_dict)
  return event


def main():
  config = readYamlFile()

  books = config['books']
  side_projects = config['side_projects']
  courses = config['courses']

  book_rotation_duration = config['book_rotation_period']
  course_rotation_duration = config['course_rotation_period']
  side_project_rotation_duration = config['side_project_rotation_period']

  tz = pytz.timezone(config['time_zone'].replace(' ', '_'))

  cal = Calendar()
  cal.add('prodid', '-//Scheduled Discipline//')
  cal.add('version', '2.0')
  cal.add('X-WR-TIMEZONE', config['time_zone'])

  start_date = datetime.now(tz) + timedelta(days=1)
  # end_date = start_date + timedelta(days=config['schedule_duration'])

  schedule = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA']
  work_days = schedule[:4]
  weekend_days = schedule[4:]

  tasks = [
    ('Wake up', timedelta(minutes=5)),
    ('Brush teeth', timedelta(minutes=5)),
    ('Shower', timedelta(minutes=10)),
    ('Meditate', timedelta(minutes=10)),
    ('Read the Bible', timedelta(minutes=15)),
    ('Morning Workout', timedelta(minutes=25)),
    ('Morning Journal', timedelta(minutes=15)),
    ('Review goals and tasks', timedelta(minutes=15)),
    ('Work', timedelta(hours=8)),
    ('Break Fast', timedelta(minutes=30)),
    ('Read: {current_book}', timedelta(hours=1)),
    ('Course: {current_course}', timedelta(hours=1)),
    ('Evening Workout', timedelta(minutes=30)),
    ('Dinner', timedelta(minutes=30)),
    ('Side Project: {current_side_project}', timedelta(hours=2)),
    ('Relax and Unwind', timedelta(minutes=20)),
    ('Prepare for Tomorrow', timedelta(minutes=30)),
    ('Sleep', timedelta(hours=9)),
  ]

  start_of_day = time(hour=config['start_of_day'])

  daily_tasks = []
  current_time = start_of_day
  for task, duration in tasks:
    daily_tasks.append((task, current_time, duration, 'DAILY', work_days))
    current_time = (datetime.combine(date.today(), current_time) + duration).time()

  weekly_tasks = [
    ('Clean room and bathroom', timedelta(hours=1)),
    ('Work out with dad', timedelta(hours=1)),
    ('Reach out to mentors', timedelta(hours=1)),
    ('Church service', timedelta(hours=2)),
    ('Plan the upcoming week', timedelta(hours=1)),
    ('Review and update goals', timedelta(hours=1)),
    ('Connect with friends or family', timedelta(hours=2)),
    ('Invest in personal growth (read, listen to podcasts, etc.)', timedelta(hours=3)),
  ]

  scheduled_tasks = []
  current_time = start_of_day
  for task, duration in weekly_tasks:
    scheduled_tasks.append((task, current_time, duration, 'WEEKLY', weekend_days))
    current_time = (datetime.combine(date.today(), current_time) + duration).time()

  for week in range(52):    
    for day in range(7 * week, 7 * (week + 1)):
      for task in daily_tasks:
        task_start_time = start_date + timedelta(days=day, hours=task[1].second // 3600, minutes=task[1].second // 60 % 60)
        current_book = books[(day // book_rotation_duration) % len(books)]
        task_name = task[0].replace("{current_book}", current_book)
        current_side_project = side_projects[(day // side_project_rotation_duration) % len(side_projects)]
        task_name = task_name.replace("{current_side_project}", current_side_project)
        current_course = courses[(day // course_rotation_duration) % len(courses)]
        task_name = task_name.replace("{current_course}", current_course)
        event = create_event(task_name, task_start_time, task[2], task[3], task[4])
        cal.add_component(event)

  for task in scheduled_tasks:
    start_day = start_date
    days_to_add = 0
    while start_day.strftime('%a') != task[3]:
      start_day += timedelta(days=1)
      days_to_add += 1
      if days_to_add > 6:
        break
    event = create_event(task[0], start_day + timedelta(hours=task[1].second // 3600, minutes=task[1].second // 60 % 60), task[2], task[3], task[4])
    cal.add_component(event)

  checkup_start_date = start_date + timedelta(days=30)
  for _ in range(len(courses)):
    event = create_event('Evaluate Side Projects Progress', checkup_start_date, timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    event = create_event('Evaluate Funds', checkup_start_date + timedelta(hours=1), timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    event = create_event('Health Checkup (weight, exercise, nutrition)', checkup_start_date + timedelta(hours=2), timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    event = create_event('Personal Development Review (skills, hobbies, learning)', checkup_start_date + timedelta(hours=3), timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    event = create_event('Relationships Check-in (family, friends, partner)', checkup_start_date + timedelta(hours=4), timedelta(hours=1), 'MONTHLY')
    cal.add_component(event)
    checkup_start_date += timedelta(days=30)

  with open('personal_schedule.ics', 'wb') as f:
    f.write(cal.to_ical())

if __name__ == '__main__':
  main()

