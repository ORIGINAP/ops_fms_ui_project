import requests

req = requests.get('http://127.0.0.1:8000/hello?name=James')

print(req.text)
