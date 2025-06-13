# Python Reddit Nuker

Python Reddit Nuker is a command-line tool that allows you to quickly and permanently delete your Reddit comments and/or posts in bulk. It uses the Reddit API (via PRAW) to authenticate your account and provides a simple interactive interface for selecting and confirming which content to remove. The tool displays progress and status updates in the terminal, making it easy to manage your Reddit data deletion securely and efficiently.

<img src="https://github.com/user-attachments/assets/3dab42e0-a541-4749-b2bc-599a99d3b0f0" alt="Reddit Nuker GIF" width="1000"/>

## Prerequisites

Before using the Python Reddit Nuker, ensure that you have the following:

1. Python: The program requires **Python (3.13.4 recommended)** to be installed on your system. You can download Python from the official Python website: [python.org](https://www.python.org).
2. [Anaconda or Miniconda](https://www.anaconda.com/docs/main) (recommended for managing environments).
3. [Git](https://git-scm.com/) (for cloning the repository).

## Setup

To set up the Python Reddit Nuker program, follow these steps:

1. **Clone the repository using git:**

   ```bash
   git clone https://github.com/Maddox-RVS/Reddit-Nuker.git
   cd Reddit-Nuker
   ```

2. **Create and activate a conda environment (recommended):**

   ```bash
   conda create -n reddit-nuker python=3.13.4
   conda activate reddit-nuker
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Retrieving Reddit Account Client ID and Client Secret

To retrieve your Reddit account's `clientID` and `clientSecret`, you need to create a Reddit app. Follow these steps:

1. Go to the [Reddit Apps page](https://www.reddit.com/prefs/apps).

2. Scroll down to the "Developed Applications" section and click the "Create App" button.

3. Fill in the required fields: name, description, and about url (optional).

4. Select the app type as "script".

5. In the "About" section, enter a redirect URI. This can be any valid URL, such as `http://localhost:8080`.

6. Click the "Create app" button.

7. Once the app is created, you will see the `clientID` (clientID is underneath "personal use script") and `clientSecret` (clientSecret is next to "secret") on the app details page. Make a note of these values as you will need them during the setup process.

8. Set the following environment variables in your terminal or system before running the program:

   - `REDDIT_CLIENT_ID`
   - `REDDIT_CLIENT_SECRET`

   For example, on Windows Command Prompt:

   ```cmd
   set REDDIT_CLIENT_ID=your_client_id
   set REDDIT_CLIENT_SECRET=your_client_secret
   ```

   Or on PowerShell:

   ```powershell
   $env:REDDIT_CLIENT_ID="your_client_id"
   $env:REDDIT_CLIENT_SECRET="your_client_secret"
   ```

## Usage

To use the Python Reddit Nuker program, follow these steps:

1. Open a terminal or command prompt and navigate to the directory where the program files are located.

2. Make sure your `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET` environment variables are set as described above.

3. Run the Python Reddit Nuker program by executing the following command:

   ```bash
   python nuke.py
   ```

4. The program will prompt you to enter your Reddit username and password interactively.

5. The program will prompt you to choose a specific nuking action.

6. The program will prompt you to confirm whether you want to nuke your comments and/or posts. Answer the prompts accordingly.

7. If confirmed, the program will start deleting the selected comments and/or posts. The progress will be displayed with a progress bar.

**Note:** Be cautious when using the Python Reddit Nuker as it permanently deletes your comments and/or posts. Deleted content cannot be recovered.

## Additional Notes

- The program uses ANSI escape codes for some terminal effects (such as clearing lines), which may not be supported in all terminal environments. Regardless, the core program logic should work on any OS where Python, PRAW, and Rich are supported
- **Be cautious: deleted comments and posts cannot be recovered.**