import requests 
import argparse 

## Imports for the needed functions ==============================================================================================================================================
from config import TIMEOUT, SECURITY_HEADERS
from analyzers import ANALYZERS

# Argument and CLI Support ========================================================================================================================================
parser = argparse.ArgumentParser(
    description="Audit HTTP security headers of a website."
)
parser.add_argument("url", help="The URL to scan (e.g. https://github.com)")
args = parser.parse_args()

URL = args.url

# Main Program Loop ==============================================================================================================================================
try:
    r = requests.get(URL, timeout=TIMEOUT)

    ## Show the Status Code of the URL
    print("=== Status Code ===")
    print(f"URL: {r.url} ")
    print(f"Status Code: {r.status_code}")

    lengthHeaders = len(r.headers)

    print(f"Total of received headers : {lengthHeaders}")

    # Showing the Security Headers and giving a Report and Note
    countSH = 0
    for s in SECURITY_HEADERS :
        if s in r.headers:
            value = r.headers[s]
            print(f"✅ {s}: {value}")
            countSH = countSH + 1

            if s in ANALYZERS:
                grade,message = ANALYZERS[s](value)
                print(f"   ↳ Grade: {grade} — {message}")
        else :
            print(f"❌ {s}: MISSING")
    
    print(f"Report : This URL: {URL} has {countSH} out of {len(SECURITY_HEADERS)} Security Headers")

# =============================== Error Handling ======================================================================================================

# This takes care of URLS that take a long time to answer to the GET
except requests.exceptions.Timeout as e:
    print(f"Timeout when trying to access {URL}: the website didn't answer in {TIMEOUT}s")

# This except block should always take care of Connection Error Problems and give us a Report of what happened
except requests.exceptions.ConnectionError as e:
    print(f"Connection error when accessing {URL}: {e}")

# This is the final block that should catch everything that passes the other exceptions
except requests.exceptions.RequestException as e:
     print(f"Unexpected error when accessing {URL}: {e}")

    



