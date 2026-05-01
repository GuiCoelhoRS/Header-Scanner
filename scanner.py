import requests 

## Imports for the needed functions ==============================================================================================================================================
from config import TIMEOUT, SECURITY_HEADERS
from analyzers import (
    analyze_x_content_type_options,
    analyze_x_frame_options,
    analyze_referrer_policy,
    analyze_strict_transport_security,
    analyze_permissions_policy,
    analyze_content_security_policy,
)


# URLs for Testing the Program (CLI support is the next thing I want to add still have to learn it) =======================================================================

# URL = 'https://github.com/'
# URL = 'https://site-que-nao-existe-12345.pt/' 
# URL = 'https://httpstat.us/200?sleep=15000'
# URL = 'https://example.com/'
URL = 'https://pypi.org/'
# URL = 'https://www.ulusofona.pt/' 
# URL = 'https://www.bancomontepio.pt/'





# Main Program Loop ==============================================================================================================================================
try:
    r = requests.get(URL, timeout=TIMEOUT)

    ## Show the Status Code of the URL
    print("=== Status Code ===")
    print(f"URL: {r.url} ")
    print(f"Status Code: {r.status_code}")

    lengthHeaders = len(r.headers)

    print(f"Total of received headers : {lengthHeaders}")

    # Showing the Security Headers and giving a small Report
    countSH = 0
    for s in SECURITY_HEADERS :
        if s in r.headers:
            value = r.headers[s]
            print(f"✅ {s}: {value}")
            countSH = countSH + 1

            # Report for X-Content-Type-Options
            if s == "X-Content-Type-Options":
                grade, message = analyze_x_content_type_options(value)
                print(f"   ↳ Grade: {grade} — {message}")
            
            # Report for X-Frame-Options
            if s == "X-Frame-Options":
                grade, message = analyze_x_frame_options(value)
                print(f"   ↳ Grade: {grade} — {message}")

            # Report for Referrer-Policy
            if s == "Referrer-Policy":
                grade, message = analyze_referrer_policy(value)
                print(f"   ↳ Grade: {grade} — {message}")

            # Report for Strict-Transport-Security
            if s == "Strict-Transport-Security":
                grade, message = analyze_strict_transport_security(value)
                print(f"   ↳ Grade: {grade} — {message}")

            if s == "Permissions-Policy":
                grade, message = analyze_permissions_policy(value)
                print(f"   ↳ Grade: {grade} — {message}")

            if s == "Content-Security-Policy":
                grade, message = analyze_content_security_policy(value)
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

    



