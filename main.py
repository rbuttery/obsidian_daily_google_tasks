# main.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from clients.google_tasks_client import GoogleTasksClient
from clients.obsidian_client import ObsidianClient

import time
from datetime import datetime

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




class DailyNoteHandler(FileSystemEventHandler):
    def __init__(self, on_created_callbacks=None, on_modified_callbacks=None, on_deleted_callbacks=None) -> None:
        super().__init__()
        self.obsidian_client = ObsidianClient()
        self.google_tasks_client = GoogleTasksClient()
        self.obsidian_dir = self.__get_obsidian_dir()
        self.run_interval = 1  # Interval in seconds to run the script
        self.debounce_delay = 0.5  # Delay in seconds
        self.last_modified = None

        # Callbacks should be lists of functions
        self.on_created_callbacks = on_created_callbacks if on_created_callbacks else []
        self.on_modified_callbacks = on_modified_callbacks if on_modified_callbacks else []
        self.on_deleted_callbacks = on_deleted_callbacks if on_deleted_callbacks else []

    def __get_obsidian_dir(self):
        return self.obsidian_client.obsidian_dir
    
    def _execute_callbacks(self, callbacks, event):
        for callback in callbacks:
            callback(event)

    def on_created(self, event):
        if not event.is_directory and self._is_target_file(event.src_path):
            self._execute_callbacks(self.on_created_callbacks, event)

    def on_modified(self, event):
        if not event.is_directory and self._is_target_file(event.src_path):
            current_time = time.time()
            if not self.last_modified or (current_time - self.last_modified > self.debounce_delay):
                self._execute_callbacks(self.on_modified_callbacks, event)
                self.last_modified = current_time

    def on_deleted(self, event):
        if not event.is_directory and self._is_target_file(event.src_path):
            self._execute_callbacks(self.on_deleted_callbacks, event)

    def _is_target_file(self, path):
        if self.file_extension:
            return path.endswith(self.file_extension)
        return True

    def start_observing(self, path=None, file_extension=None):
        self.file_extension = file_extension
        observing_path = f"{self.obsidian_dir}\\{path}" if path else self.obsidian_dir
        observer = Observer()
        observer.schedule(self, observing_path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(self.run_interval)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()




if __name__ == "__main__":
    
    print("Daily Note Handler is running...")
    
    obsidian_client = ObsidianClient()
    google_tasks_client = GoogleTasksClient()
    day=datetime.now() 
    tag=os.getenv("DAILY_NOTE_TAG")  # Get tag from environment variable
    daily_notes_path=os.getenv("DAILY_NOTES_PATH")  # Get daily notes path from environment variable
    
    def on_create(event):
        print(f"File created: {event.src_path}")
        
        # fill today's new daily note with current google tasks
        gtask= GoogleTasksClient()
        obsidian = ObsidianClient()

        markdown_tasks = gtask.get_current_tasks_as_markdown().split('\n')
        daily_note_path = obsidian.get_note_path_by_datetime(date=day, path=daily_notes_path)

        with open(daily_note_path, "r", encoding='utf-8') as file:
            daily_note_content = file.readlines()

        if f"{tag}\n" in daily_note_content:
            tasks_index = daily_note_content.index(f"{tag}\n") + 1

            for task in markdown_tasks:
                if task and task + '\n' not in daily_note_content[tasks_index:]:
                    daily_note_content.insert(tasks_index, task + '\n')
                    tasks_index += 1

            with open(daily_note_path, "w", encoding='utf-8') as file:
                file.writelines(daily_note_content)
    
    def on_modifiy(event):
        # print(f"File modified at time : {datetime.now()}")
        
        # update google tasks from obsidian
        obsidian_tasks = obsidian_client.get_tasks_from_daily_note()
        google_tasks = google_tasks_client.list_tasks()
        
        if len(obsidian_tasks) > 0:
            for obsidian_task in obsidian_tasks:
                if obsidian_task[1] == 'completed':
                    google_tasks_client.find_and_complete_task(obsidian_task[0])
                    obsidian_client.remove_task_from_daily_note(obsidian_task[0])
                if obsidian_task[1] == 'incomplete':
                    if obsidian_task[0] not in [x['title'] for x in google_tasks]:
                        google_tasks_client.add_task(obsidian_task[0])
                        print(f"Task '{obsidian_task[0]}' added to Google Tasks.")
               
    def on_delete(event):
        print(f"File deleted: {event.src_path}")
    
    daily_note_handler = DailyNoteHandler(
        on_created_callbacks=[on_create], 
        on_modified_callbacks=[on_modifiy], 
        on_deleted_callbacks=[on_delete]
    )
    
    daily_note_handler.start_observing(path=daily_notes_path, file_extension='.md')
    
