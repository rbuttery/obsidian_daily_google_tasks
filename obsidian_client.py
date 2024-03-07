import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

class ObsidianClient:
    def __init__(self) -> None:
        self.obsidian_dir = os.getenv("OBSIDIAN_VAULT")
        self.template_path = os.path.join(self.obsidian_dir, "Templates", "Daily Planning Template.md")

    def get_note_path(self, date):
        """Helper function to generate the note path based on a date."""
        return os.path.join(self.obsidian_dir, "Daily Notes", f"{date.strftime('%A, %B %d, %Y')}.md")

    def get_note_content(self, note_path):
        """Helper function to get or create note content."""
        if not os.path.exists(note_path):
            # If the note does not exist, create it from the template
            with open(self.template_path, 'r') as template_file:
                template_content = template_file.read()

            with open(note_path, 'w') as note_file:
                note_file.write(template_content)
                return template_content
        else:
            with open(note_path, 'r', encoding='utf-8') as note_file:
                return note_file.read()

    def get_today_daily_note(self):
        # Format today's date as "Wednesday, March 06, 2024"
        today = datetime.now().strftime("%A, %B %d, %Y")
        # Define the file path for today's daily note
        daily_note_path = os.path.join(f"{self.obsidian_dir}\\Daily Notes", f"{today}.md")

        # Check if today's daily note exists
        if not os.path.exists(daily_note_path):
            # If the note does not exist, create it from the template
            with open(self.template_path, 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            with open(daily_note_path, 'w', encoding='utf-8') as daily_note_file:
                daily_note_file.write(template_content)
                daily_note_content = daily_note_file
            
            print(f"Created today's daily note: {daily_note_path}")
        else:
            # Open and return the note
            with open(daily_note_path, 'r', encoding='utf-8') as daily_note_file:
                daily_note_content = daily_note_file.read()
            print(f"Today's daily note already exists: {daily_note_path}")
        
        return daily_note_content
    
    def get_tomorrows_daily_note(self):
        """Get or create tomorrow's daily note based on the template."""
        tomorrow = datetime.now() + timedelta(days=1)
        note_path = self.get_note_path(tomorrow)
        return self.get_note_content(note_path)

    def get_yesterdays_daily_note(self):
        """Get yesterday's daily note if it exists."""
        yesterday = datetime.now() - timedelta(days=1)
        note_path = self.get_note_path(yesterday)
        if os.path.exists(note_path):
            with open(note_path, 'r', encoding='utf-8') as note_file:
                return note_file.read()
        else:
            print("Yesterday's daily note does not exist.")
            return None


if __name__ == "__main__":
    obsidian = ObsidianClient()
    print("\n-----------------\nYesterday's Note:\n-----------------\n")
    print(obsidian.get_yesterdays_daily_note())
    print("\n-----------------\nToday's Note:\n-----------------\n")
    print(obsidian.get_today_daily_note())
    print("\n-----------------\nTomorrow's Note:\n-----------------\n")
    print(obsidian.get_tomorrows_daily_note())

