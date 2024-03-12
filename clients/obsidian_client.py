# obsidian_client.py
import os
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

class ObsidianClient:
    """
    A class for interacting with Obsidian daily notes.
    """
    def __init__(self):
        self.obsidian_dir = os.getenv("OBSIDIAN_VAULT")
        self.template_path = os.path.join(self.obsidian_dir, "Templates", "Daily Planning Template.md")

    def get_note_path_by_datetime(self, date):
        return os.path.join(self.obsidian_dir, "Daily Notes", f"{date.strftime('%A, %B %d, %Y')}.md")

    def get_today_daily_note(self):
        """
        Gets or creates today's daily note based on the template.

        Returns:
            str: The content of today's daily note.
        """
        today = datetime.now().strftime("%A, %B %d, %Y")
        daily_note_path = os.path.join(self.obsidian_dir, "Daily Notes", f"{today}.md")

        if not os.path.exists(daily_note_path):
            with open(self.template_path, 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            with open(daily_note_path, 'w', encoding='utf-8') as daily_note_file:
                daily_note_file.write(template_content)
            print(f"Created today's daily note: {daily_note_path}")
        else:
            # print(f"Today's daily note already exists: {daily_note_path}")
            pass

        with open(daily_note_path, 'r', encoding='utf-8') as daily_note_file:
            daily_note_content = daily_note_file.read()

        return daily_note_content

    def get_tasks_from_daily_note(self):
            """
            Parses today's daily note to extract tasks (only the text between "**") and their completion status.

            Returns:
                list of tuples: A list where each tuple contains a task name (text between "**") and its status ('completed' or 'incomplete').
            """
            daily_note_content = self.get_today_daily_note()
            # Updated regex to include an optional time period before the task name
            task_pattern = re.compile(r'- \[(x| )\](?: (\d{2}:\d{2} - \d{2}:\d{2}))? \*\*(.+?)\*\*')
            tasks = []

            for line in daily_note_content.split('\n'):
                match = task_pattern.match(line.strip())
                if match:
                    status = 'completed' if match.group(1) == 'x' else 'incomplete'
                    task_name = match.group(3).strip()  # Group 3 is now the task name
                    tasks.append((task_name, status))

            return tasks
    
    def remove_task_from_daily_note(self, task):
        """
        Removes a task from today's daily note.

        Args:
            task (str): The task to remove.
        """
        today = datetime.now().strftime("%A, %B %d, %Y")
        daily_note_path = os.path.join(self.obsidian_dir, "Daily Notes", f"{today}.md")

        with open(daily_note_path, "r", encoding='utf-8') as file:
            daily_note_content = file.readlines()

        with open(daily_note_path, "w", encoding='utf-8') as file:
            for line in daily_note_content:
                if task not in line:
                    file.write(line)

    
    
if __name__ == "__main__":
    obsidian = ObsidianClient()