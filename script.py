import requests
import shelve

from pytodoist import todoist
from credentials import USER, PASS
import datetime

def zapier_to_skedpal(project_name="Inbox", Title="Placeholder-title", Notes=None, Plan_key=None, Priority=None, Duration=None, URL=None):
    """
    Priority:
        0, High
        1, Normal
        2, Low

    Plan_key:
        0, Later Today
        1, Tomorrow
        2, This Week
        4, Next Week
    """

    url = 'https://hooks.zapier.com/hooks/catch/944081/v8f300/'

    project_name_id = {
        'Inbox': "cc4469a4-0667-42d8-9181-f6038837dfda"
    }

    if project_name in project_name_id:
        project_id = project_name_id.get("Inbox")

    payload = {'project_id': project_id,
               'Title': Title,
               'Notes': Notes,
               'Plan for': Plan_key,
               'Priority': Priority,
               'Duration': Duration,
               'URL': URL
               }

    print("Sending to SkedPal")
    print(payload)

    requests.post(url, json=payload)

### Start script here ###
user = todoist.login(USER, PASS)
print("Finished setting up todoist login")

inbox_tasks = user.get_project("Inbox").get_tasks()

d = shelve.open("task_log.txt") #Define shelf for already sent tasks

for task in inbox_tasks:
    if task.due_date_utc is not None:
        if task.due_date_utc[0:6] == datetime.date.today().strftime("%a %d"):
            if task.content in d and d.get(task.content) == task.due_date_utc:
                #Check if task is added, and has today as due date
                print("Task already added, continuing")
                continue
            else:
                zapier_to_skedpal(project_name="Inbox",
                                  Title=task.content,
                                  Plan_key="0",
                                  Priority="0",
                                  Duration="30m")

                d[task.content] = task.due_date_utc
