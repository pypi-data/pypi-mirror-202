from datetime import datetime, timedelta, date, time
from win32com import client
from oldschool_management_tools.special_prompts.special_prompts import SPECIAL_PROMPTS
from os import system
from oldschool_management_tools.calendar_items.calendar_item import CalendarItem

# Ideas:
#  - See allocated time per day
#  - Plan in breaks
#  - Draw schedule in hours

# Do the work where it is fast :)

CATEGORIES_REQUIRING_PREP = ["green category"]
system('color')


def get_calendar(begin, end) -> client.CDispatch:
    outlook = client.Dispatch('Outlook.Application').GetNamespace('MAPI')
    calendar = outlook.getDefaultFolder(9).Items
    calendar.IncludeRecurrences = True
    calendar.Sort('[Start]')

    restriction = "[Start] >= '" + begin.strftime('%d/%m/%Y') + "' AND [END] <= '" + end.strftime('%d/%m/%Y') + "'"
    calendar = calendar.Restrict(restriction)
    return calendar


def get_day_cal(date: datetime):
    return get_calendar(date, date + timedelta(days=1))


def print_cal(cal):
    for outlook_apt in cal:
        cal_apt = CalendarItem.from_outlook_apt(outlook_apt)
        cal_apt.print()


def start_of_day(day: date) -> datetime:
    return datetime.combine(day, time())


def parse_day(day) -> datetime:
    match day:
        case "today":
            return start_of_day(date.today())
        case "tomorrow":
            return start_of_day(date.today()) + timedelta(days=1)
        case d if day.isnumeric():
            return start_of_day(date.today()) + timedelta(days=int(d))
        case _:
            raise ValueError(f"Bad day [{day}]")


def show_day_sched(parsed_day=datetime.today()):
    cal = get_day_cal(parsed_day)
    print_cal(cal)


def prompt_day_tasks(parsed_day=datetime.today()):
    for spec_prompt in SPECIAL_PROMPTS:
        spec_prompt.show()
    cal = get_day_cal(parsed_day)
    for apt in cal:
        if apt.Categories.lower() in CATEGORIES_REQUIRING_PREP:
            input(f"Prep for {apt.Subject} => Done?")


