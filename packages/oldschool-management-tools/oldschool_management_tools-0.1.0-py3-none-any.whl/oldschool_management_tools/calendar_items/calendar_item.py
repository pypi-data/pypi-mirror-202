from dataclasses import dataclass
from datetime import time
from termcolor import cprint


def nice_time_str(time_in_zone) -> str:
    return str(time_in_zone)[0:-3]


@dataclass
class CalendarItem:
    name: str
    location: str
    category: str
    start_time: time
    end_time: time

    def print(self):
        cprint(f"{nice_time_str(self.start_time)} to {nice_time_str(self.end_time)} - {self.name} - {self.location}", self.category)

    @classmethod
    def from_outlook_apt(cls, apt):
        start_time = time.fromisoformat(str(apt.StartInStartTimeZone.time()))
        end_time = time.fromisoformat(str(apt.EndInEndTimeZone.time()))

        location = apt.Location
        category = apt.Categories.split(' ')[0].lower()
        match category:
            case '':
                category = 'blue'
            case 'orange':
                category = 'yellow'
            case 'purple':
                category = 'magenta'
        return CalendarItem(apt.Subject, location, category, start_time, end_time)

