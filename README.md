# Taskify
Task Management Project 

## Group Members:

- Eric Nguyen
- Jonathan Wu

## Project Description: A short summary of what the application does.
This is a task management application that allows the user to create an account and manage tasks.
Once the user logins, they can add tasks, view, or edit tasks, and logout.

## Dependencies: List all external Python libraries required.
This application uses the following libraries that need to be installed:
- tkcalendar
- matplotlib
- SQLAlchemy

## Setup and Execution Instructions: Clear, step-by-step instructions on how to set up the environment 
Install dependencies by running: `pip install -r requirements.txt`

Run the application by running `python src/main.py`.

## File Structure Overview: Briefly describe the purpose of the main files and directories in your project archive.
The src directory contains all the python files. The main.py file can be found it in that runs the application. 
There are different folders that contain the different components of our project. The database folder contains the files that configure and manage database interactions.
The gui directory contains the folder of pages and widgets used to create the User Interface.
The model directory holds the Users and Task table we create for our database.

## Known Bugs or Limitations: List any known issues or features that are not fully implemented.
Our application expects that the user follows the proper flow of registering, logging in, creating tasks, editing, and revising tasks.
There may still be possible corner cases that cause bugs that have not all been found yet.
The current application is limited in scope. Future features may include different visualizations and color coding to help users find tasks more easily.
