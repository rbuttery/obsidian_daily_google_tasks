## Add Google Tasks Into Obsidian With Python

### How It Works
1. Python uses the [watchdog](https://pypi.org/project/watchdog/) library to observe changes in your Obsidian Vault.
2. [clients\google_tasks_client.py](https://github.com/rbuttery/obsidian_daily_google_tasks/blob/main/clients/google_tasks_client.py) is a basic Google Tasks client. For this to work, you must first obtain a credentials.json service account file from Google Cloud Console - this is free, but is not straight forward for anyone not familiar. Reach out if you need help setting this up! 
3. [clients\obsidian_client.py](https://github.com/rbuttery/obsidian_daily_google_tasks/blob/main/clients/obsidian_client.py) needs your "OBSIDIAN_VAULT" environment variable. To set this up, navigate to [.env](https://github.com/rbuttery/obsidian_daily_google_tasks/blob/main/clients/.env) and input the folder in which your Obsidian Valut is located.


### Installation
1. Clone this repo (requires git is installed)
    ``` powershell
    git clone https://github.com/rbuttery/obsidian_daily_google_tasks.git
   ```
2. Have python installed, or install python.
    - https://www.python.org/downloads/windows/

3. Run setup.bat
    ``` powershell
    setup.bat
    ```
    - you can also just click on this file to run it!

4. Run launch_obsidian_with_watchdog.bat
   ⚠️ Requires that you have added your Google Cloud credentials.json file into the same directory. Follow the [Google Task Python Quickstart](https://developers.google.com/tasks/quickstart/python) from Google to get started. Sepcifically, the part on [Authentication](https://developers.google.com/tasks/quickstart/python#authorize_credentials_for_a_desktop_application)
   ``` powershell
   launch_obsidian_with_watchdog.bat
   ```

### Optional but recommended: **Pin to your taskbar**
5.  Create a shortcut on your desktop.

    - Right click & create a new "shortcut" on your desktop. 

    - The "location" of this shortcut should point towards launch_obsidian_with_watchdog.bat. 

    - Name this something like "Obsidian Python".

    - Next, let's edit the shortcut:
        - right click + "properties"
        - under "shortcut" select "change icon..."
        - browse & select the included "obsidian-icon.ico" file. Apply this changes.
        - next, still from inside the "properties" panel, find the line that is "Target". Add the word "explorer " with a space to the BEGINNING of the "Target" field: 
        
        ``` powershell
        explorer C:\YOUR\PATH\HERE
        ```
        
        - apply these changes & close the "properties".
        - Now drag the new shortcut to your task bar, and you will have a 1 click launcher that launches the python script & your Obsidian.exe application.


### Notes:
- Only tested on Windows
