import urllib.parse

values = "https://test test"

data = urllib.parse.quote(values)
print(data)
