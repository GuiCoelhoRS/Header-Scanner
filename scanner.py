import requests 

# =============================== Global Variables ===============================

# URL = 'https://github.com/'
# URL = 'https://site-que-nao-existe-12345.pt/' 
# URL = 'https://httpstat.us/200?sleep=15000'
# URL = 'https://example.com/'
# URL = 'https://pypi.org/'
# URL = 'https://www.ulusofona.pt/' 
URL = 'https://www.bancomontepio.pt/'

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
# def analyze_x_content_type_options():



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
            print(f"✅ {s}: {r.headers[s]}")
            countSH = countSH + 1
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

    



