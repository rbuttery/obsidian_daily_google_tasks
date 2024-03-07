from google_tasks_client import GoogleTasksClient
from obsidian_client import ObsidianClient
from datetime import datetime, timedelta

def update_obsidian_daily_note_with_current_google_tasks():
    gtask = GoogleTasksClient()
    obsidian = ObsidianClient()

    markdown_tasks = gtask.get_current_tasks_as_markdown().split('\n')

    # Get the path to today's daily note
    daily_note_path = obsidian.get_note_path(date=datetime.now())

    # Read the current content of the daily note
    with open(daily_note_path, "r", encoding='utf-8') as file:
        daily_note_content = file.readlines()

    if "# Tasks\n" in daily_note_content:
        # Find the position to insert new tasks
        tasks_index = daily_note_content.index("# Tasks\n") + 1

        # Check each task for uniqueness and add it if it's not already in the note
        for task in markdown_tasks:
            if task and task + '\n' not in daily_note_content[tasks_index:]:
                daily_note_content.insert(tasks_index, task + '\n')
                tasks_index += 1

        # Write the updated content back to the daily note
        with open(daily_note_path, "w", encoding='utf-8') as file:
            file.writelines(daily_note_content)

def find_completed_obsidian_tasks(daily_note_path):
    """
    Parses the Obsidian daily note to find completed tasks.

    Args:
        daily_note_path (str): Path to the daily note file.

    Returns:
        list of str: A list of completed task names.
    """
    completed_tasks = []
    with open(daily_note_path, "r", encoding='utf-8') as file:
        for line in file:
            # Check if the line contains a completed task (markdown checkbox checked)
            if line.strip().startswith("- [x] "):
                # Extract the task name, removing the markdown checkbox and any trailing relative date
                task_name = line.strip()[6:].split("(")[0].strip()
                completed_tasks.append(task_name)
    return completed_tasks

def update_google_task(task_name, gtask):
    """
    Updates the status of a task in Google Tasks to completed based on the task name.

    Args:
        task_name (str): Name of the task to be updated.
        gtask (GoogleTasksClient): An instance of GoogleTasksClient.
    """
    updated_task = gtask.find_and_complete_task(task_name)

def find_obsidian_completed_yesterday_tasks_and_update_google_tasks_to_completed_status(date=datetime.now()):
    gtask = GoogleTasksClient()
    obsidian = ObsidianClient()

    # Get the path to today's daily note
    daily_note_path = obsidian.get_note_path(date)


    # Find completed tasks in the Obsidian daily note
    completed_tasks = find_completed_obsidian_tasks(daily_note_path)
    

    # Update the status of completed tasks in Google Tasks
    for task_name in completed_tasks:
        update_google_task(task_name, gtask)
        
        
def prepare_for_day():
    find_obsidian_completed_yesterday_tasks_and_update_google_tasks_to_completed_status()
    update_obsidian_daily_note_with_current_google_tasks()
    
    
if __name__ == "__main__":
    prepare_for_day()
