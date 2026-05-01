import requests 

# =============================== Global Variables ===============================

# === URLS for Testing ===

URL = 'https://github.com/'
# URL = 'https://site-que-nao-existe-12345.pt/' 
# URL = 'https://httpstat.us/200?sleep=15000'
# URL = 'https://example.com/'
# URL = 'https://pypi.org/'
# URL = 'https://www.ulusofona.pt/' 
# URL = 'https://www.bancomontepio.pt/'

TIMEOUT = 10

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Permissions-Policy",
    "Referrer-Policy",  
]    

# =============================== Functions for Reports  ===============================

# ============= Function to analyze the Security Header X-Content-Type-Options =============
# This header helps us avoid MIME Type Sniffing
def analyze_x_content_type_options(value):
    normalized = value.strip().lower()
    if normalized == "nosniff":
        return "A", "Correctly configured with 'nosniff'"
    else :
        return "F", "Invalid value. Should be 'nosniff'"
    
# ============= Function to analyze the Security Header X-Frame-Options =============
#
def analyze_x_frame_options(value):
    # To catch duplicate headers it happened when I was testing so I added this case
    if "," in value:
        return "F", f"Multiple/duplicate values detected: {value}"
    
    normalized = value.strip().lower()

    if normalized == "deny":
        return "A","It will never be loaded in an iframe"
    elif normalized == "sameorigin":
        return "B","It has to be an iframe from the same origin"
    elif normalized.startswith("allow-from"):
        return "C","Deprecated, ignored by modern browsers"
    else :
        return "F","Invalid value. Should be DENY or SAMEORIGIN"
    
# ============= Function to analyse the Security Header Referrer-Policy =============
# This header controls the information that is send when we click on a link to other website
def analyze_referrer_policy(value):
    if "," in value:
        value = value.split(",")[0]

    normalized = value.strip().lower()

    if normalized == "no-referrer":
        return "A+","Never sends a referrer"
    elif normalized in ("same-origin","strict-origin","strict-origin-when-cross-origin"):
        return "A", "Strong privacy protection"
    elif normalized == "no-referrer-when-downgrade":
        return "B", "Default for older browsers"
    elif normalized == "origin":
        return "B", "Always sends the origin"
    elif normalized == "origin-when-cross-origin":
        return "C","Leaks path on same-origin requests"
    elif normalized == "unsafe-url":
        return "F","Privacy risk — leaks full URL even on HTTPS to HTTP"
    else :
        return "F", f"Invalid or unknown value: {value}"


# =============================== Main Program  ===============================


try:
    r = requests.get(URL, timeout=TIMEOUT)

    ## Show the Status Code of the URL
    print("=== Status Code ===")
    print(f"URL: {r.url} ")
    print(f"Status Code: {r.status_code}")


    ## This snippet can be used for debug but it's not needed for the project
    ## Showing the headers 
    # print("=== Headers ===")
    # for nome_header,valor in r.headers.items():
    #    print(nome_header,":",valor)
    
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
        else :
            print(f"❌ {s}: MISSING")
    
    print(f"Report : This URL: {URL} has {countSH} out of {len(SECURITY_HEADERS)} Security Headers")


# =============================== Error Handling ===============================

# This takes care of URLS that take a long time to answer to the GET
except requests.exceptions.Timeout as e:
    print(f"Timeout when trying to access {URL}: the website didn't answer in {TIMEOUT}s")


# This except block should always take care of Connection Error Problems and give us a Report of what happened
except requests.exceptions.ConnectionError as e:
    print(f"Connection error when accessing {URL}: {e}")

# This is the final block that should catch everything that passes the other exceptions
except requests.exceptions.RequestException as e:
     print(f"Unexpected error when accessing {URL}: {e}")

    



