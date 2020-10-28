import sys
from slack_app.gui_tools import *
from slack_app.validations import *


# ------------------------------------------------------------------------------
# UI. Request User Input
# ------------------------------------------------------------------------------
button, channel, message, u_time, days = include_greetings()


# ------------------------------------------------------------------------------
# Validations
# ------------------------------------------------------------------------------
# Validate if process should continue
if button == 'cancel':
    sys.exit()

# Validate time format
while (not validate_time(u_time)) & (button != 'cancel'):
    info_message("Not a valid Time format \n\nTry Again, example 09:00")
    button, channel, message, u_time, days = include_greetings()

if button == 'cancel':
    sys.exit()

# Validate Channel format
while (not validate_channel(channel)) & (button != 'cancel'):
    info_message("Not valid Channel (Must include '#' or '@')\n\nTry Again")
    button, channel, message, u_time, days = include_greetings()

if button == 'cancel':
    sys.exit()

# Validate Days selection
while (not validate_days(days)) & (button != 'cancel'):
    info_message("You must select at least one day \n\nTry Again")
    button, channel, message, u_time, days = include_greetings()

if button == 'cancel':
    sys.exit()


# ------------------------------------------------------------------------------
# Schedule Job
# ------------------------------------------------------------------------------
days = [d.lower() for d in days]

#TODO: Make it more pythonic
if 'monday' in days:
    schedule.every().monday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'tuesday' in days:
    schedule.every().tuesday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'wednesday' in days:
    schedule.every().wednesday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'thursday' in days:
    schedule.every().thursday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'friday' in days:
    schedule.every().friday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'saturday' in days:
    schedule.every().saturday.at(u_time).\
        do(job, u_channel=channel, u_message=message)

if 'sunday' in days:
    schedule.every().sunday.at(u_time).\
        do(job, u_channel=channel, u_message=message)


winroot = tk.Tk()
client = ThreadedJob(winroot)
winroot.geometry("300x200")
winroot.attributes("-topmost", True)
winroot.title("Greetings App")
tk.Label(winroot, text="Running").pack()
winroot.mainloop()









