from datetime import datetime, timedelta, date, time
from win32com import client
from special_prompts.special_prompts import SPECIAL_PROMPTS
from os import system
from calendar_items.calendar_item import CalendarItem

outlook = client.Dispatch('Outlook.Application').GetNamespace('MAPI')
recipient = outlook.CreateRecipient("Da ROom")
resolved = recipient.Resolve()
calendar = outlook.getSharedDefaultFolder(recipient, 9)
print(calendar)