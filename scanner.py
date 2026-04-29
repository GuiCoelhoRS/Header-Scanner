import requests 

# URL = 'https://github.com/'
# URL = 'https://site-que-nao-existe-12345.pt/' 
URL = 'https://httpstat.us/200?sleep=15000'

TIMEOUT = 10

try:
    r = requests.get(URL, timeout=TIMEOUT)

    ## Show the Status Code of the URL
    print("=== Status Code ===")
    print(f"URL: {r.url} ")
    print(f"Status Code: {r.status_code}")


    ## Showing the headers 
    print("=== Headers ===")
    for nome_header,valor in r.headers.items():
        print(nome_header,":",valor)
    
    lengthHeaders = len(r.headers)

    print(f"Total de headers Recebidos : {lengthHeaders}")



# This takes care of URLS that take a long time to answer to the GET
except requests.exceptions.ReadTimeout as e:
    print(f"Timeout ao aceder a {URL}: o site não respondeu em {TIMEOUT}s")
except requests.exceptions.Timeout as e:
    print(f"Timeout ao aceder a {URL}: o site não respondeu em {TIMEOUT}s")


# This except block should always take care of Connection Error Problems and give us a Report of what happened
except requests.exceptions.ConnectionError as e:
    print(f"Erro de ligação a {URL}: {e}")

# This is the final block that should catch everything that passes the other exceptions
except requests.exceptions.RequestException as e:
    print(f"Erro inesperado ao aceder a {URL}: {e}")

    



