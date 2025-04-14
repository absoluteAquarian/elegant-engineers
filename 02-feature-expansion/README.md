# Leaderboard Tracker
This simple application allows users to create usernames and submit scores for those usernames to a leaderboard.

## Setup Instructions
1. Clone the repository
    ```commandline
    git clone https://github.com/absoluteAquarian/elegant-engineers.git
    ```
2. Navigate to this directory
    ```commandline
    cd 01-functional-prototype
    ```
3. Install the dependencies
    ```commandline
    pip install -r requirements.txt
    ```
4. Run the application
    ```commandline
    python run.py
    ```

## How to Use the Application
Upon running the application, you will be brought to the index (`/`) page.  
From this page, you can either add a new username, submit a new score or view the leaderboard of existing scores.

Due to the simplicity of the application, there isn't much else to describe here.

The intended functionality would be that scores can only be submitted for existing users, but difficulties with the database API resulted in this being only semi-completed.  
However, the main feature — the leaderboard — is completely functional.

## How to use new feature: File Submission
When entering the submit a score page, you will now be given the option to upload a file of your score to the leaderboard.

This serves the purpose of providing proof of your score to the scoreboard, reminiscant of real life speedrun boards to record scores and times

## Screenshots
Initial page:
![image](https://github.com/user-attachments/assets/05617847-2039-4097-9dd5-65bff79b9a28)

User Registration page:
![image](https://github.com/user-attachments/assets/97a9f822-bf63-464b-af78-1e03781bbc73)

Score submission page:
![image](https://github.com/user-attachments/assets/1bc47cfc-8395-4258-9201-f6d9f6d5610b)

Leaderboard page:
![image](https://github.com/user-attachments/assets/70b89832-8389-461e-8afe-420ae94d636a)
