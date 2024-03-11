# google_tasks_client.py
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz


class GoogleTasksClient:
    """
    A class for interacting with the Google Tasks API.
    """
    SCOPES = ["https://www.googleapis.com/auth/tasks"]

    def __init__(self):
        self.creds = self.__auth()
        self.service = build("tasks", "v1", credentials=self.creds)

    def __auth(self):
        """
        Private method to authenticate the Google API client.
        """
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
        """
        Lists the first 10 task lists.
        """
        try:
            results = self.service.tasklists().list().execute()
            items = results.get("items", [])

            if not items:
                print("No task lists found.")
            else:
                print("Task lists:")
                for item in items:
                    print(f"{item['title']}")
        except HttpError as err:
            print(err)

    def list_tasks(self, tasklist="@default", show_completed=False, show_hidden=False, max_results=100):
        """
        Lists tasks from the specified tasklist.

        Args:
            tasklist (str, optional): The tasklist to retrieve tasks from. Defaults to "@default".
            show_completed (bool, optional): Whether to include completed tasks. Defaults to False.
            show_hidden (bool, optional): Whether to include hidden tasks. Defaults to False.
            max_results (int, optional): Maximum number of tasks to retrieve. Defaults to 100.

        Returns:
            list: A list of task dictionaries.
        """
        try:
            results = self.service.tasks().list(
                tasklist=tasklist,
                showCompleted=show_completed,
                showHidden=show_hidden,
                maxResults=max_results
            ).execute()
            items = results.get("items", [])
            return items
        except HttpError as err:
            print(err)

    def get_current_tasks_as_markdown(self):
        """
        Returns a string containing current tasks in Markdown format.
        """
        now = datetime.now(pytz.utc)
        current_day = now.date()
        markdown_tasks = ""

        tasks = self.list_tasks()
        for task in tasks:
            if 'due' in task:
                due_datetime = datetime.strptime(task["due"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc)
                due_date = due_datetime.date()

                if due_date < current_day:
                    days_expired = (current_day - due_date).days - 1
                    if days_expired >= 14:
                        weeks_expired = days_expired // 7
                        status = f"{weeks_expired} weeks expired"
                    else:
                        status = f"{days_expired} days expired"

                    markdown_tasks += f"- [ ] **{task['title']}** ({status})\n"
                elif due_date == current_day:
                    markdown_tasks += f"- [ ] **{task['title']}** (Due today)\n"

        return markdown_tasks

    def find_and_complete_task(self, task_name, tasklist='@default'):
        """
        Finds a Google task by its name. If found, it marks the task as completed if it isn't already.
        If the task is not found, it creates a new task with a 24-hour due date.

        Args:
            task_name (str): The name of the task to find or create.
            tasklist (str, optional): The tasklist to search in or add to. Defaults to "@default".

        Returns:
            dict: The updated or newly created task dictionary.
        """
        tasks = self.list_tasks(tasklist)

        for task in tasks:
            if task['title'] == task_name:
                if task['status'] == 'completed':
                    print(f"Task '{task_name}' is already completed.")
                    return task
                else:
                    body = {
                        "id": task['id'],
                        "status": "completed",
                        "completed": datetime.utcnow().isoformat() + 'Z',
                    }

                    try:
                        updated_task = self.service.tasks().update(tasklist=tasklist, task=task['id'], body=body).execute()
                        print(f"Task '{task_name}' marked as completed.")
                        return updated_task
                    except Exception as e:
                        print(f"An error occurred: {e}")

    def add_task(self, task_name, tasklist='@default', due_date = datetime.utcnow() + timedelta(days=1)):
        """
        Creates a new Google Task with a 24-hour due date.

        Args:
            task_name (str): The name of the task to create.
            tasklist (str, optional): The tasklist to add the task to. Defaults to "@default".

        Returns:
            dict: The newly created task dictionary.
        """
    
        task_body = {
            'title': task_name,
            'due': due_date.isoformat() + 'Z',
        }

        try:
            new_task = self.service.tasks().insert(tasklist=tasklist, body=task_body).execute()
            # print(f"New task '{task_name}' created with a 24-hour due date.")
            return new_task
        except Exception as e:
            print(f"An error occurred while creating the task: {e}")
            return None



if __name__ == "__main__":
    client = GoogleTasksClient()
    