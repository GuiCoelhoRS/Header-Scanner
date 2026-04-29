import requests 

r = requests.get('https://github.com/')

## Show the Status Code of the URL
print("----------------Status Code------------------")
firstComment = f"This {r.url} has a status of {r}"
print(firstComment)

## Showing the headers 
print("----------------Headers------------------")
for k,i in r.items():
    print(k.headers)


