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
- Take care of the errors that are going to appear on URL Problems

**Taking Care of the Errors Notes**
- This code snippet that I have here is what we can use when we need to take carre of errors.
- The best ideia is to force the erros and on the `except` have this so we can find all the data we need to then fix the errors we encounter directly. Other way we can force the error and look in the terminal because all the data is there.
**Exceptions:** https://requests.readthedocs.io/en/latest/api/#exceptions


```
except Exception as e:
    print(f"Tipo de erro: {type(e).__name__}")
    print(f"Módulo: {type(e).__module__}")
    print(f"Mensagem: {e}")
```
- **Important:** This Snippet should only be used for testing not as a final version of the code.  

**Orders of the Exceptions MATTER**

- We need to catch the most specific exceptions first and then the most generics so in this view :
- The last except we will have is the RequestException

RequestException (main)
├── ConnectionError
├── Timeout
│   └── ReadTimeout
├── HTTPError
└── ...