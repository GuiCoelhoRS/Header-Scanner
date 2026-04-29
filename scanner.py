import requests 


r = requests.get('https://github.com/')

## Show the Status Code of the URL
print("=== Status Code ===")
print(f"URL : {r.url} ")
print(f"Status Code: {r.status_code}")


## Showing the headers 
print("=== Headers ===")
for nome_header,valor in r.headers.items():
    print(nome_header,":",valor)


print(len(r.headers))