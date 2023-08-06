from datetime import datetime, timedelta, date, time

import win32com.client
from win32com import client
from oldschool_management_tools.special_prompts.special_prompts import SPECIAL_PROMPTS
from os import system
from oldschool_management_tools.calendar_items.calendar_item import CalendarItem
from dataclasses import dataclass

# Ideas:
#  - See allocated time per day
#  - Plan in breaks
#  - Draw schedule in hours

# Do the work where it is fast :)

CATEGORIES_REQUIRING_PREP = ["green"]
PREP_DURATION = 15
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
    apts = [CalendarItem.from_outlook_apt(apt) for apt in cal]
    for apt in apts:
        if apt.category.lower() in CATEGORIES_REQUIRING_PREP:
            input(f"Prep for {apt.name} => Done?")


@dataclass
class TimeSlot:
    start_datetime: datetime
    end_datetime: datetime


def fill_prep(parsed_day=datetime.today()):
    cal = get_day_cal(parsed_day)
    apts = [CalendarItem.from_outlook_apt(apt) for apt in cal]
    free_slots: list[TimeSlot] = []
    last_apt_end_time: datetime = None
    new_apts = []

    for apt in apts:
        if not free_slots:
            free_slots.append(TimeSlot(apt.start_datetime.replace(hour=8, minute=0, second=0), apt.start_datetime))
        elif last_apt_end_time and free_slots[-1].end_datetime < apt.start_datetime \
                and last_apt_end_time < apt.start_datetime:
            new_free_slot = TimeSlot(last_apt_end_time, apt.start_datetime)
            free_slots.append(new_free_slot)

        if apt.category.lower() in CATEGORIES_REQUIRING_PREP:
            last_free_slot = free_slots[-1]
            if last_free_slot.end_datetime < apt.end_datetime:
                prep_slot = TimeSlot(last_free_slot.end_datetime - timedelta(minutes=PREP_DURATION), last_free_slot.end_datetime)
                last_free_slot.end_datetime = last_free_slot.end_datetime - timedelta(minutes=PREP_DURATION)
                if last_free_slot.end_datetime - timedelta(minutes=PREP_DURATION) <= last_free_slot.start_datetime:
                    free_slots.pop()
            new_apts.append(CalendarItem(f"Prep {apt.name}", "Desk", "yellow",
                                         prep_slot.start_datetime, prep_slot.start_datetime.time(),
                                         prep_slot.end_datetime, prep_slot.end_datetime.time()))
        last_apt_end_time = apt.end_datetime

    [add_apt(cal, apt) for apt in new_apts]


def add_apt(cal: win32com.client.CDispatch, apt: CalendarItem):
    outlook = client.Dispatch('Outlook.Application')
    apt.print()
    appt = outlook.CreateItem(1)
    appt.Start = str(apt.start_datetime)[0:-6]
    appt.Subject = apt.name
    appt.Categories = apt.category + " Category"
    appt.Duration = PREP_DURATION
    appt.Location = apt.location
    appt.Save()
