import requests

url = "https://www.caberj.com.br/wspls/WS005.apw"

querystring = {"WSDL":""}

payload = ""
headers = {
    "cookie": "SESSIONID=36c9c80f7d7d823affe2b4d5d3522477",
    "Authorization": "Basic cmVzdHVzZXI6UEBzc3cwcmQyMDIz"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)