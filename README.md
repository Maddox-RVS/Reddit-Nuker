# Python Reddit Nuker

The Python Reddit Nuker is a program designed to delete your comments and/or posts on Reddit. This readme file provides instructions on how to set up and use the program effectively.

## Prerequisites

Before using the Python Reddit Nuker, ensure that you have the following:

1. Python: The program requires Python to be installed on your system. You can download Python from the official Python website: [python.org](https://www.python.org).

## Setup

To set up the Python Reddit Nuker program, follow these steps:

1. Download the Python Reddit Nuker program files.

2. Open a terminal or command prompt and navigate to the directory where the program files are located.

3. Install the required dependencies by running the following command:

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

## Usage

To use the Python Reddit Nuker program, follow these steps:

1. Open a terminal or command prompt and navigate to the directory where the program files are located.

2. Open the `credentials.txt` file in a text editor.

3. Enter your Reddit account credentials and the `clientID` and `clientSecret` obtained from the previous step in the following format:

   ```
   handle = <your_reddit_username>
   passcode = <your_reddit_password>
   clientID = <your_reddit_clientID>
   clientSecret = <your_reddit_clientSecret>
   ```

   Replace `<your_reddit_username>`, `<your_reddit_password>`, `<your_reddit_clientID>`, and `<your_reddit_clientSecret>` with your actual Reddit account information.

4. Save the `credentials.txt` file.

5. Run the Python Reddit Nuker program by executing the following command:

   ```bash
   python <program_file_name>.py
   ```

   Replace `<program_file_name>` with the actual name of the program file.

6. The program will prompt you to confirm whether you want to nuke your newest 100 comments and/or posts. Answer the prompts accordingly.

7. If confirmed, the program will start deleting the selected comments and/or posts. The progress will be displayed with a progress bar.

8. Once the nuking process is finished, the program will display a completion message.

**Note:** Be cautious when using the Python Reddit Nuker as it permanently deletes your comments and/or posts. Deleted content cannot be recovered.

## Additional Notes

- The program retrieves the newest 100 comments and/or posts and deletes them, it cannot do more than 100 at a time because PRAW respects reddit's request limit of a maximum of 100 requests at a time.

- The program uses the Colorama library to display a progress bar and text in color.

- The program ONLY works for the Windows operating system, sorry MAC users ¯\\_(ツ)_/¯ 