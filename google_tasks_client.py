import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# for finding today's task
from datetime import datetime, timedelta
import pytz

# for exporting
import json

class GoogleTasksClient:
    SCOPES = ["https://www.googleapis.com/auth/tasks"]

    def __init__(self):
        self.creds = self.__auth()
        self.service = build("tasks", "v1", credentials=self.creds)

    def __auth(self):
        """Private method to authenticate the Google API client."""
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                creds = flow.run_local_server(port=50567)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def list_task_lists(self):
        """Lists the first 10 task lists."""
        try:
            results = self.service.tasklists().list().execute()
            items = results.get("items", [])
            
            if not items:
                print("No task lists found.")
                return

            print("Task lists:")
            for item in items:
                print(f"{item['title']}")
        except HttpError as err:
            print(err)

    def list_tasks(self, tasklist="@default", showCompleted=False, showHidden=False, maxResults=100):
        """
        showCompleted=False & showHidden=False = current tasks
        showCompleted=True & showHidden=True = completed tasks 
        """
        try:
            results = self.service.tasks().list(tasklist=tasklist, showCompleted=showCompleted, showHidden=showHidden, maxResults=maxResults).execute()
            items = results.get("items", [])
            if not items:
                print("No tasks found.")
                return
            
            return items
        except HttpError as err:
            print(err)

    def get_current_tasks_as_markdown(self):
        # Get the current date and time in UTC to match the task 'due' format
        now = datetime.now(pytz.utc)
        current_day = now.date()
        
        # Initialize an empty string to store the formatted markdown tasks
        markdown_tasks = ""

        tasks = self.list_tasks()
        for task in tasks:
            # Check if the 'due' key exists in the task dictionary
            if 'due' in task:
                # Parse the 'due' datetime in UTC
                due_datetime = datetime.strptime(task["due"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
                due_date = due_datetime.date()

                # Determine if the task is expired and calculate the number of days expired
                if due_date < current_day:
                    days_expired = (current_day - due_date).days - 1
                    if days_expired >= 14:
                        weeks_expired = days_expired // 7
                        status = f"{weeks_expired} weeks expired"
                    else:
                        status = f"{days_expired} days expired"

                    # Format the task in markdown and append it to the result string
                    markdown_tasks += f"- [ ] {task['title']} ({status})\n"
                elif due_date == current_day:
                    # Format tasks due today
                    markdown_tasks += f"- [ ] {task['title']} (Due today)\n"
            else:
                # Handle tasks without a 'due' field, if necessary
                pass

        return markdown_tasks
    
    def find_and_complete_task(self, task_name, tasklist='@default'):
        """Finds a Google task by its name and marks it as completed."""
        tasks = self.list_tasks(tasklist)

        for task in tasks:
            if task['title'] == task_name and task['status'] != 'completed':
                # Prepare the body to mark the task as completed
                body = {
                    "tasklist": tasklist,
                    "id": task['id'],
                    "status": "completed",
                    "completed": datetime.utcnow().isoformat() + 'Z',  # Marking the task completion time as now
                }

                print(task)

                # Update the task status to completed
                try:
                    # Make sure to use the correct identifiers for tasklist and task
                    updated_task = self.service.tasks().update(task=task['id'], tasklist=tasklist, body=body).execute()
                    print(f"Task '{task_name}' marked as completed.")
                except Exception as e:
                    print(f"An error occurred: {e}")

                return updated_task


    
    
    
if __name__ == "__main__":
    client = GoogleTasksClient()

    current_tasks = client.list_tasks()

    with open("task_data/current_tasks.json", "w") as current_tasks_export:
        json.dump(current_tasks, current_tasks_export, indent=4)
    
    markdown_tasks = client.get_current_tasks_as_markdown()
    print(markdown_tasks)
    
    # client.find_and_complete_task(task_name="Nova breakfast")

        

    