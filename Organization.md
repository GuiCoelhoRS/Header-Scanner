Verifying Python Version on CMD : `python --version`

Creating the Virtual Environemnt : `python -m venv venv`
Activate the Venv : `source venv/bin/activate`

- Now we can see (venv) in the terminal Lines that means we are on the virtual environment of the project so we can install any packages just on this project.

Installing the requests librar : `pip install requests`
Create the requirements.txt : `pip freeze > requirements.txt`

- The file requirements.txt contains the tools that the requests library has for it to work. 


### 1 º Phase of the Build
- Receive an URL (harcoded for now)
- Do an HTTP Request to that URL
- Show the headers of the answer on the CLI
